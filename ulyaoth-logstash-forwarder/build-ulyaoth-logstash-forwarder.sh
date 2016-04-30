ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
logstashforwarderversion=0.4.0

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
else
echo yeah Fedora!
fi

if type dnf 2>/dev/null
then
  dnf install -y go golang
elif type yum 2>/dev/null
then
  yum install -y go golang
fi

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/elastic/logstash-forwarder/archive/v'"$logstashforwarderversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$logstashforwarderversion"'.tar.gz"
su ulyaoth -c "cd /home/ulyaoth/logstash-forwarder-'"$logstashforwarderversion"'/ && go build"
su ulyaoth -c "mv /home/ulyaoth/logstash-forwarder-'"$logstashforwarderversion"'/logstash-forwarder-'"$logstashforwarderversion"' /home/ulyaoth/rpmbuild/SOURCES/logstash-forwarder"
su ulyaoth -c "rm -rf /home/ulyaoth/logstash-forwarder-'"$logstashforwarderversion"'/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash-forwarder/SPECS/ulyaoth-logstash-forwarder.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-logstash-forwarder.spec
fi

su ulyaoth -c "spectool ulyaoth-logstash-forwarder.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-logstash-forwarder.spec"

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