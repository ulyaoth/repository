%define debug_package %{nil}
#
%define hiawatha_home %{_localstatedir}/cache/hiawatha
%define hiawatha_user hiawatha
%define hiawatha_group hiawatha
%define hiawatha_loggroup adm

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?fedora} >= 18
Group: System Environment/Daemons
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
%define with_spdy 1
%endif

# end of distribution specific definitions

Summary: Hiawatha is an open source webserver with a focus on security.
Name: ulyaoth-hiawatha
Version: 9.14
Release: 3%{?dist}
BuildArch: x86_64
Vendor: Hiawatha.
URL: https://www.hiawatha-webserver.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://downloads.ulyaoth.net/hiawatha-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hiawatha/SOURCES/hiawatha.service
Source2: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hiawatha/SOURCES/hiawatha.init
Source3: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hiawatha/SOURCES/hiawatha-logrotate

License: GPLv2

BuildRoot: %{_tmppath}/hiawatha-%{version}-%{release}-root
BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: glibc-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: zlib-devel
BuildRequires: ulyaoth-mbedtls2

Requires: libxml2
Requires: libxslt
Requires: ulyaoth-mbedtls2

Provides: hiawatha
Provides: ulyaoth-hiawatha

%description
Hiawatha is an open source webserver with a focus on security. I started Hiawatha in January 2002. Before that time, I had used several webservers, but I didn't like them. They had unlogical, almost cryptic configuration syntax and none of them gave me a good feeling about their security and robustness. So, I decided it was time to write my own webserver. I never thought that my webserver would become what it is today, but I enjoyed working on it and liked to have my own open source project. In the years that followed, Hiawatha became a fully functional webserver.

%prep
%setup -q -n hiawatha-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX="" \
      -DCMAKE_INSTALL_BINDIR=%{_bindir} \
      -DCMAKE_INSTALL_SBINDIR=%{_sbindir} \
      -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_MANDIR=%{_mandir} \
      -DCONFIG_DIR=%{_sysconfdir}/hiawatha \
      -DLOG_DIR=%{_localstatedir}/log/hiawatha \
      -DPID_DIR=%{_localstatedir}/run \
      -DWORK_DIR=%{_localstatedir}/cache/hiawatha \
      -DWEBROOT_DIR=/srv/hiawatha/public \
      -DENABLE_CACHE=on \
      -DENABLE_IPV6=on \
      -DENABLE_MONITOR=on \
      -DENABLE_RPROXY=on \
      -DENABLE_TLS=on \
      -DENABLE_TOMAHAWK=on \
      -DENABLE_TOOLKIT=on \
      -DENABLE_XSLT=on \
	  -DUSE_SYSTEM_MBEDTLS=on
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/hiawatha/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/hiawatha/sites-enabled
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/hiawatha/ssl

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/hiawatha.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/hiawatha
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/hiawatha

sed -i "s/#ServerId = www-data/ServerId = hiawatha/" %{buildroot}%{_sysconfdir}/hiawatha/hiawatha.conf
sed -i '107 c\Include /etc/hiawatha/sites-enabled/' %{buildroot}%{_sysconfdir}/hiawatha/hiawatha.conf
sed -i '19 c\ServerString = Hiawatha' %{buildroot}%{_sysconfdir}/hiawatha/hiawatha.conf
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir %{_sysconfdir}/hiawatha
%dir %{_sysconfdir}/hiawatha/sites-available
%dir %{_sysconfdir}/hiawatha/sites-enabled
%dir %{_sysconfdir}/hiawatha/ssl
%attr(0755,root,root) %dir %{_localstatedir}/cache/hiawatha
%attr(0755,root,root) %dir %{_localstatedir}/log/hiawatha
%dir /srv/hiawatha
%dir /srv/hiawatha/public
#%dir %{_libdir}/hiawatha/

%{_bindir}/ssi-cgi
%{_sbindir}/hiawatha
%{_sbindir}/wigwam
%{_sbindir}/cgi-wrapper
/srv/hiawatha/public/index.html
%{_mandir}/*

%config(noreplace) %{_sysconfdir}/hiawatha/hiawatha.conf
%config(noreplace) %{_sysconfdir}/hiawatha/cgi-wrapper.conf
%config(noreplace) %{_sysconfdir}/hiawatha/mimetype.conf
%config(noreplace) %{_sysconfdir}/hiawatha/error.xslt
%config(noreplace) %{_sysconfdir}/hiawatha/index.xslt
%config(noreplace) %{_sysconfdir}/logrotate.d/hiawatha

%if %{use_systemd}
%{_unitdir}/hiawatha.service
%else
%{_initrddir}/hiawatha
%endif

%pre
# Add the "hiawatha" user
getent group %{hiawatha_group} >/dev/null || groupadd -r %{hiawatha_group}
getent passwd %{hiawatha_user} >/dev/null || \
    useradd -r -g %{hiawatha_group} -s /sbin/nologin \
    -d %{hiawatha_home} -c "hiawatha user"  %{hiawatha_user}
exit 0

%post
# Register the hiawatha service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset hiawatha.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add hiawatha
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-hiawatha!

Please find the official documentation for hiawatha here:
* https://www.hiawatha-webserver.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/hiawatha ]; then
        if [ ! -e %{_localstatedir}/log/hiawatha/access.log ]; then
            touch %{_localstatedir}/log/hiawatha/access.log
            %{__chmod} 0640 %{_localstatedir}/log/hiawatha/access.log
            %{__chown} hiawatha:%{hiawatha_loggroup} %{_localstatedir}/log/hiawatha/access.log
        fi

        if [ ! -e %{_localstatedir}/log/hiawatha/error.log ]; then
            touch %{_localstatedir}/log/hiawatha/error.log
            %{__chmod} 640 %{_localstatedir}/log/hiawatha/error.log
            %{__chown} hiawatha:%{hiawatha_loggroup} %{_localstatedir}/log/hiawatha/error.log
        fi

		if [ ! -e %{_localstatedir}/log/hiawatha/system.log ]; then
            touch %{_localstatedir}/log/hiawatha/system.log
            %{__chmod} 640 %{_localstatedir}/log/hiawatha/system.log
            %{__chown} hiawatha:%{hiawatha_loggroup} %{_localstatedir}/log/hiawatha/system.log
        fi

        if [ ! -e %{_localstatedir}/log/hiawatha/garbage.log ]; then
            touch %{_localstatedir}/log/hiawatha/garbage.log
            %{__chmod} 640 %{_localstatedir}/log/hiawatha/garbage.log
            %{__chown} hiawatha:%{hiawatha_loggroup} %{_localstatedir}/log/hiawatha/garbage.log
        fi
		
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable hiawatha.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop hiawatha.service >/dev/null 2>&1 ||:
%else
    /sbin/service hiawatha stop > /dev/null 2>&1
    /sbin/chkconfig --del hiawatha
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service hiawatha status  >/dev/null 2>&1 || exit 0
    /sbin/service hiawatha upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check hiawatha's error.log"
fi

%changelog
* Sun Sep 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.14-3
- Updated to mbed TLS 2.1.1.

* Sun Sep 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.14-2
- Updated to mbed TLS 2.1.0.

* Fri Aug 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.14-1
- Updated to Hiawatha 9.14.
- Updated to mbed TLS 2.0.0.

* Tue Jun 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 9.13-1
- Initial release.