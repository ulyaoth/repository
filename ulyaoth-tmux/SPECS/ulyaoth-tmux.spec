#
%define debug_package %{nil}

Summary:    tmux is a "terminal multiplexer"
Name:       ulyaoth-tmux
Version:    2.8
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD
Group:      System Environment/Shells
URL:        https://github.com/tmux/tmux
Vendor:     tmux
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    https://github.com/tmux/tmux/releases/download/%{version}/tmux-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tmux-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ncurses-devel

%if 0%{?rhel}  == 6
BuildRequires: libevent2-devel
%else
BuildRequires: libevent-devel
%endif

Provides: tmux
Provides: ulyaoth-tmux

%description
tmux is a "terminal multiplexer", it enables a number of terminals (or windows) to be accessed and controlled from a single terminal. 
tmux is intended to be a simple, modern, BSD-licensed alternative to programs such as GNU screen.

%prep
%setup -q -n tmux-%{version}

%build
./configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__rm} -rf $RPM_BUILD_ROOT/lib

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
/usr/bin/tmux
%doc /usr/share/man/man1/tmux.1.gz

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tmux!

Please find the official documentation for tmux here:
* https://github.com/tmux/tmux

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 2.8-1
- Updated tmux to 2.8.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.7-1
- Updated tmux to 2.7.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.6-1
- Updated tmux to 2.6.

* Tue May 30 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.5-1
- Updated tmux to 2.5.

* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.4-1
- Updated tmux to 2.4.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.3-1
- Updated tmux to 2.3.

* Sun Jun 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2-1
- Initial release.