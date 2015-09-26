%define debug_package %{nil}
%define spotifyrepo http://repository.spotify.com/pool/non-free/s/spotify
%define spotify_home /opt/spotify
%define spotify_group spotify
%define spotify_user spotify

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary: Spotify music player.
Name: spotify-client
Version: 0.9.17.1
Release: 1%{?dist}
URL: https://www.spotify.com
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
License: Proprietary (non-free)
Group: Applications/Multimedia
Vendor: Spotify Ltd
BuildArch: x86_64
AutoReqProv: no
Source0: ulyaoth-spotify.tar.gz
Source1: spotify.service
Source2: spotify.init
BuildRoot:  %{_tmppath}/spotify-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils

Requires: zenity
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

Provides: spotify
Provides: spotify-client
Provides: ulyaoth-spotify
Provides: ulyaoth-spotify-client

%description
Spotify is a commercial music streaming service providing digital rights management–restricted[4] content from record labels including Sony, EMI, Warner Music Group and Universal.[5][6] Music can be browsed or searched by artist, album, genre, playlist, or record label. Paid "Premium" subscriptions remove advertisements and allow users to download music to listen to offline.[7] On computers, a link allows users to purchase selected material via partner retailers.

%setup -q

%build

%install

tar xvf %{SOURCE0} -C $RPM_BUILD_ROOT

%if 0%{?fedora} == 21
ln -s /usr/lib64/libgcrypt.so.11.8.2 ${RPM_BUILD_ROOT}/usr/lib64/libgcrypt.so.11
ln -s /usr/lib64/libudev.so.1 ${RPM_BUILD_ROOT}/usr/lib64/libudev.so.0
ln -s /usr/lib64/libudev.so.1 ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/Data/libudev.so.0
%endif

ln -sf /usr/lib64/libnspr4.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libnspr4.so.0d
ln -sf /usr/lib64/libnss3.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libnss3.so.1d
ln -sf /usr/lib64/libnssutil3.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libnssutil3.so.1d
ln -sf /usr/lib64/libplc4.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libplc4.so.0d
ln -sf /usr/lib64/libplds4.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libplds4.so.0d
ln -sf /usr/lib64/libssl3.so ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/libssl3.so.1d
chmod 0775 ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/Data/libffmpegsumo.so
chmod 0775 ${RPM_BUILD_ROOT}/opt/spotify/spotify-client/Data/libcef.so

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/spotify.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/spotify
%endif

desktop-file-validate %{buildroot}%{_datadir}/applications/spotify.desktop

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{spotify_group} >/dev/null || groupadd -r %{spotify_group}
getent passwd %{spotify_user} >/dev/null || /usr/sbin/useradd --comment "Spotify Daemon User" --shell /bin/bash -M -r -g %{spotify_group} --home %{spotify_home} %{spotify_user}

%files
%defattr(-,%{spotify_user},%{spotify_group})
%dir /opt/spotify
%{spotify_home}/*
%dir /opt/spotify/spotify-client
%dir /opt/spotify/spotify-client/Data
%dir /opt/spotify/spotify-client/Data/locales
%dir /opt/spotify/spotify-client/Icons
/opt/spotify/spotify-client/*
/opt/spotify/spotify-client/Data/*
/opt/spotify/spotify-client/Icons/*
/opt/spotify/spotify-client/Data/locales/*

%defattr(-,root,root)
%dir %{_defaultdocdir}/spotify-client-gnome-support
%dir %{_defaultdocdir}/spotify-client-qt
%dir %{_defaultdocdir}/spotify-client
%dir %{_datadir}/spotify
/usr/lib64/*
%{_defaultdocdir}/spotify-client-gnome-support/*
%{_defaultdocdir}/spotify-client-qt/*
%{_defaultdocdir}/spotify-client/*
%{_bindir}/*
%{_datadir}/applications/*
/usr/share/applications/spotify.desktop
/usr/share/icons/hicolor/16x16/apps/spotify-client.png
/usr/share/icons/hicolor/22x22/apps/spotify-client.png
/usr/share/icons/hicolor/24x24/apps/spotify-client.png
/usr/share/icons/hicolor/32x32/apps/spotify-client.png
/usr/share/icons/hicolor/48x48/apps/spotify-client.png
/usr/share/icons/hicolor/64x64/apps/spotify-client.png
/usr/share/icons/hicolor/128x128/apps/spotify-client.png
/usr/share/icons/hicolor/256x256/apps/spotify-client.png

%if %{use_systemd}
%{_unitdir}/spotify.service
%else
%{_initrddir}/spotify
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service spotify status  >/dev/null 2>&1 || exit 0
fi

ldconfig
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable spotify.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop spotify.service >/dev/null 2>&1 ||:
%else
    /sbin/service spotify stop > /dev/null 2>&1
    /sbin/chkconfig --del spotify
%endif
fi

ldconfig
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :

%post
# Register the spotify service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset spotify.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add spotify
%endif
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

%changelog
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