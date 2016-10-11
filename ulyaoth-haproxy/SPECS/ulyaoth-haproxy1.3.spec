AutoReqProv: no
%define debug_package %{nil}

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
BuildRequires: systemd-devel
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
%endif

# end of distribution specific definitions

Summary:    The Reliable, High Performance TCP/HTTP Load Balancer
Name:       ulyaoth-haproxy1.3
Version:    1.3.28
Release:    1%{?dist}
BuildArch: x86_64
License:    GPL/LGPL
Group:      System Environment/Daemons
URL:        https://www.haproxy.org/
Vendor:     HAProxy
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://www.haproxy.org/download/1.3/src/haproxy-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.3.cfg
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.3.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.3.service
BuildRoot:  %{_tmppath}/haproxy-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: zlib-devel
BuildRequires: pcre-devel

Requires: pcre
Requires: zlib

Provides: haproxy1.3
Provides: ulyaoth-haproxy1.3

%description
HAProxy is a free, very fast and reliable solution offering high availability, load balancing, and proxying for TCP and HTTP-based applications. It is particularly suited for very high traffic web sites and powers quite a number of the world's most visited ones. Over the years it has become the de-facto standard opensource load balancer, is now shipped with most mainstream Linux distributions, and is often deployed by default in cloud platforms. Since it does not advertise itself, we only know it's used when the admins report it :-)

%prep
%setup -q -n haproxy-%{version}

%build

make PREFIX=/usr/local/ulyaoth/haproxy/haproxy1.3 TARGET=linux26 USE_LINUX_TPROXY=1 USE_PCRE=1

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/haproxy1.3
mkdir -p $RPM_BUILD_ROOT/usr/sbin

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr/local/ulyaoth/haproxy/haproxy1.3 install

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/haproxy1.3/share/man $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/haproxy1.3/
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/haproxy1.3/share

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/haproxy
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/haproxy/haproxy1.3.cfg

ln -s /usr/local/ulyaoth/haproxy/haproxy1.3/sbin/haproxy $RPM_BUILD_ROOT/usr/sbin/haproxy1.3
	
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/haproxy1.3.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE2 \
    $RPM_BUILD_ROOT%{_initrddir}/haproxy1.3
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/sbin/haproxy1.3

%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/haproxy
%dir /usr/local/ulyaoth/haproxy/haproxy1.3

%dir %{_sysconfdir}/haproxy
%config(noreplace) %{_sysconfdir}/haproxy/haproxy1.3.cfg

%dir /usr/local/ulyaoth/haproxy/haproxy1.3/sbin
/usr/local/ulyaoth/haproxy/haproxy1.3/sbin/haproxy

%dir  /usr/local/ulyaoth/haproxy/haproxy1.3/man
%dir  /usr/local/ulyaoth/haproxy/haproxy1.3/man/man1
/usr/local/ulyaoth/haproxy/haproxy1.3/man/man1/haproxy.1

%dir /usr/local/ulyaoth/haproxy/haproxy1.3/doc
%dir /usr/local/ulyaoth/haproxy/haproxy1.3/doc/haproxy/
/usr/local/ulyaoth/haproxy/haproxy1.3/doc/haproxy/architecture.txt
/usr/local/ulyaoth/haproxy/haproxy1.3/doc/haproxy/configuration.txt
/usr/local/ulyaoth/haproxy/haproxy1.3/doc/haproxy/haproxy-en.txt
/usr/local/ulyaoth/haproxy/haproxy1.3/doc/haproxy/haproxy-fr.txt

%if %{use_systemd}
%{_unitdir}/haproxy1.3.service
%else
%{_initrddir}/haproxy1.3
%endif

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-haproxy1.3!

Please find the official documentation for HAProxy here:
* https://www.haproxy.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun -p /sbin/ldconfig

%changelog
* Tue Oct 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.28-1
- Initial release for HAProxy 1.3.