PKG_REPO=/Users/rfoucher/Documents/

NAGIOSMGR_NAME=nagios-mgr
NAGIOSMGR_VERSION=1.1.1-1
NAGIOSMGR_LABEL="Nagios manager client manage backend database for Ninja"
NAGIOSMGR_LOCATION=~/darwinbuild/nagios_mgr/
NAGIOSMGR_PATH=usr/local/nagios/addons/nagios_mgr/

CHECKNAGIOS_NAME=check-nagios
CHECKNAGIOS_VERSION=1.0.2-1
CHECKNAGIOS_LABEL="Ninja packaging for Nagios Checks"
CHECKNAGIOS_LOCATION=~/darwinbuild/check-nagios/
CHECKNAGIOS_PATH=usr/local/nagios/addons/check-nagios/
cd $NAGIOSMGR_LOCATION
cd $NAGIOSMGR_PATH
git pull
cd $CHECKNAGIOS_LOCATION
cd $CHECKNAGIOS_PATH
git pull

rm -rf $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.pkg
rm -rf $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.dmg
rm -rf $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.pkg
rm -rf $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.dmg

/Applications/PackageMaker.app/Contents/MacOS/PackageMaker \
                        -r $CHECKNAGIOS_LOCATION \
                        -o $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.pkg \
                        -i com.apple.sre.$CHECKNAGIOS_NAME \
                        -n $CHECKNAGIOS_VERSION \
                        -t "$CHECKNAGIOS_LABEL" \
                        -v
hdiutil create -srcfolder $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.pkg $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.dmg 


/Applications/PackageMaker.app/Contents/MacOS/PackageMaker \
                        -r $NAGIOSMGR_LOCATION \
                        -o $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.pkg \
                        -i com.apple.sre.$NAGIOSMGR_NAME \
                        -n $NAGIOSMGR_VERSION \
                        -t "$NAGIOSMGR_LABEL" \
                        -v
hdiutil create -srcfolder $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.pkg $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.dmg

hdiutil attach $PKG_REPO/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.dmg
cd /Volumes/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION/
sudo installer -pkg $CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION.pkg -target "/"
hdiutil detach /Volumes/$CHECKNAGIOS_NAME-$CHECKNAGIOS_VERSION/

ls /$NAGIOSMGR_PATH

hdiutil attach $PKG_REPO/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.dmg 
cd /Volumes/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION/
sudo installer -pkg $NAGIOSMGR_NAME-$NAGIOSMGR_VERSION.pkg -target "/"
hdiutil detach /Volumes/$NAGIOSMGR_NAME-$NAGIOSMGR_VERSION/

ls /$NAGIOSMGR_PATH



