%define debug_package %{nil}
%define spotifyrepo https://repository-origin.spotify.com/pool/non-free/s/spotify-client/
%define spotify_home /opt/spotify
%define spotify_group spotify
%define spotify_user spotify

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
Requires: ulyaoth-openssl1.1.0
Requires: zenity
Requires: curl
Requires: qt-x11
Requires: hicolor-icon-theme
Requires: libXScrnSaver
Requires: GConf2
Requires: alsa-lib
Requires: glibc
Requires: libstdc++
Requires: usbutils
Requires: xdg-utils
Requires: gtk2
Requires: nss
Requires: nspr
Requires: glib2
Requires: libpng
Requires: dbus-x11
Requires: libgudev1
%else
Requires: systemd
Requires: zenity
Requires: curl
Requires: qt-x11
Requires: hicolor-icon-theme
Requires: openssl
Requires: libXScrnSaver
Requires: GConf2
Requires: alsa-lib
Requires: glibc
Requires: libstdc++
Requires: usbutils
Requires: xdg-utils
Requires: gtk2
Requires: nss
Requires: nspr
Requires: glib2
Requires: libpng
Requires: dbus-x11
Requires: libgudev1
%endif

# end of distribution specific definitions

Summary: Spotify music player.
Name: spotify-client
Version: 1.0.79
Release: 1%{?dist}
URL: https://www.spotify.com
Packager: Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
License: https://www.spotify.com/legal/end-user-agreement
Group: Applications/Multimedia
Vendor: Spotify Ltd
BuildArch: x86_64
AutoReqProv: no

Source0:        https://repository-origin.spotify.com/pool/non-free/s/spotify-client/spotify-client_1.0.79.223.g92622cc2-21_amd64.deb
Source2:        spotify-wrapper
Source3:        spotify.xml
Source4:        spotify.appdata.xml

BuildRoot:  %{_tmppath}/spotify-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: desktop-file-utils
BuildRequires: chrpath
BuildRequires: libappstream-glib
BuildRequires: systemd

Provides: spotify
Provides: spotify-client
Provides: ulyaoth-spotify
Provides: ulyaoth-spotify-client

%description
Spotify is a commercial music streaming service providing digital rights management–restricted[4] content from record labels including Sony, EMI, Warner Music Group and Universal.[5][6] Music can be browsed or searched by artist, album, genre, playlist, or record label. Paid "Premium" subscriptions remove advertisements and allow users to download music to listen to offline.[7] On computers, a link allows users to purchase selected material via partner retailers.

%prep
%setup -q -c -T

ar x %{SOURCE0}
tar -xzf data.tar.gz

chrpath -d \
    .%{_datadir}/spotify/libwidevinecdmadapter.so \
    .%{_datadir}/spotify/spotify

%build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}

# Program resources - 512x512 icon along main executable is needed by the client
cp -frp \
    .%{_datadir}/spotify/*.{pak,dat,bin} \
    .%{_datadir}/spotify/{Apps,locales} \
    %{buildroot}%{_libdir}/%{name}
install -p -D -m 644 .%{_datadir}/spotify/icons/spotify-linux-512.png \
    %{buildroot}%{_libdir}/%{name}/icons/spotify-linux-512.png
	
# Binaries
install -p -m 755 \
    .%{_datadir}/spotify/*.so \
    .%{_datadir}/spotify/spotify \
    %{buildroot}%{_libdir}/%{name}/

# Wrapper script
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE2} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' \
    > %{buildroot}%{_bindir}/spotify
chmod +x %{buildroot}%{_bindir}/spotify

# Desktop file
install -m 0644 -D -p .%{_datadir}/spotify/spotify.desktop \
    %{buildroot}%{_datadir}/applications/spotify.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/spotify.desktop

# Icons
for size in 16 22 24 32 48 64 128 256 512; do
    install -p -D -m 644 .%{_datadir}/spotify/icons/spotify-linux-${size}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

# Firewalld rules
install -D -m 644 -p %{SOURCE3} \
    %{buildroot}%{_prefix}/lib/firewalld/services/spotify.xml

%if 0%{?fedora}
# Install AppData
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/appdata/
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/spotify.appdata.xml
%endif

desktop-file-validate %{buildroot}%{_datadir}/applications/spotify.desktop

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%{_bindir}/spotify
%{_datadir}/applications/spotify.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%if 0%{?fedora}
%{_datadir}/appdata/spotify.appdata.xml
%endif
%{_libdir}/%{name}
%{_prefix}/lib/firewalld/services/spotify.xml

%preun
ldconfig
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :

%post
%if 0%{?rhel} == 7
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%endif
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
%firewalld_reload

%postun
%if 0%{?rhel} == 7
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%endif
%if 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

ldconfig
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :

# print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using Spotify!

Please find the official documentation for Spotify here:
* https://www.spotify.com/

----------------------------------------------------------------------
BANNER

%posttrans
%if 0%{?rhel} == 7
%{_bindir}/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
%endif
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Sat May 19 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.0.79-1
- Update Spotify to version 1.0.79.
- Due to not having updated this long, our spec file is fully based on https://negativo17.org/repos/spotify/fedora-28/SRPMS/
- Please give the guys at Negativo17.org a big thanks.

* Wed Nov 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.17.8-1
- Update Spotify to version 0.9.17.8.

* Mon Apr 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.9.17.1-1
- Update Spotify version.

* Thu Mar 19 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.9.11.27-3
- Support for Fedora 22.
- Support for Oracle Linux 6 & 7.
- Support for CentOS 6 & 7.

* Sun Mar 1 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.9.11.27-2
- Adding systemd and initd files.
- multiple fixes.

* Sat Oct 4 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.9.11.27-1
- Creating new clean spec file.
- Support for Fedora 19, 20 and 21.
- Support for RHEL 6 and 7.