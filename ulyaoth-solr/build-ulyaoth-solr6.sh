ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"
version=6.0.0

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"

# Downloads solr 6 package and prepare for rpm build.
su ulyaoth -c "wget http://apache.mirrors.spacedump.net/lucene/solr/$version/solr-$version.tgz"
su ulyaoth -c "tar xvf solr-$version.tgz"
rm -rf /home/ulyaoth/solr-$version/example
rm -rf /home/ulyaoth/solr-$version/docs
rm -rf /home/ulyaoth/solr-$version/bin/init.d
rm -rf /home/ulyaoth/solr-$version/bin/install_solr_service.sh
rm -rf /home/ulyaoth/solr-$version/bin/solr.in.sh
rm -rf /home/ulyaoth/solr-$version/server/resources/log4j.properties
su ulyaoth -c "tar cvf solr-$version.tar.gz solr-$version/"
su ulyaoth -c "mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

# Download spec file.
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr6.spec"

# Check if we use 32 bit and if we do change spec file.
if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-solr6.spec
fi

# Install the solr requirements for building the rpm.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-solr6.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-solr6.spec
fi

# Build Solr 6 rpm.
su ulyaoth -c "spectool ulyaoth-solr6.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-solr6.spec"
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
cd /root
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/solr-$version

# Downloads solr 6 package and prepare for examples.
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "tar xvf solr-$version.tgz"
su ulyaoth -c "mv solr-$version solr"
su ulyaoth -c "mkdir -p /home/ulyaoth/solr-$version"
mv /home/ulyaoth/solr/example /home/ulyaoth/solr-$version/
su ulyaoth -c "tar cvf solr-$version.tar.gz solr-$version/"
su ulyaoth -c "mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

# Build solr 6 examples rpm.
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr6-examples.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-solr6-examples.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-solr6-examples.spec"
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
cd /root
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/solr
rm -rf /home/ulyaoth/solr-$version

# Downloads solr 6 package and prepare for documentation.
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "tar xvf solr-$version.tgz"
su ulyaoth -c "mv solr-$version solr"
su ulyaoth -c "mkdir -p /home/ulyaoth/solr-$version"
mv /home/ulyaoth/solr/docs /home/ulyaoth/solr-$version/
su ulyaoth -c "tar cvf solr-$version.tar.gz solr-$version/"
su ulyaoth -c "mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

# Build Solr 6 Documentation rpm.
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr6-docs.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-solr6-docs.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-solr6-docs.spec"

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

# Clean all files.
rm -rf /home/ulyaoth/solr*
rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild