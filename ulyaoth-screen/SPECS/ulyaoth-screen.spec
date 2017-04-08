#
%bcond_with multiuser
%define debug_package %{nil}
%define osbuildversion %(cat /etc/ulyaoth)

Summary:    Screen is a full-screen window manager that multiplexes a physical terminal between several processes, typically interactive shells.
Name:       ulyaoth-screen
Version:    4.5.1
Release:    1%{?dist}
BuildArch: x86_64
License: GPLv2+
Group:      Applications/System
URL:        https://www.gnu.org/software/screen/
Vendor:     gnu
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    ftp://ftp.gnu.org/gnu/screen/screen-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-screen/SOURCES/screen.pam
BuildRoot:  %{_tmppath}/screen-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: libutempter-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: texinfo

Provides: screen
Provides: ulyaoth-screen

%description
Screen is a full-screen window manager that multiplexes a physical terminal between several processes, typically interactive shells.
Each virtual terminal provides the functions of the DEC VT100 terminal and, in addition, several control functions from the ANSI X3.64 (ISO 6429) and ISO 2022 standards (e.g., insert/delete line and support for multiple character sets).
There is a scrollback history buffer for each virtual terminal and a copy-and-paste mechanism that allows the user to move text regions between windows.
When screen is called, it creates a single window with a shell in it (or the specified command) and then gets out of your way so that you can use the program as you normally would.
Then, at any time, you can create new (full-screen) windows with other programs in them (including more shells), kill the current window, view a list of the active windows, turn output logging on and off, copy text between windows, view the scrollback history, switch between windows, etc.
All windows run their programs completely independent of each other.
Programs continue to run when their window is currently not visible and even when the whole screen session is detached from the users terminal.

%prep
%setup -q -n screen-%{version}

%build
./autogen.sh

%configure \
	--enable-pam \
	--enable-colors256 \
	--enable-rxvt_osc \
	--enable-use-locale \
	--enable-telnet \
	--with-pty-mode=0620 \
	--with-pty-group=$(getent group tty | cut -d : -f 3) \
	--with-sys-screenrc="%{_sysconfdir}/screenrc" \
	--with-socket-dir="%{_localstatedir}/run/screen"

# braille support. (as shown in F24 spec file)
sed -i -e 's/.*#.*undef.*HAVE_BRAILLE.*/#define HAVE_BRAILLE 1/;' config.h

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/licenses/screen
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/screen

install -m 0644 etc/etcscreenrc $RPM_BUILD_ROOT%{_sysconfdir}/screenrc
cat etc/screenrc >> $RPM_BUILD_ROOT%{_sysconfdir}/screenrc

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/screen

%{__rm} -rf $RPM_BUILD_ROOT%{_infodir}/dir

%{__mv} %{_builddir}/screen-%{version}/COPYING $RPM_BUILD_ROOT/usr/share/licenses/screen/

%if 0%{?rhel}  == 6
%else
%{__mkdir} -p $RPM_BUILD_ROOT%{_tmpfilesdir}
cat <<EOF > $RPM_BUILD_ROOT%{_tmpfilesdir}/screen.conf
# screen needs directory in /var/run
%if %{with multiuser}
d %{_localstatedir}/run/screen 0755 root root
%else
d %{_localstatedir}/run/screen 0775 root screen
%endif
EOF
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g 84 -r -f screen
:

%files
%defattr(-,root,root)
/usr/bin/screen
%{_mandir}/man1/screen.1.gz
%dir /usr/share/licenses/screen
%dir /usr/share/screen
/usr/share/screen/utf8encodings/01
/usr/share/screen/utf8encodings/02
/usr/share/screen/utf8encodings/03
/usr/share/screen/utf8encodings/04
/usr/share/screen/utf8encodings/18
/usr/share/screen/utf8encodings/19
/usr/share/screen/utf8encodings/a1
/usr/share/screen/utf8encodings/bf
/usr/share/screen/utf8encodings/c2
/usr/share/screen/utf8encodings/c3
/usr/share/screen/utf8encodings/c4
/usr/share/screen/utf8encodings/c6
/usr/share/screen/utf8encodings/c7
/usr/share/screen/utf8encodings/c8
/usr/share/screen/utf8encodings/cc
/usr/share/screen/utf8encodings/cd
/usr/share/screen/utf8encodings/d6
%config(noreplace) %{_sysconfdir}/screenrc
%config(noreplace) %{_sysconfdir}/pam.d/screen

%if %{with multiuser}
%attr(4755,root,root) %{_bindir}/screen-%{version}
%attr(755,root,root) %{_localstatedir}/run/screen
%else
%attr(2755,root,screen) %{_bindir}/screen-%{version}
%attr(775,root,screen) %{_localstatedir}/run/screen
%endif

%if 0%{?rhel}  == 6
%doc /usr/share/licenses/screen/COPYING
%else
%if "%{osbuildversion}" == "amazonlinux"
%license /usr/share/licenses/screen/COPYING
%else
%license /usr/share/licenses/screen/COPYING
%{_tmpfilesdir}/screen.conf
%endif
%endif

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-screen!

Please find the official documentation for screen here:
* https://www.gnu.org/software/screen/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 4.5.1-1
- Updated to Screen 4.5.1.

* Thu Feb 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 4.5.0-1
- Updated to Screen 4.5.0.

* Mon Jun 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 4.4.0-1
- Initial release based on Fedora spec file.