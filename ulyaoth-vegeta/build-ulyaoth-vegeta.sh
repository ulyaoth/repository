# Required variables.
os=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
vegetaversion=6.1.0

# Check if we are using a 32-bit system.
if [ "$arch" == "i686" ]
then
arch="i386"
fi

if [ "$os" == "fedora" ]
then
if type dnf 2>/dev/null
then
  dnf install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.fedora.noarch.rpm -y
elif type yum 2>/dev/null
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.fedora.noarch.rpm -y
fi
elif [ "$os" == "redhat" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.redhat.noarch.rpm -y
elif [ "$os" == "amazonlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.amazonlinux.noarch.rpm -y
elif [ "$os" == "centos" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.centos.noarch.rpm -y
elif [ "$os" == "oraclelinux" ]
then 
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.oraclelinux.noarch.rpm -y
elif [ "$os" == "scientificlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-1.1.0-1.scientificlinux.noarch.rpm -y
fi

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"

if type dnf 2>/dev/null
then
  dnf install ulyaoth-go -y
elif type yum 2>/dev/null
then
  yum install ulyaoth-go -y
fi

# Add where to find go into bashrc
echo 'export GOROOT=/usr/local/go' >> /home/ulyaoth/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /home/ulyaoth/.bashrc
echo 'export GOPATH=/home/ulyaoth/' >> /home/ulyaoth/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /home/ulyaoth/.bashrc
echo 'export GOBIN=/usr/local/go/bin/' >> /home/ulyaoth/.bashrc

su ulyaoth -c "source ~/.bashrc"

# Download vegeta and build it.
su - ulyaoth -s /usr/bin/bash -c "wget https://github.com/tsenart/vegeta/archive/v'"$vegetaversion"'.tar.gz"
su - ulyaoth -s /usr/bin/bash -c "tar xvzf v'"$vegetaversion"'.tar.gz"
su - ulyaoth -s /usr/bin/bash -c "go get -u github.com/tsenart/vegeta"
su - ulyaoth -s /usr/bin/bash -c "rm -rf /home/ulyaoth/src/github.com/tsenart/vegeta"
su - ulyaoth -s /usr/bin/bash -c "mv vegeta-'"$vegetaversion"' /home/ulyaoth/src/github.com/tsenart/vegeta"
su - ulyaoth -s /usr/bin/bash -c "cd /home/ulyaoth/src/github.com/tsenart/vegeta/ && go build"
su - ulyaoth -s /usr/bin/bash -c "mv /home/ulyaoth/src/github.com/tsenart/vegeta/vegeta /home/ulyaoth/rpmbuild/SOURCES/"
su - ulyaoth -s /usr/bin/bash -c "rm -rf src v'"$vegetaversion"'.tar.gz pkg"

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-vegeta/SPECS/ulyaoth-vegeta.spec"

# If we use 32-bit then change specifile to build for 32-bit.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-vegeta.spec
fi

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-vegeta.spec"

# Copy the rpms to root directory.
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/

# Clean everything we needed to build the rpm.
rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-vegeta.sh