ulyaothos=`cat /etc/ulyaoth`

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-geoipupdate/SPECS/ulyaoth-geoipupdate.spec"

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-geoipupdate.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-geoipupdate.spec
fi

su ulyaoth -c "spectool ulyaoth-geoipupdate.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-geoipupdate.spec"

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