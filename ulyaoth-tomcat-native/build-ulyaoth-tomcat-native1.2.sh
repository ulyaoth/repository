ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

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

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/SPECS/ulyaoth-tomcat-native1.2.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat-native1.2.spec
fi

if type dnf 2>/dev/null
then
  dnf remove -y apr apr-devel
  dnf install -y java-1.8.0-openjdk-devel
  dnf builddep -y ulyaoth-tomcat-native1.2.spec
elif type yum 2>/dev/null
then
  yum remove -y apr apr-devel
  yum install -y java-1.8.0-openjdk-devel
  yum-builddep -y ulyaoth-tomcat-native1.2.spec
fi

su ulyaoth -c "spectool ulyaoth-tomcat-native1.2.spec -g -R"

if grep -q -i "release 19" /etc/fedora-release || grep -q -i "release 20" /etc/fedora-release || grep -q -i "release 21" /etc/fedora-release || grep -q -i "release 22" /etc/fedora-release
then
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
elif grep -q -i "release 6" /etc/redhat-release || grep -q -i "release 7" /etc/redhat-release
then
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
elif grep -q -i "amazon" /etc/ulyaoth
then
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
else
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
fi

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