arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi


if type dnf 2>/dev/null
then
  dnf install -y policycoreutils-python checkpolicy selinux-policy-devel policycoreutils-python-utils
elif type yum 2>/dev/null
then
  yum install -y policycoreutils-python checkpolicy selinux-policy-devel policycoreutils-python-utils
fi

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SELinux/ulyaoth-nginx-mainline.txt"
su ulyaoth -c "audit2allow -M ulyaoth-nginx-mainline < ulyaoth-nginx-mainline.txt"
su ulyaoth -c "mv ulyaoth-nginx-mainline.pp /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SPECS/ulyaoth-nginx-mainline-selinux.spec"
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-selinux.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-mainline-selinux.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-mainline-selinux.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-mainline-selinux.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /home/ulyaoth/ulyaoth-*
rm -rf /root/build-ulyaoth-nginx-pagespeed-selinux.sh