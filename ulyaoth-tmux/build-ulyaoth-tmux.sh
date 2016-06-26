ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"
arch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tmux/SPECS/ulyaoth-tmux.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tmux.spec
fi

if [ "$ulyaothos" == "scientificlinux" ]
then
if grep -q -i "release 6" /etc/redhat-release
then
if [ "$arch" != "x86_64" ]
then
yum install http://mirror.centos.org/centos/6/os/i386/Packages/libevent2-2.0.21-2.el6.i686.rpm http://mirror.centos.org/centos/6/os/i386/Packages/libevent2-devel-2.0.21-2.el6.i686.rpm -y
else
yum install http://mirror.centos.org/centos/6/os/x86_64/Packages/libevent2-2.0.21-2.el6.x86_64.rpm http://mirror.centos.org/centos/6/os/x86_64/Packages/libevent2-devel-2.0.21-2.el6.x86_64.rpm -y
fi
fi
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-tmux.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-tmux.spec
fi

su ulyaoth -c "spectool ulyaoth-tmux.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-tmux.spec"

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