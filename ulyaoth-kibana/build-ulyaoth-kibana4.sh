ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kibana/SPECS/ulyaoth-kibana4.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-kibana4.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-kibana4.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-kibana4.spec
fi

su ulyaoth -c "spectool ulyaoth-kibana4.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-kibana4.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild