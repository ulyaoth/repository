buildarch="$(uname -m)"

if grep -q -i "rhel" /etc/ulyaoth
then
  wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/SOURCES/ulyaoth-rhel.repo -O /etc/yum.repos.d/ulyaoth.repo
elif grep -q -i "CentOS" /etc/ulyaoth
then
  wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/SOURCES/ulyaoth-centos.repo -O /etc/yum.repos.d/ulyaoth.repo
elif grep -q -i "Fedora" /etc/ulyaoth
then
  wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/SOURCES/ulyaoth-fedora.repo -O /etc/yum.repos.d/ulyaoth.repo
elif grep -q -i "OracleLinux" /etc/ulyaoth
then
  wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/SOURCES/ulyaoth-oraclelinux.repo -O /etc/yum.repos.d/ulyaoth.repo
elif grep -q -i "scientific" /etc/ulyaoth
then
  wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/SOURCES/ulyaoth-scientific.repo -O /etc/yum.repos.d/ulyaoth.repo
else
  echo "A unsupported OS was detected!"
fi

sed -i "s/gpgcheck=1/gpgcheck=0/" /etc/yum.repos.d/ulyaoth.repo

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-monkey/SPECS/ulyaoth-monkey.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-monkey.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-monkey.spec
else
yum-builddep -y ulyaoth-monkey.spec
fi

su ulyaoth -c "spectool ulyaoth-monkey.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-monkey.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-monkey.sh
rm -rf /home/ulyaoth/rpmbuild