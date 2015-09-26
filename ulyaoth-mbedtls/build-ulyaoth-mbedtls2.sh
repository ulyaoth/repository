buildarch="$(uname -m)"

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-mbedtls/SPECS/ulyaoth-mbedtls2.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-mbedtls2.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-mbedtls2.spec
else
yum-builddep -y ulyaoth-mbedtls2.spec
fi

su ulyaoth -c "spectool ulyaoth-mbedtls2.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-mbedtls2.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-mbedtls2.sh
rm -rf /home/ulyaoth/rpmbuild