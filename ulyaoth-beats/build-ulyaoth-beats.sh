# Required variables.
ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
beatsversion=1.3.0

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

# Download beats and prepare for build.
su ulyaoth -c "wget https://github.com/elastic/beats/archive/v'"$beatsversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$beatsversion"'.tar.gz"
su ulyaoth -c "mkdir -p /home/ulyaoth/src/github.com/elastic"
su ulyaoth -c "mv beats-'"$beatsversion"' /home/ulyaoth/src/github.com/elastic/beats"

# Build Topbeat and move to rpmbuild source.
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/elastic/beats/topbeat/ && gmake"
su ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/beats/topbeat/topbeat /home/ulyaoth/rpmbuild/SOURCES/"

# Build Packetbeat and move to rpmbuild source.
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/elastic/beats/packetbeat/ && gmake"
su ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/beats/packetbeat/packetbeat /home/ulyaoth/rpmbuild/SOURCES/"

# Build Filebeat and move to rpmbuild source.
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/elastic/beats/filebeat/ && gmake"
su ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/beats/filebeat/filebeat /home/ulyaoth/rpmbuild/SOURCES/"

# Delete beats build dir.
su ulyaoth -c "rm -rf src v'"$beatsversion"'.tar.gz"

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SPECS/ulyaoth-beats.spec"

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "spectool ulyaoth-beats.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-beats.spec"

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

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild