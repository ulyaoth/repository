# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat8.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat8-admin.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-admin.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat8-docs.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-docs.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat8-examples.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-examples.spec

# Install all requirements
if type dnf 2>/dev/null
then
  dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8.spec
elif type yum 2>/dev/null
then
  yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-admin.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-docs.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat8-examples.spec