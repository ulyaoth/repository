# Required variables.
ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
logstashforwarderversion=0.4.0

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
echo 'export GOROOT=/usr/local/go' >> /home/ulyaoth/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /home/ulyaoth/.bashrc
echo 'export GOPATH=/home/ulyaoth/' >> /home/ulyaoth/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /home/ulyaoth/.bashrc
echo 'export GOBIN=/usr/local/go/bin/' >> /home/ulyaoth/.bashrc

su ulyaoth -c "source ~/.bashrc"

# Download logstash-forwarder and build it.
su - ulyaoth -c "wget https://github.com/elastic/logstash-forwarder/archive/v'"$logstashforwarderversion"'.tar.gz"
su - ulyaoth -c "tar xvzf v'"$logstashforwarderversion"'.tar.gz"
su - ulyaoth -c "mkdir -p /home/ulyaoth/src/github.com/elastic"
su - ulyaoth -c "mkdir -p /home/ulyaoth/bin"
su - ulyaoth -c "mkdir -p /home/ulyaoth/pkg"
su - ulyaoth -c "go get -u github.com/elastic/logstash-forwarder"
su - ulyaoth -c "mv logstash-forwarder-'"$logstashforwarderversion"' /home/ulyaoth/src/github.com/elastic/logstash-forwarder"
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/elastic/logstash-forwarder/ && go build"
su - ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/logstash-forwarder/logstash-forwarder /home/ulyaoth/rpmbuild/SOURCES/"
su - ulyaoth -c "rm -rf bin src v'"$logstashforwarderversion"'.tar.gz pkg"

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash-forwarder/SPECS/ulyaoth-logstash-forwarder.spec"

# If we use 32-bit then change specifile to build for 32-bit.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-logstash-forwarder.spec
fi

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "spectool ulyaoth-logstash-forwarder.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-logstash-forwarder.spec"

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