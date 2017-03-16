ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"

cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-keepalived/SPEC/ulyaoth-keepalived.spec"

if [ "$arch" != "x86_64" ]
then
  sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-keepalived.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-keepalived.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-keepalived.spec
fi

su ulyaoth -c "spectool ulyaoth-keepalived.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-keepalived.spec"

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