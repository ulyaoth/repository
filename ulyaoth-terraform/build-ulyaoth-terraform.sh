# Required variables.
ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
terraformversion=0.7.0

# Check if we are using a 32-bit system.
if [ "$arch" == "i686" ]
then
arch="i386"
fi

if [ "$ulyaothos" == "fedora" ]
then
if type dnf 2>/dev/null
then
  dnf install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.noarch.rpm -y
elif type yum 2>/dev/null
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.noarch.rpm -y
fi
elif [ "$ulyaothos" == "redhat" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.redhat.noarch.rpm -y
elif [ "$ulyaothos" == "amazonlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.amazonlinux.noarch.rpm -y
elif [ "$ulyaothos" == "centos" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.centos.noarch.rpm -y
elif [ "$ulyaothos" == "oraclelinux" ]
then 
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.oraclelinux.noarch.rpm -y
elif [ "$ulyaothos" == "scientificlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.scientificlinux.noarch.rpm -y
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
echo 'export GOROOT=/usr/local/go' >> /root/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /root/.bashrc
echo 'export GOPATH=/root' >> /root/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /root/.bashrc
echo 'export GOBIN=/usr/local/go/bin' >> /root/.bashrc

source ~/.bashrc

#Create and build terraform
mkdir -p /root/src/github.com/hashicorp

wget https://github.com/hashicorp/terraform/archive/v$terraformversion.tar.gz
tar xvzf v$terraformversion.tar.gz
mv terraform-$terraformversion /root/src/github.com/hashicorp/terraform
cd /root/src/github.com/hashicorp/terraform 

# If we use 32-bit build for 32-bit.
if [ "$arch" != "x86_64" ]
then
XC_OS=linux XC_ARCH=386 make bin
else
XC_OS=linux XC_ARCH=amd64 make bin
fi

mv /root/src/github.com/hashicorp/terraform/bin/terraform /home/ulyaoth/rpmbuild/SOURCES/
chown ulyaoth:ulyaoth /home/ulyaoth/rpmbuild/SOURCES/terraform

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-terraform/SPECS/ulyaoth-terraform.spec"

# If we use 32-bit then change specifile to build for 32-bit.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-terraform.spec
fi

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-terraform.spec"

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
rm -rf /root/bin
rm -rf /root/pkg
rm -rf /root/src
rm -rf /root/$terraformversion.tar.gz
rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild