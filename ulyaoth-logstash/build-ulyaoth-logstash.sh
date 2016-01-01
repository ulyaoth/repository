buildarch="$(uname -m)"
version=2.1.1

if type dnf 2>/dev/null
then
  dnf install java-1.8.0-openjdk-devel rubygem-rake-compiler
elif type yum 2>/dev/null
then
  yum install java-1.8.0-openjdk-devel rubygem-rake-compiler
fi

useradd ulyaoth
cd /home/ulyaoth

su ulyaoth -c "rpmdev-setuptree"

su ulyaoth -c "wget https://github.com/elastic/logstash/archive/v$version.tar.gz"
su ulyaoth -c "tar xvzf v$version.tar.gz"
su ulyaoth -c "cd logstash-$version && rake artifact:tar"
su ulyaoth -c "cp /home/ulyaoth/logstash-$version/build/logstash-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/SPECS/ulyaoth-logstash.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-logstash.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-logstash.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-logstash.spec
fi

su ulyaoth -c "spectool ulyaoth-logstash.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-logstash.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/logstash-$version v$version.tar.gz
rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-logstash.sh