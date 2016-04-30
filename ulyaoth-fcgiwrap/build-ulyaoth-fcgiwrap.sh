ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"
fcgiwrapversion=1.1.0

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/gnosek/fcgiwrap/archive/'"$fcgiwrapversion"'.tar.gz"
su ulyaoth -c "tar xvzf '"$fcgiwrapversion"'.tar.gz"
su ulyaoth -c "mv /home/ulyaoth/fcgiwrap-'"$fcgiwrapversion"' /home/ulyaoth/fcgiwrap"
su ulyaoth -c "sed -i 's/http/fcgiwrap/g' /home/ulyaoth/fcgiwrap/systemd/fcgiwrap.service"
su ulyaoth -c "tar cvf fcgiwrap.tar.gz fcgiwrap"
su ulyaoth -c "mv fcgiwrap.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf /home/ulyaoth/fcgiwrap/ '"$fcgiwrapversion"'.tar.gz"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fcgiwrap/SPEC/ulyaoth-fcgiwrap.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-fcgiwrap.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-fcgiwrap.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-fcgiwrap.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-fcgiwrap.spec"

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
