buildarch="$(uname -m)"
bananaversion=1.6.0

useradd ulyaoth
cd /home/ulyaoth

su ulyaoth -c "rpmdev-setuptree"

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-banana/SPECS/ulyaoth-banana.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-banana.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-banana.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-banana.spec
fi

su ulyaoth -c "spectool ulyaoth-banana.spec -g -R"

cd /home/ulyaoth
su ulyaoth -c "wget https://github.com/LucidWorks/banana/archive/v'"$bananaversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$bananaversion"'.tar.gz"
su ulyaoth -c "mkdir -p /home/ulyaoth/banana-'"$bananaversion"'/build"
cd /home/ulyaoth/banana-$bananaversion
su ulyaoth -c "ant"
mv /home/ulyaoth/banana-$bananaversion/build/banana-0.war /home/ulyaoth/rpmbuild/SOURCES/banana.war
cd /home/ulyaoth/rpmbuild/SPECS/

su ulyaoth -c "rpmbuild -bb ulyaoth-banana.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/

rm -rf /home/ulyaoth/banana-$bananaversion
rm -rf /home/ulyaoth/rpmbuild
