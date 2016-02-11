buildarch="$(uname -m)"

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9.spec"
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-admin.spec"
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-docs.spec"
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SPECS/ulyaoth-tomcat9-examples.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat9.spec
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat9-admin.spec
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat9-docs.spec
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat9-examples.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-tomcat9.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-tomcat9.spec
fi

su ulyaoth -c "spectool ulyaoth-tomcat9.spec -g -R"

su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat9.spec"
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat9-admin.spec"
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat9-docs.spec"
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat9-examples.spec"

cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-tomcat9.sh
