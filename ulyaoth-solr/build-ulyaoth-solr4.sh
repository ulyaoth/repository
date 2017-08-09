ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"
version=4.10.4

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"

# Downloads solr 4 package and prepare for rpm build.
su ulyaoth -c "wget https://archive.apache.org/dist/lucene/solr/$version/solr-$version.tgz"
#su ulyaoth -c "wget https://repos.ulyaoth.net/random/solr-$version.tgz"
su ulyaoth -c "tar xvf solr-$version.tgz"
rm -rf /home/ulyaoth/solr-$version/bin/solr.in.sh
su ulyaoth -c "tar cvf solr-$version.tar.gz solr-$version/"
su ulyaoth -c "mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

# Download spec file.
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr4.spec"

# Check if we use 32 bit and if we do change spec file.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-solr4.spec
fi

# Install the solr requirements for building the rpm.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-solr4.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-solr4.spec
fi

# Build Solr 4 rpm.
su ulyaoth -c "spectool ulyaoth-solr4.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-solr4.spec"

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

# Clean all files.
rm -rf /home/ulyaoth/solr*
rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild