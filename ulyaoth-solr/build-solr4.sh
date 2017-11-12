# This script is supposed to run as the user "ulyaoth".

# Set variables.
version=4.10.4

# Create build environment.
rpmdev-setuptree

# Downloads solr 4 package and prepare for rpm build.
wget https://archive.apache.org/dist/lucene/solr/$version/solr-$version.tgz
tar xvf solr-$version.tgz
rm -rf /home/ulyaoth/solr-$version/bin/solr.in.sh
tar cvf solr-$version.tar.gz solr-$version/
mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SPECS/ulyaoth-solr4.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr4.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr4.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr4.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr4.spec
fi

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-solr4.spec


