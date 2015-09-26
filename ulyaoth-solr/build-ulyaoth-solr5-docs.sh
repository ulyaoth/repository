buildarch="$(uname -m)"
version=5.3.0

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"

su ulyaoth -c "wget http://apache.mirrors.spacedump.net/lucene/solr/5.3.0/solr-5.3.0.tgz"
su ulyaoth -c "tar xvf solr-$version.tgz"
su ulyaoth -c "mv solr-$version solr"
su ulyaoth -c "mkdir -p /home/ulyaoth/solr-$version"
mv /home/ulyaoth/solr/docs /home/ulyaoth/solr-$version/
su ulyaoth -c "tar cvf solr-$version.tar.gz solr-$version/"
su ulyaoth -c "mv solr-$version.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-solr/SPECS/ulyaoth-solr5-docs.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-solr5-docs.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-solr5-docs.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/