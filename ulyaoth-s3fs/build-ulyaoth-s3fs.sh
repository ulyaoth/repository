buildarch="$(uname -m)"
ulyaothrepo=1.1.0-1

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-s3fs/SPECS/ulyaoth-s3fs.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-s3fs.spec
fi

if [ "$os" == "fedora" ]
then
if type dnf 2>/dev/null
then
  dnf install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.fedora.noarch.rpm -y
elif type yum 2>/dev/null
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.fedora.noarch.rpm -y
fi
elif [ "$os" == "redhat" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.redhat.noarch.rpm -y
elif [ "$os" == "amazonlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.amazonlinux.noarch.rpm -y
elif [ "$os" == "centos" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.centos.noarch.rpm -y
elif [ "$os" == "oraclelinux" ]
then 
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.oraclelinux.noarch.rpm -y
elif [ "$os" == "scientificlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-$ulyaothrepo.scientificlinux.noarch.rpm -y
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-s3fs.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-s3fs.spec
fi

su ulyaoth -c "spectool ulyaoth-s3fs.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-s3fs.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-s3fs.sh
rm -rf /home/ulyaoth/rpmbuild