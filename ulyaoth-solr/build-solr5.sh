# Set variables.
version=5.5.5

# create build environment.
rpmdev-setuptree

# Download the spec files
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5-examples.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-examples.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr5-docs.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-docs.spec

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

# Install the solr requirements for building the rpm.
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec
fi

# Download additional from spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec -g -R

# Build Solr 5 rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5.spec

# Clean
rm -rf /home/ulyaoth/rpmbuild/BUILD
rm -rf /home/ulyaoth/rpmbuild/SOURCES
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
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-examples.spec

# Clean
rm -rf /home/ulyaoth/rpmbuild/BUILD
rm -rf /home/ulyaoth/rpmbuild/SOURCES
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
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr5-docs.spec

# Copy the file to Ulyaoth home folder.
cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/