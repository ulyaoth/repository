# Required variables.
ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
terraformversion=0.11.10

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

if type dnf 2>/dev/null
then
  dnf install ulyaoth-go -y
elif type yum 2>/dev/null
then
  yum install ulyaoth-go -y
fi

# Install Gox
cd /root
echo 'export GOROOT=/usr/local/ulyaoth/go' >> /root/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /root/.bashrc
echo 'export GOPATH=/home/ulyaoth/' >> /root/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /root/.bashrc
echo 'export GOBIN=/usr/local/ulyaoth/go/bin/' >> /root/.bashrc
source ~/.bashrc
go get github.com/mitchellh/gox
go get golang.org/x/tools/cmd/stringer
chown -R ulyaoth:ulyaoth /home/ulyaoth


# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"

# Add where to find go into bashrc
echo 'export GOROOT=/usr/local/ulyaoth/go' >> /home/ulyaoth/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /home/ulyaoth/.bashrc
echo 'export GOPATH=/home/ulyaoth/' >> /home/ulyaoth/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /home/ulyaoth/.bashrc
echo 'export GOBIN=/usr/local/ulyaoth/go/bin/' >> /home/ulyaoth/.bashrc

su ulyaoth -c "source ~/.bashrc"

# Download vegeta and build it.
su - ulyaoth -c "wget https://github.com/hashicorp/terraform/archive/v'"$terraformversion"'.tar.gz"
su - ulyaoth -c "tar xvzf v'"$terraformversion"'.tar.gz"
su - ulyaoth -c "mkdir -p /home/ulyaoth/src/github.com/hashicorp"
su - ulyaoth -c "mkdir -p /home/ulyaoth/bin"
su - ulyaoth -c "mkdir -p /home/ulyaoth/pkg"
su - ulyaoth -c "mv terraform-'"$terraformversion"' /home/ulyaoth/src/github.com/hashicorp/terraform"
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/hashicorp/terraform/ && XC_OS=linux XC_ARCH=amd64 make bin"
su - ulyaoth -c "mv /home/ulyaoth/src/github.com/hashicorp/terraform/bin/terraform /home/ulyaoth/rpmbuild/SOURCES/"
su - ulyaoth -c "rm -rf src v'"$terraformversion"'.tar.gz pkg bin"


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