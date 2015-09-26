arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf install -y policycoreutils-python checkpolicy selinux-policy-devel
else
yum install -y policycoreutils-python checkpolicy selinux-policy-devel
fi

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/SELinux/ulyaoth-nginx-pagespeed.txt"
su ulyaoth -c "audit2allow -M ulyaoth-nginx-pagespeed < ulyaoth-nginx-pagespeed.txt"
su ulyaoth -c "mv ulyaoth-nginx-pagespeed.pp /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/SPECS/ulyaoth-nginx-pagespeed-selinux.spec"
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-pagespeed-selinux.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-pagespeed-selinux.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-pagespeed-selinux.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-pagespeed-selinux.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /home/ulyaoth/ulyaoth-*
rm -rf /root/build-ulyaoth-nginx-pagespeed-selinux.sh