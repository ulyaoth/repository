buildarch="$(uname -m)"

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SPECS/ulyaoth-zookeeper3.4.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-zookeeper3.4.spec
fi


if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-zookeeper3.4.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-zookeeper3.4.spec
fi

su ulyaoth -c "spectool ulyaoth-zookeeper3.4.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-zookeeper3.4.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-zookeeper3.4.sh