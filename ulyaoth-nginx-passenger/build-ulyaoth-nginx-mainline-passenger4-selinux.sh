ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if type dnf 2>/dev/null
then
  dnf install -y policycoreutils-python checkpolicy selinux-policy-devel
elif type yum 2>/dev/null
then
  yum install -y policycoreutils-python checkpolicy selinux-policy-devel
fi

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SELinux/ulyaoth-nginx-mainline-passenger4.txt"
su ulyaoth -c "audit2allow -M ulyaoth-nginx-mainline-passenger4 < ulyaoth-nginx-mainline-passenger4.txt"
su ulyaoth -c "mv ulyaoth-nginx-mainline-passenger4.pp /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SPECS/ulyaoth-nginx-mainline-passenger4-selinux.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-passenger4-selinux.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-mainline-passenger4-selinux.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-mainline-passenger4-selinux.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-mainline-passenger4-selinux.spec"

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