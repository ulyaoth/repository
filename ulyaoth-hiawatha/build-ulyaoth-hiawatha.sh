ulyaothos=`cat /etc/ulyaoth`
fedoraos=`cat /etc/ulyaoth`

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hiawatha/SPECS/ulyaoth-hiawatha.spec"
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hiawatha/SPECS/ulyaoth-hiawatha-letsencrypt.spec"

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

if grep --quiet 19 /etc/fedora-release; then
  wget http://www.hiawatha-webserver.org/files/hiawatha-10.6.tar.gz -P /home/ulyaoth/rpmbuild/SOURCES
fi

if type dnf 2>/dev/null
then
  dnf remove -y cmake
elif type yum 2>/dev/null
then
  yum remove -y cmake
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-hiawatha.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-hiawatha.spec
fi

su ulyaoth -c "spectool ulyaoth-hiawatha.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-hiawatha.spec"
su ulyaoth -c "rpmbuild -ba ulyaoth-hiawatha-letsencrypt.spec"

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

rm -rf /root/build-ulyaoth-*.sh
rm -rf /home/ulyaoth/rpmbuild
