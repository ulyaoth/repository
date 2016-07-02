%define debug_package %{nil}
#
%define monkey_home %{_localstatedir}/cache/monkey
%define monkey_user monkey
%define monkey_group monkey
%define monkey_loggroup adm
%define mbedtls_version 2.3.0

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Summary: Monkey is a lightweight and powerful web server and development stack for GNU/Linux.
Name: ulyaoth-monkey
Version: 1.6.9
Release: 2%{?dist}
BuildArch: x86_64
Vendor: Monkey HTTP Daemon development group.
URL: http://monkey-project.com/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: http://monkey-project.com/releases/1.6/monkey-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-monkey/SOURCES/monkey.service
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-monkey/SOURCES/monkey.init
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-monkey/SOURCES/monkey.logrotate


License: GPLv2+

Requires: ulyaoth-mbedtls2.3 = %{mbedtls_version}

BuildRoot: %{_tmppath}/monkey-%{version}-%{release}-root
BuildRequires: ulyaoth-mbedtls2.3 = %{mbedtls_version}
BuildRequires: cmake

Obsoletes: ulyaoth-mbedtls
Obsoletes: ulyaoth-mbedtls2.1
Obsoletes: ulyaoth-mbedtls2.2

Provides: webserver
Provides: monkey
Provides: monkey-web-server
Provides: ulyaoth-monkey
Provides: ulyaoth-monkey-web-server

%description
Monkey is a lightweight and powerful web server and development stack for GNU/Linux.

It has been designed to be very scalable with low memory and CPU consumption, the perfect solution for embedded devices. Made for ARM, x86 and x64.

%prep
%setup -q -n monkey-%{version}

%build
%if %{use_systemd}
./configure \
  --malloc-libc \
  --prefix=/srv/monkey \
  --sbindir=%{_sbindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir}/monkey \
  --sysconfdir=%{_sysconfdir}/monkey \
  --webroot=/srv/monkey/public \
  --mandir=%{_mandir} \
  --logdir=%{_localstatedir}/log/monkey \
  --pidpath=%{_localstatedir}/run \
  --pidfile=monkey.pid \
  --enable-plugins=tls \
  --mbedtls-shared \
  --default-port=80 \
  --default-user=monkey \
  $*
%else
./configure \
  --malloc-libc \
  --prefix=/srv/monkey \
  --sbindir=%{_sbindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir}/monkey \
  --sysconfdir=%{_sysconfdir}/monkey \
  --webroot=/srv/monkey/public \
  --mandir=%{_mandir} \
  --logdir=%{_localstatedir}/log/monkey \
  --pidpath=%{_localstatedir}/run \
  --pidfile=monkey.pid \
  --enable-plugins=tls \
  --mbedtls-shared \
  --default-port=80 \
  --default-user=root \
  $*
%endif
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT/var/log/monkey

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/monkey.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/monkey
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/monkey

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/monkey
%{_sbindir}/mk_passwd

%dir /etc/monkey
%dir /usr/include/monkey
%dir /srv/monkey
%dir /srv/monkey/public
%dir /var/log/monkey

/srv/monkey/*
%{_includedir}/monkey/*
%{_sysconfdir}/monkey/*
%{_libdir}/*
%{_mandir}/*

%config(noreplace) /etc/monkey/monkey.conf
%config(noreplace) /etc/monkey/plugins/cheetah/cheetah.conf
%config(noreplace) /etc/monkey/plugins/dirlisting/dirhtml.conf
%config(noreplace) /etc/monkey/plugins/fastcgi/fastcgi.conf
%config(noreplace) /etc/monkey/plugins/logger/logger.conf
%config(noreplace) /etc/monkey/plugins/mandril/mandril.conf
%config(noreplace) /etc/logrotate.d/monkey

%attr(755, monkey, adm) /var/log/monkey

%if %{use_systemd}
%{_unitdir}/monkey.service
%else
%{_initrddir}/monkey
%endif

%pre
# Add the "monkey" user
getent group %{monkey_group} >/dev/null || groupadd -r %{monkey_group}
getent passwd %{monkey_user} >/dev/null || \
    useradd -r -g %{monkey_group} -s /sbin/nologin \
    -d %{monkey_home} -c "monkey user"  %{monkey_user}
exit 0

%post
# Register the monkey service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset monkey.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add monkey
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-monkey!

Please find the official documentation for monkey here:
* http://monkey-project.com/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/monkey ]; then
        if [ ! -e %{_localstatedir}/log/monkey/access.log ]; then
            touch %{_localstatedir}/log/monkey/access.log
            %{__chmod} 640 %{_localstatedir}/log/monkey/access.log
            %{__chown} monkey:%{monkey_loggroup} %{_localstatedir}/log/monkey/access.log
        fi

        if [ ! -e %{_localstatedir}/log/monkey/error.log ]; then
            touch %{_localstatedir}/log/monkey/error.log
            %{__chmod} 640 %{_localstatedir}/log/monkey/error.log
            %{__chown} monkey:%{monkey_loggroup} %{_localstatedir}/log/monkey/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable monkey.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop monkey.service >/dev/null 2>&1 ||:
%else
    /sbin/service monkey stop > /dev/null 2>&1
    /sbin/chkconfig --del monkey
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif

%changelog
* Sat Jul 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.9-2
- Updating to use mbedTLS 2.3.0.

* Mon Jun 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.9-1
- Updated to Monkey 1.6.9.

* Fri Jan 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.8-1
- Updated to Monkey 1.6.8.

* Tue Jan 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.7-2
- Added obsoletes for ulyaoth-mbedtls and ulyaoth-mbedtls2.1.

* Fri Jan 8 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.7-1
- Updated to Monkey 1.6.7.
- Updating to use MbedTLS 2.2.1.

* Sat Nov 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.6-1
- Updated to Monkey 1.6.6.

* Sun Nov 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.5-3
- Fixed dependency error while upgrading.

* Sat Nov 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.5-2
- Updating to use MbedTLS 2.2.0.

* Sun Nov 1 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.5-1
- Updated to Monkey 1.6.5.

* Thu Oct 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.3-1
- Updated to Monkey 1.6.3.
- Updating to use MbedTLS 2.1.2.

* Sun Sep 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.2-2
- Updating to use MbedTLS 2.1.1.

* Sat Sep 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.2-1
- Updated to Monkey 1.6.2.

* Sat Aug 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.1-1
- Updated to Monkey 1.6.1.

* Wed Aug 12 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.0-1
- Updated to Monkey 1.6.0.

* Sun May 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.6-2
- Adding Secure Socket Layers (SSL) support.

* Fri May 1 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.6-1
- Initial release.