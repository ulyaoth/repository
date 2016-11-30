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
Name:       ulyaoth-haproxy1.7
Version:    1.7.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GPL/LGPL
Group:      System Environment/Daemons
URL:        https://www.haproxy.org/
Vendor:     HAProxy
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://www.haproxy.org/download/1.7/src/haproxy-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.7.cfg
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.7.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SOURCES/haproxy1.7.service
BuildRoot:  %{_tmppath}/haproxy-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: ulyaoth-openssl1.1.0
BuildRequires: ulyaoth-lua5.3

Requires: ulyaoth-openssl1.1.0
Requires: ulyaoth-lua5.3
Requires: pcre
Requires: zlib

Provides: haproxy1.7
Provides: ulyaoth-haproxy1.7

%description
HAProxy is a free, very fast and reliable solution offering high availability, load balancing, and proxying for TCP and HTTP-based applications. It is particularly suited for very high traffic web sites and powers quite a number of the world's most visited ones. Over the years it has become the de-facto standard opensource load balancer, is now shipped with most mainstream Linux distributions, and is often deployed by default in cloud platforms. Since it does not advertise itself, we only know it's used when the admins report it :-)

%prep
%setup -q -n haproxy-%{version}

%build

make PREFIX=/usr/local/ulyaoth/haproxy/1.7 TARGET=linux2628 USE_GETADDRINFO=1 USE_LINUX_TPROXY=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1 LUA_LIB=/usr/local/ulyaoth/lua/5.3/lib/ LUA_INC=/usr/local/ulyaoth/lua/5.3/include/ USE_OPENSSL=1 SSL_INC=/usr/local/ulyaoth/ssl/openssl1.1.0/include SSL_LIB=/usr/local/ulyaoth/ssl/openssl1.1.0/lib ADDLIB=-ldl

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/1.7
mkdir -p $RPM_BUILD_ROOT/usr/sbin

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr/local/ulyaoth/haproxy/1.7 install

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/1.7/share/man $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/1.7/
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/haproxy/1.7/share

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/haproxy1.7
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/haproxy1.7/haproxy.cfg

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/haproxy1.7
	
ln -s /usr/local/ulyaoth/haproxy/haproxy1.7/sbin/haproxy $RPM_BUILD_ROOT/usr/sbin/haproxy1.7
	
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/haproxy1.7.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE2 \
    $RPM_BUILD_ROOT%{_initrddir}/haproxy1.7
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/sbin/haproxy1.7

%attr(0755,root,root) %dir %{_localstatedir}/log/haproxy1.7

%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/haproxy
%dir /usr/local/ulyaoth/haproxy/1.7

%dir %{_sysconfdir}/haproxy1.7
%config(noreplace) %{_sysconfdir}/haproxy1.7/haproxy.cfg

%dir /usr/local/ulyaoth/haproxy/1.7/sbin
/usr/local/ulyaoth/haproxy/1.7/sbin/haproxy

%dir  /usr/local/ulyaoth/haproxy/1.7/man
%dir  /usr/local/ulyaoth/haproxy/1.7/man/man1
/usr/local/ulyaoth/haproxy/1.7/man/man1/haproxy.1

%dir /usr/local/ulyaoth/haproxy/1.7/doc
%dir /usr/local/ulyaoth/haproxy/1.7/doc/haproxy/
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/architecture.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/close-options.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/configuration.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/cookie-options.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/intro.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/linux-syn-cookies.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/lua.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/management.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/network-namespaces.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/proxy-protocol.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/51Degrees-device-detection.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/DeviceAtlas-device-detection.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/SPOE.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/WURFL-device-detection.txt
/usr/local/ulyaoth/haproxy/1.7/doc/haproxy/netscaler-client-ip-insertion-protocol.txt


%if %{use_systemd}
%{_unitdir}/haproxy1.7.service
%else
%{_initrddir}/haproxy1.7
%endif

%post
/sbin/ldconfig
# Register the haproxy1.7 service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset haproxy1.7.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add haproxy1.7
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-haproxy1.7!

Please find the official documentation for HAProxy here:
* https://www.haproxy.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable haproxy1.7.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop haproxy1.7.service >/dev/null 2>&1 ||:
%else
    /sbin/service haproxy1.6 stop > /dev/null 2>&1
    /sbin/chkconfig --del haproxy1.7
%endif
fi

%postun
/sbin/ldconfig
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service haproxy1.7 status  >/dev/null 2>&1 || exit 0
    /sbin/service haproxy1.7 upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Wed Nov 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.0-1
- Initial release for HAProxy 1.7.