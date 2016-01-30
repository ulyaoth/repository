arch="$(uname -m)"
buildarch="$(uname -m)"

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"

cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-go/SPECS/ulyaoth-go.spec"

if [ "$arch" != "x86_64" ]
then
  sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-go.spec
  sed -i 's/amd64/386/g' ulyaoth-go.spec
fi

su ulyaoth -c "spectool ulyaoth-go.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-go.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-go.spec