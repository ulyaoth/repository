Summary:    Screen is a full-screen window manager that multiplexes a physical terminal between several processes, typically interactive shells.
Name:       ulyaoth-screen
Version:    4.4.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GPLv2+
Group:      Applications/System
URL:        https://www.gnu.org/software/screen/
Vendor:     gnu
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    ftp://ftp.gnu.org/gnu/screen/screen-%{version}.tar.gz
Source1:	screen.pam
BuildRoot:  %{_tmppath}/screen-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: libutempter-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: textino

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
%setup -q -n %{name}-%{version}

%build
./autogen.sh

%configure \
	--enable-pam \
	--enable-colors256 \
	--enable-rxvt_osc \
	--enable-use-locale \
	--enable-telnet \
	--with-sys-screenrc="%{_sysconfdir}/screenrc" \
	--with-socket-dir="%{_localstatedir}/run/screen"

# braille support. (as shown in F24 spec file)
sed -i -e 's/.*#.*undef.*HAVE_BRAILLE.*/#define HAVE_BRAILLE 1/;' config.h

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-screen!

Please find the official documentation for screen here:
* https://www.gnu.org/software/screen/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Mon Jun 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 4.4.0-1
- Initial release.