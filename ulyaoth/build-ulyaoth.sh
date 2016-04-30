ulyaothos=`cat /etc/ulyaoth`

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/

su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SPECS/ulyaoth.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec"
sed -i "s/sbagmeijer/$ulyaothos/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

su ulyaoth -c "spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec -g -R"
su ulyaoth -c "rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild