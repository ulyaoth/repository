%define debug_package %{nil}
#
%define clamav_home %{_localstatedir}/cache/clamav
%define clamav_user clamav
%define clamav_group clamav
%define clamav_loggroup adm

Summary: ClamAV® is an open source (GPL) anti-virus engine .
Name: ulyaoth-clamav
Version: 0.99.1
Release: 1%{?dist}
BuildArch: x86_64
Vendor: ClamAV.
URL: https://www.clamav.net
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://www.clamav.net/downloads/production/clamav-%{version}.tar.gz

License: GPLv2

BuildRoot: %{_tmppath}/hiawatha-%{version}-%{release}-root
BuildRequires: openssl-devel
BuildRequires: ncurses-devel
BuildRequires: json-devel
BuildRequires: libxml2-devel
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: bzip2-devel
BuildRequires: libcurl-devel

Requires: openssl
Requires: libxml2
Requires: ncurses
Requires: zlib
Requires: json
Requires: bzip2
Requires: pcre
Requires: libcurl

Provides: clamav
Provides: ulyaoth-clamav

%description
ClamAV® is an open source (GPL) anti-virus engine used in a variety of situations including email scanning, web scanning, and end point security. It provides a number of utilities including a flexible and scalable multi-threaded daemon, a command line scanner and an advanced tool for automatic database updates.
%prep
%setup -q -n clamav-%{version}

%build
./configure --prefix=/usr \
			--bindir=/usr/bin \
			--sbindir=/usr/sbin \
			--libexecdir=%{_libexecdir} \
			--sysconfdir=%{_sysconfdir} \
			--sharedstatedir=%{_sharedstatedir} \
			--localstatedir=%{_localstatedir} \
			--libdir=%{_libdir} \
			--includedir=%{_includedir} \
			--datarootdir=%{_datarootdir} \
			--datadir=%{_datadir} \
			--infodir=%{_infodir} \
			--localedir=/usr/share/locale \
			--mandir=%{_mandir} \
			--docdir=%{_docdir} \
			--enable-clamdtop \
			--with-openssl=/usr \
			--with-xml=/usr \
			--with-libjson \
			--with-zlib=/usr \
			--with-pcre \
			--with-iconv \
			--with-libbz2-prefix \
			--with-dbdir=/var/lib/clamav \
			--with-libncurses-prefix \
			--with-libcurl
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
# Add the "clamav" user
getent group %{clamav_group} >/dev/null || groupadd -r %{clamav_group}
getent passwd %{clamav_user} >/dev/null || \
    useradd -r -g %{clamav_group} -s /sbin/nologin \
    -d %{clamav_home} -c "clamav user"  %{clamav_user}
exit 0

%post
# Register the clamav service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset clamav.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add clamav
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-clamav!

Please find the official documentation for clamav here:
* https://www.clamav.net

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

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
    /usr/bin/systemctl --no-reload disable clamav.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop clamav.service >/dev/null 2>&1 ||:
%else
    /sbin/service clamav stop > /dev/null 2>&1
    /sbin/chkconfig --del clamav
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service clamav status  >/dev/null 2>&1 || exit 0
    /sbin/service clamav upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check clamav's error.log"
fi

%changelog
* Sun Mar 20 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.99.1-1
- Initial release.
