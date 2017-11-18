# This script is supposed to run as the user "ulyaoth".

# Clean repository because AMI could have old data.
if type dnf 2>/dev/null
then
  sudo dnf clean all
elif type yum 2>/dev/null
then
  sudo yum clean all
fi

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-admin.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-admin.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-docs.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-docs.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-examples.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-examples.spec

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-admin.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-docs.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat9-examples.spec