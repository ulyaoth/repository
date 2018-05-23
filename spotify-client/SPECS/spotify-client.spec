%define debug_package %{nil}
%global __strip /bin/true

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

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
Requires: libatomic

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
Source0: spotify-client.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SOURCES/spotify-wrapper
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SOURCES/spotify.xml
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SOURCES/spotify.appdata.xml
BuildRoot:  %{_tmppath}/spotify-client-%{version}-%{release}-root-%(%{__id_u} -n)

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

%setup -q

%build

%install

tar xvf %{SOURCE0} -C $RPM_BUILD_ROOT

# firewalld rules
install -D -m 644 -p %{SOURCE2} \
    %{buildroot}%{_prefix}/lib/firewalld/services/spotify.xml

appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/spotify.appdata.xml

desktop-file-validate %{buildroot}%{_datadir}/applications/spotify.desktop	

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%{_bindir}/spotify
%{_datadir}/applications/spotify.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/spotify.appdata.xml
/usr/share/spotify
%{_prefix}/lib/firewalld/services/spotify.xml
/usr/share/doc/spotify-client/changelog.gz

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
* Tue May 22 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.0.79-1
- Update Spotify to version 1.0.79.
- partly based on spec file from negativo17.org.

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