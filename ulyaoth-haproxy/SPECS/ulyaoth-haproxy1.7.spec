AutoReqProv: no
%define debug_package %{nil}
%define ulyaoth_openssl_version 1.1.0

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
Name:       ulyaoth-haproxy1.7
Version:    1.7.9
Release:    1%{?dist}
BuildArch: x86_64
License:    GPL/LGPL
Group:      System Environment/Daemons
URL:        https://www.haproxy.org/
Vendor:     HAProxy
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://www.haproxy.org/download/1.7/src/haproxy-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy.cfg
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy.service
BuildRoot:  %{_tmppath}/haproxy-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: zlib-devel
BuildRequires: pcre-devel
%if 0%{?fedora} >= 26
BuildRequires: openssl-devel
%else
BuildRequires: ulyaoth-openssl%{ulyaoth_openssl_version}-devel
%endif
BuildRequires: ulyaoth-lua5.3-devel
BuildRequires: ulyaoth-lua5.3-static

%if 0%{?fedora} >= 26
BuildRequires: openssl
%else
BuildRequires: ulyaoth-openssl%{ulyaoth_openssl_version}-libs
%endif 
Requires: pcre
Requires: zlib

Provides: haproxy
Provides: ulyaoth-haproxy
Provides: ulyaoth-haproxy1.7

Conflicts: ulyaoth-haproxy1.8
Conflicts: ulyaoth-haproxy1.6
Conflicts: ulyaoth-haproxy1.5
Conflicts: ulyaoth-haproxy1.4
Conflicts: ulyaoth-haproxy1.3

%description
HAProxy is a free, very fast and reliable solution offering high availability, load balancing, and proxying for TCP and HTTP-based applications. It is particularly suited for very high traffic web sites and powers quite a number of the world's most visited ones. Over the years it has become the de-facto standard opensource load balancer, is now shipped with most mainstream Linux distributions, and is often deployed by default in cloud platforms. Since it does not advertise itself, we only know it's used when the admins report it :-)

%prep
%setup -q -n haproxy-%{version}

%build

%if 0%{?fedora} >= 26
make PREFIX=/usr TARGET=linux2628 USE_GETADDRINFO=1 USE_LINUX_TPROXY=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1 LUA_LIB=/usr/local/ulyaoth/lua5.3/lib64 LUA_INC=/usr/local/ulyaoth/lua5.3/include USE_OPENSSL=1 ADDLIB=-ldl

%else
make PREFIX=/usr TARGET=linux2628 USE_GETADDRINFO=1 USE_LINUX_TPROXY=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1 LUA_LIB=/usr/local/ulyaoth/lua5.3/lib64 LUA_INC=/usr/local/ulyaoth/lua5.3/include USE_OPENSSL=1 SSL_INC=/usr/local/ulyaoth/openssl1.1.0/include SSL_LIB=/usr/local/ulyaoth/openssl1.1.0/lib ADDLIB=-ldl
%endif 

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%{__mkdir} -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/usr/doc $RPM_BUILD_ROOT/usr/share/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/haproxy
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/haproxy/haproxy.cfg

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/haproxy
	
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/haproxy.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE2 \
    $RPM_BUILD_ROOT%{_initrddir}/haproxy
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/sbin/haproxy

%attr(0755,root,root) %dir %{_localstatedir}/log/haproxy

%dir %{_sysconfdir}/haproxy
%config(noreplace) %{_sysconfdir}/haproxy/haproxy.cfg

%dir %{_docdir}/haproxy
%{_docdir}/haproxy/51Degrees-device-detection.txt
%{_docdir}/haproxy/DeviceAtlas-device-detection.txt
%{_docdir}/haproxy/SPOE.txt
%{_docdir}/haproxy/WURFL-device-detection.txt
%{_docdir}/haproxy/architecture.txt
%{_docdir}/haproxy/close-options.txt
%{_docdir}/haproxy/configuration.txt
%{_docdir}/haproxy/cookie-options.txt
%{_docdir}/haproxy/intro.txt
%{_docdir}/haproxy/linux-syn-cookies.txt
%{_docdir}/haproxy/lua.txt
%{_docdir}/haproxy/management.txt
%{_docdir}/haproxy/netscaler-client-ip-insertion-protocol.txt
%{_docdir}/haproxy/network-namespaces.txt
%{_docdir}/haproxy/proxy-protocol.txt

%{_mandir}/man1/haproxy.1.gz

%if %{use_systemd}
%{_unitdir}/haproxy.service
%else
%{_initrddir}/haproxy
%endif

%post
/sbin/ldconfig
# Register the haproxy service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset haproxy.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add haproxy
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-haproxy1.7!

Please find the official documentation for HAProxy here:
* https://www.haproxy.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable haproxy.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop haproxy.service >/dev/null 2>&1 ||:
%else
    /sbin/service haproxy stop > /dev/null 2>&1
    /sbin/chkconfig --del haproxy
%endif
fi

%postun
/sbin/ldconfig
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service haproxy status  >/dev/null 2>&1 || exit 0
    /sbin/service haproxy upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Thu Nov 30 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.7.9-1
- Updated to HAProxy 1.7.9.

* Wed Aug 9 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.7.8-1
- Updated to HAProxy 1.7.8.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.7.7-1
- Updated to HAProxy 1.7.7.

* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.5-1
- Updated to HAProxy 1.7.5.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.4-1
- Updated to HAProxy 1.7.4.

* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.3-1
- Updated to HAProxy 1.7.3.

* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.2-1
- Updated to HAProxy 1.7.2.
- Changed locations to be stock like.

* Wed Nov 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.0-1
- Initial release for HAProxy 1.7.