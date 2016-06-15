ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

useradd ulyaoth
cd /home/ulyaoth/

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

su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "git clone git://github.com/jgrahamc/httpdiff.git"
su ulyaoth -c "cd /home/ulyaoth/httpdiff/ && go build"
su ulyaoth -c "mv /home/ulyaoth/httpdiff/httpdiff /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf /home/ulyaoth/httpdiff/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-httpdiff/SPECS/ulyaoth-httpdiff.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-httpdiff.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-httpdiff.spec"

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