# Required variables.
arch="$(uname -m)"
buildarch="$(uname -m)"
topbeatversion=1.2.0
goversion=1.6

# Check if we are using a 32-bit system.
if [ "$arch" == "i686" ]
then
arch="i386"
fi

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"

# Download newest go version.
if [ "$arch" == "i386" ]
then
su ulyaoth -c "wget https://storage.googleapis.com/golang/go'"$goversion"'.linux-386.tar.gz"
su ulyaoth -c "tar xvzf go'"$goversion"'.linux-386.tar.gz"
su ulyaoth -c "rm -rf go'"$goversion"'.linux-386.tar.gz"
else
su ulyaoth -c "wget https://storage.googleapis.com/golang/go'"$goversion"'.linux-amd64.tar.gz"
su ulyaoth -c "tar xvzf go'"$goversion"'.linux-amd64.tar.gz"
su ulyaoth -c "rm -rf go'"$goversion"'.linux-amd64.tar.gz"
fi

# Add where to find go into bashrc
echo 'export GOROOT=/home/ulyaoth/go' >> /home/ulyaoth/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> /home/ulyaoth/.bashrc
echo 'export GOPATH=/home/ulyaoth/' >> /home/ulyaoth/.bashrc
echo 'export PATH=$GOPATH/bin:$PATH' >> /home/ulyaoth/.bashrc
echo 'export GOBIN=/home/ulyaoth/go/bin/' >> /home/ulyaoth/.bashrc

# Download filebeat and build it.
su ulyaoth -c "wget https://github.com/elastic/beats/archive/v'"$topbeatversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$topbeatversion"'.tar.gz"
su ulyaoth -c "mkdir -p /home/ulyaoth/src/github.com/elastic"
su ulyaoth -c "mv beats-'"$topbeatversion"' /home/ulyaoth/src/github.com/elastic/beats"
su - ulyaoth -c "cd /home/ulyaoth/src/github.com/elastic/beats/topbeat/ && gmake"
su ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/beats/topbeat/topbeat /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf src v'"$topbeatversion"'.tar.gz"

# Go to spec file directory and download the spec file.
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-topbeat/SPECS/ulyaoth-topbeat.spec"

# If we use 32-bit then change specifile to build for 32-bit.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-topbeat.spec
fi

# Download the requirements the spec files specifies and build the rpm.
su ulyaoth -c "spectool ulyaoth-topbeat.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-topbeat.spec"

# Copy the rpms to root directory.
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/

# Clean everything we needed to build the rpm.
rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-topbeat.sh
rm -rf /home/ulyaoth/go