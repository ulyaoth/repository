# Required variables.
ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
legoversion=0.3.1

# Check if we are using a 32-bit system.
if [ "$arch" == "i686" ]
then
arch="i386"
fi

if [ "$ulyaothos" == "fedora" ]
then
if type dnf 2>/dev/null
then
  dnf install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.x86_64.rpm -y
elif type yum 2>/dev/null
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.x86_64.rpm -y
fi
elif [ "$ulyaothos" == "redhat" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.redhat.x86_64.rpm -y
elif [ "$ulyaothos" == "amazonlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.amazonlinux.x86_64.rpm -y
elif [ "$ulyaothos" == "centos" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.centos.x86_64.rpm -y
elif [ "$ulyaothos" == "oraclelinux" ]
then 
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.oraclelinux.x86_64.rpm -y
elif [ "$ulyaothos" == "scientificlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.scientificlinux.x86_64.rpm -y
fi

# Install Go
if type dnf 2>/dev/null
then
  dnf install ulyaoth-go -y
elif type yum 2>/dev/null
then
  yum install ulyaoth-go -y
fi

# Create the rpmbuild directory.
su ulyaoth -c "rpmdev-setuptree"

# Build
cd /root
echo 'export GOROOT=/usr/local/ulyaoth/go' >> /root/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /root/.bashrc
echo 'export GOPATH=/root/' >> /root/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /root/.bashrc
echo 'export GOBIN=/usr/local/ulyaoth/go/bin/' >> /root/.bashrc
source ~/.bashrc
/usr/local/ulyaoth/go/bin/go get -u github.com/xenolf/lego
cd /root/src/github.com/xenolf/lego/ && go build
mv /root/src/github.com/xenolf/lego/lego /home/ulyaoth/rpmbuild/SOURCES/
chown ulyaoth:ulyaoth /home/ulyaoth/rpmbuild/SOURCES/lego

# Create build user and go to it's home directory.
useradd ulyaoth

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lego/SPECS/ulyaoth-lego.spec"

# If we use 32-bit then change specifile to build for 32-bit.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-lego.spec
fi

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-lego.spec"

# Copy the rpms to root directory.
if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

# Clean everything we needed to build the rpm.
rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild