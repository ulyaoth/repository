ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
kafkamanagerversion=1.3.1.8

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if type dnf 2>/dev/null
then
  dnf install java-1.8.0-openjdk-devel -y
elif type yum 2>/dev/null
then
  yum install java-1.8.0-openjdk-devel -y
fi

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"

su ulyaoth -c "wget https://github.com/yahoo/kafka-manager/archive/'"$kafkamanagerversion"'.tar.gz"
su ulyaoth -c "tar xvzf '"$kafkamanagerversion"'.tar.gz"
su ulyaoth -c "cd kafka-manager-'"$kafkamanagerversion"' && ./sbt clean dist"
su ulyaoth -c "mv /home/ulyaoth/kafka-manager-'"$kafkamanagerversion"'/target/universal/kafka-manager-'"$kafkamanagerversion"'.zip /home/ulyaoth/rpmbuild/SOURCES/"

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/SPECS/ulyaoth-kafka-manager.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-kafka-manager.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-kafka-manager.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-kafka-manager.spec
fi

su ulyaoth -c "spectool ulyaoth-kafka-manager.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-kafka-manager.spec"

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
rm -rf /home/ulyaoth/kafka-manager-$kafkamanagerversion
rm -rf /home/ulyaoth/$kafkamanagerversion.tar.gz
rm -rf /home/ulyaoth/.sbt