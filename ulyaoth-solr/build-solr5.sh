# Set variables.
version=5.5.5

# create build environment.
rpmdev-setuptree

# Downloads solr 5 package and prepare for rpm build.
wget http://apache.mirrors.spacedump.net/lucene/solr/$version/solr-$version.tgz
tar xvf solr-$version.tgz
rm -rf /home/ulyaoth/solr-$version/example
rm -rf /home/ulyaoth/solr-$version/docs
rm -rf /home/ulyaoth/solr-$version/bin/init.d
rm -rf /home/ulyaoth/solr-$version/bin/install_solr_service.sh
rm -rf /home/ulyaoth/solr-$version/bin/solr.in.sh
rm -rf /home/ulyaoth/solr-$version/server/resources/log4j.properties
tar cvf solr-$version.tar.gz solr-$version/
mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec

# Install the solr requirements for building the rpm.
if type dnf 2>/dev/null
then
  dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec
elif type yum 2>/dev/null
then
  yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec
fi

# Download additional from spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec -g -R

# Build Solr 5 rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec

cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/solr
rm -rf /home/ulyaoth/solr-$version

# Downloads solr 5 package and prepare for examples.
rpmdev-setuptree
tar xvf solr-$version.tgz
mv solr-$version solr
mkdir -p /home/ulyaoth/solr-$version
mv /home/ulyaoth/solr/example /home/ulyaoth/solr-$version/
tar cvf solr-$version.tar.gz solr-$version/
mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/

# Build solr 5 examples rpm.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5-examples.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-examples.spec
rpmbuild -ba ulyaoth-solr5-examples.spec
cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/solr
rm -rf /home/ulyaoth/solr-$version

# Downloads solr 5 package and prepare for documentation.
rpmdev-setuptree
tar xvf solr-$version.tgz
mv solr-$version solr
mkdir -p /home/ulyaoth/solr-$version
mv /home/ulyaoth/solr/docs /home/ulyaoth/solr-$version/
tar cvf solr-$version.tar.gz solr-$version/
mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/

# Build Solr 5 Documentation rpm.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5-docs.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-docs.spec
rpmbuild -ba ulyaoth-solr5-docs.spec
cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/solr
rm -rf /home/ulyaoth/solr-$version