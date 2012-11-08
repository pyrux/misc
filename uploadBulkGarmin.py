#!/usr/bin/env python

import cookielib
import json
import logging
import os
import poster
import sys
import urllib
import urllib2

_USERNAME = 'user'
_PASSWORD = 'password'

_LOGIN_URL = 'https://connect.garmin.com/signin'
_USERNAME_URL = 'http://connect.garmin.com/user/username'
_UPLOAD_URL = 'http://connect.garmin.com/proxy/upload-service-1.1/json/upload/.gpx'

class GarminConnectUploader:

    def __init__(self):
        self.__opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
            poster.streaminghttp.StreamingHTTPHandler,
            poster.streaminghttp.StreamingHTTPRedirectHandler,
            poster.streaminghttp.StreamingHTTPSHandler)
        self.__logged_in = False

    def __authenticate(self, username, password):
        assert username
        assert password

        logging.info('Getting cookies from Garmin Connect...')
        self.__opener.open(_LOGIN_URL)

        data = {
            'login': 'login',
            'login:loginUsernameField': username,
            'login:password': password,
            'login:signInButton': 'Sign In',
            'javax.faces.ViewState': 'j_id1',
        }

        logging.info('Signing in as %s at %s...', username, _LOGIN_URL)
        self.__opener.open(_LOGIN_URL, urllib.urlencode(data))

        logging.info('Validating authentication step...')
        readback = json.loads(self.__opener.open(_USERNAME_URL).read())
        if readback['username'] != username:
            return False

        logging.info('Succesfully logged in as %s.' % username)
        return True

    def login(self, username, password):
        self.__logged_in = self.__authenticate(username, password)
        return self.__logged_in

    def upload(self, filename):
        assert self.__logged_in
        with open(filename) as f:
            data, headers = poster.encode.multipart_encode({
                'responseContentType': 'text/html',
                'data': f,
            })

            logging.info('Uploading %s to Garmin Connect...', filename)
            self.__opener.open(urllib2.Request(_UPLOAD_URL, data, headers)).read()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <directory>' % sys.argv[0])
        sys.exit(1)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uploader = GarminConnectUploader()
    if not uploader.login(_USERNAME, _PASSWORD):
        logging.error('Error logging in to Garmin Connect!')
        sys.exit(2)

    base = os.path.abspath(sys.argv[1])
    files = sorted(os.listdir(base))
    logging.info('Uploading %d GPX files from %s...', len(files), base)
    for filename in files:
        if filename.endswith('.gpx'):
            uploader.upload(os.path.join(base, filename))
    logging.info('Done uploading %d files to Garmin Connect.', len(files))
