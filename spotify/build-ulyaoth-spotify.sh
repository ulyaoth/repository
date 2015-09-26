buildarch="$(uname -m)"

useradd ulyaoth

su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SOURCES/
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/spotify/SOURCES/spotify.init"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/spotify/SOURCES/spotify.service"

cd /home/ulyaoth
if grep -q -i "Fedora release 21" /etc/redhat-release
then
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/lib64/libgcrypt.so.11.8.2"
fi
if grep -q -i "Fedora release 22" /etc/redhat-release
then
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/lib64/libgcrypt.so.11.8.2"
fi
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/lib64/libcrypto.so.1.0.0"
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/lib64/libssl.so.1.0.0"
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/lib64/libudev.so.0.13.1"
su ulyaoth -c "wget https://trash.ulyaoth.net/spotify/spotify.desktop"
su ulyaoth -c "wget http://repository-origin.spotify.com/pool/non-free/s/spotify/spotify-client-gnome-support_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "wget http://repository-origin.spotify.com/pool/non-free/s/spotify/spotify-client-qt_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "wget http://repository-origin.spotify.com/pool/non-free/s/spotify/spotify-client_0.9.17.1.g9b85d43.7-1_amd64.deb"

su ulyaoth -c "ar x spotify-client-gnome-support_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "tar xvf data.tar.xz"
su ulyaoth -c "rm -rf control.tar.gz data.tar.xz debian-binary spotify-client-gnome-support_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "ar x spotify-client-qt_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "tar xvf data.tar.xz"
su ulyaoth -c "rm -rf control.tar.gz data.tar.xz debian-binary spotify-client-qt_0.9.17.1.g9b85d43.7-1_all.deb"
su ulyaoth -c "ar x spotify-client_0.9.17.1.g9b85d43.7-1_amd64.deb"
su ulyaoth -c "tar xvf data.tar.xz"
su ulyaoth -c "rm -rf control.tar.gz data.tar.xz debian-binary spotify-client_0.9.17.1.g9b85d43.7-1_amd64.deb"

su ulyaoth -c "mkdir -p /home/ulyaoth/usr/lib64/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/applications/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/16x16/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/22x22/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/24x24/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/32x32/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/48x48/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/64x64/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/128x128/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/256x256/apps/"

su ulyaoth -c "mv lib* /home/ulyaoth/usr/lib64/"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-16.png /home/ulyaoth/usr/share/icons/hicolor/16x16/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-22.png /home/ulyaoth/usr/share/icons/hicolor/22x22/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-24.png /home/ulyaoth/usr/share/icons/hicolor/24x24/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-32.png /home/ulyaoth/usr/share/icons/hicolor/32x32/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-48.png /home/ulyaoth/usr/share/icons/hicolor/48x48/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-64.png /home/ulyaoth/usr/share/icons/hicolor/64x64/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-128.png /home/ulyaoth/usr/share/icons/hicolor/128x128/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/opt/spotify/spotify-client/Icons/spotify-linux-256.png /home/ulyaoth/usr/share/icons/hicolor/256x256/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/spotify.desktop /home/ulyaoth/usr/share/applications/"

su ulyaoth -c "tar cvf ulyaoth-spotify.tar.gz ./opt/ ./usr/"
su ulyaoth -c "rm -rf opt/ usr/ spotify.desktop"
su ulyaoth -c "mv ulyaoth-spotify.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/spotify/SPECS/ulyaoth-spotify.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-spotify.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-spotify.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-spotify.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-spotify.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-spotify.sh