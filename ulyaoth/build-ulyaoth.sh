ulyaothos=`cat /etc/ulyaoth`

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/

su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SPECS/ulyaoth.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec"
sed -i "s/sbagmeijer/$ulyaothos/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

su ulyaoth -c "spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec -g -R"
su ulyaoth -c "rpmbuild -bb /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec"

cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /root/