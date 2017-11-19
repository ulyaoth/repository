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
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/SPECS/ulyaoth-tomcat-native.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat-native.spec

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf remove -y apr-devel
  sudo dnf install -y java-1.8.0-openjdk-devel
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat-native.spec
elif type yum 2>/dev/null
then
  sudo yum remove -y apr-devel
  sudo yum install -y java-1.8.0-openjdk-devel
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat-native.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat-native.spec -g -R

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tomcat-native.spec