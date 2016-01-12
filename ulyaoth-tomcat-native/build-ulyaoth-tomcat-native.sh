buildarch="$(uname -m)"

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/SPECS/ulyaoth-tomcat-native.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat-native.spec
fi

if type dnf 2>/dev/null
then
  dnf install -y java-1.8.0-openjdk-devel
  dnf builddep -y ulyaoth-tomcat-native.spec
elif type yum 2>/dev/null
then
  yum install -y java-1.8.0-openjdk-devel
  yum-builddep -y ulyaoth-tomcat-native.spec
fi


su ulyaoth -c "spectool ulyaoth-tomcat-native.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat-native.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-tomcat-native.sh