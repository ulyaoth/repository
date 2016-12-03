#
%define tengine_home %{_localstatedir}/cache/tengine
%define tengine_user tengine
%define tengine_group tengine
%define tengine_loggroup adm

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?fedora} >= 18
Group: System Environment/Daemons
Requires: systemd
BuildRequires: systemd
%define with_spdy 1
%endif

# end of distribution specific definitions

Summary: High performance web server
Name: ulyaoth-tengine
Version: 2.2.0
Release: 1%{?dist}
BuildArch: x86_64
Vendor: Taobao
URL: http://tengine.taobao.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://github.com/alibaba/tengine/archive/tengine-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/logrotate
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.init
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.sysconf
Source4: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.conf
Source5: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.vh.default.conf
Source6: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.vh.example_ssl.conf
Source7: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.suse.init
Source8: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.service
Source9: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.upgrade.sh
Source10: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SOURCES/tengine.suse.logrotate

License: 2-clause BSD-like license


Requires: openssl
Requires: geoip

BuildRoot: %{_tmppath}/tengine-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: geoip
BuildRequires: geoip-devel
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: curl-devel

Provides: tengine
Provides: ulyaoth-tengine

%description
Tengine is a web server originated by Taobao, the largest e-commerce website in Asia.

%package debug
Summary: debug version of tengine
Group: System Environment/Daemons
Requires: ulyaoth-tengine
%description debug
Not stripped version of tengine built with the debugging log support.

%prep
%setup -q -n tengine-%{version}

%build
./configure \
        --prefix=%{_sysconfdir}/tengine \
        --sbin-path=%{_sbindir}/tengine \
        --conf-path=%{_sysconfdir}/tengine/tengine.conf \
        --error-log-path=%{_localstatedir}/log/tengine/error.log \
        --http-log-path=%{_localstatedir}/log/tengine/access.log \
        --pid-path=%{_localstatedir}/run/tengine.pid \
        --lock-path=%{_localstatedir}/run/tengine.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/tengine/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/tengine/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/tengine/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/tengine/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/tengine/scgi_temp \
        --user=%{tengine_user} \
        --group=%{tengine_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_dav_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module=shared \
        --with-http_secure_link_module=shared \
        --with-http_flv_module=shared \
        --with-http_mp4_module=shared \
        --with-http_sub_module=shared \
		--with-http_addition_module=shared \
		--with-http_memcached_module=shared \
		--with-http_fastcgi_module=shared \
		--with-http_geoip_module=shared \
		--with-http_autoindex_module=shared \
		--with-http_access_module=shared \
		--with-http_limit_conn_module=shared \
		--with-http_limit_req_module=shared \
		--with-http_sysguard_module=shared \
		--with-http_map_module=shared \
		--with-http_split_clients_module=shared \
		--with-http_user_agent_module=shared \
		--with-http_referer_module=shared \
		--with-http_rewrite_module=shared \
		--with-http_uwsgi_module=shared \
		--with-http_scgi_module=shared \
		--with-http_empty_gif_module=shared \
		--with-http_browser_module=shared \
		--with-http_slice_module=shared \
		--with-http_concat_module=shared \
		--with-http_upstream_ip_hash_module=shared \
		--with-http_upstream_least_conn_module=shared \
		--with-http_upstream_session_sticky_module=shared \
		--with-http_upstream_consistent_hash_module=shared \
		--with-mail \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
		--with-http_v2_module \
		--dso-path=%{_sysconfdir}/tengine/modules \
		--dso-tool-path=%{_sbindir} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/tengine-%{version}/objs/tengine \
        %{_builddir}/tengine-%{version}/objs/tengine.debug
./configure \
        --prefix=%{_sysconfdir}/tengine \
        --sbin-path=%{_sbindir}/tengine \
        --conf-path=%{_sysconfdir}/tengine/tengine.conf \
        --error-log-path=%{_localstatedir}/log/tengine/error.log \
        --http-log-path=%{_localstatedir}/log/tengine/access.log \
        --pid-path=%{_localstatedir}/run/tengine.pid \
        --lock-path=%{_localstatedir}/run/tengine.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/tengine/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/tengine/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/tengine/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/tengine/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/tengine/scgi_temp \
        --user=%{tengine_user} \
        --group=%{tengine_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_dav_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module=shared \
        --with-http_secure_link_module=shared \
		--with-http_flv_module=shared \
        --with-http_mp4_module=shared \
        --with-http_sub_module=shared \
		--with-http_addition_module=shared \
		--with-http_memcached_module=shared \
		--with-http_fastcgi_module=shared \
		--with-http_geoip_module=shared \
		--with-http_autoindex_module=shared \
		--with-http_access_module=shared \
		--with-http_limit_conn_module=shared \
		--with-http_limit_req_module=shared \
		--with-http_sysguard_module=shared \
		--with-http_map_module=shared \
		--with-http_split_clients_module=shared \
		--with-http_user_agent_module=shared \
		--with-http_referer_module=shared \
		--with-http_rewrite_module=shared \
		--with-http_uwsgi_module=shared \
		--with-http_scgi_module=shared \
		--with-http_empty_gif_module=shared \
		--with-http_browser_module=shared \
		--with-http_slice_module=shared \
		--with-http_concat_module=shared \
		--with-http_upstream_ip_hash_module=shared \
		--with-http_upstream_least_conn_module=shared \
		--with-http_upstream_session_sticky_module=shared \
		--with-http_upstream_consistent_hash_module=shared \
		--with-mail \
		--with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
		--with-http_v2_module \
		--dso-path=%{_sysconfdir}/tengine/modules \
		--dso-tool-path=%{_sbindir} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/tengine
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/tengine/html $RPM_BUILD_ROOT%{_datadir}/tengine/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/tengine/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/tengine/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/tengine
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/tengine
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/tengine
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/tengine/conf.d

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/tengine/tengine.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/tengine/tengine.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/tengine/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/tengine/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/tengine

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/tengine/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/tengine/sites-enabled
   
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/tengine.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/tengine
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/tengine/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/tengine
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/tengine
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/tengine
%{__install} -m644 %{_builddir}/tengine-%{version}/objs/tengine.debug \
   $RPM_BUILD_ROOT%{_sbindir}/tengine.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/tengine
%{_sbindir}/dso_tool

%dir %{_sysconfdir}/tengine
%dir %{_sysconfdir}/tengine/modules
%dir %{_sysconfdir}/tengine/include
%dir %{_sysconfdir}/tengine/conf.d
%dir %{_sysconfdir}/tengine/sites-available
%dir %{_sysconfdir}/tengine/sites-enabled

%{_sysconfdir}/tengine/modules/*
%{_sysconfdir}/tengine/include/*

%config(noreplace) %{_sysconfdir}/tengine/tengine.conf
%config(noreplace) %{_sysconfdir}/tengine/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/tengine/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/tengine/mime.types
%config(noreplace) %{_sysconfdir}/tengine/fastcgi_params
%config(noreplace) %{_sysconfdir}/tengine/scgi_params
%config(noreplace) %{_sysconfdir}/tengine/uwsgi_params
%config(noreplace) %{_sysconfdir}/tengine/koi-utf
%config(noreplace) %{_sysconfdir}/tengine/koi-win
%config(noreplace) %{_sysconfdir}/tengine/win-utf
%config %{_sysconfdir}/tengine/browsers
%config %{_sysconfdir}/tengine/module_stubs

%config(noreplace) %{_sysconfdir}/logrotate.d/tengine
%config(noreplace) %{_sysconfdir}/sysconfig/tengine
%if %{use_systemd}
%{_unitdir}/tengine.service
%dir %{_libexecdir}/initscripts/legacy-actions/tengine
%{_libexecdir}/initscripts/legacy-actions/tengine/*
%else
%{_initrddir}/tengine
%endif

%dir %{_datadir}/tengine
%dir %{_datadir}/tengine/html
%{_datadir}/tengine/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/tengine
%attr(0755,root,root) %dir %{_localstatedir}/log/tengine

%files debug
%attr(0755,root,root) %{_sbindir}/tengine.debug

%pre
# Add the "Tengine" user
getent group %{tengine_group} >/dev/null || groupadd -r %{tengine_group}
getent passwd %{tengine_user} >/dev/null || \
    useradd -r -g %{tengine_group} -s /sbin/nologin \
    -d %{tengine_home} -c "Tengine user"  %{tengine_user}
exit 0

%post
# Register the tengine service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset tengine.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add tengine
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-tengine!

Please find the official documentation for tengine here:
* http://tengine.taobao.org/

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/tengine ]; then
        if [ ! -e %{_localstatedir}/log/tengine/access.log ]; then
            touch %{_localstatedir}/log/tengine/access.log
            %{__chmod} 640 %{_localstatedir}/log/tengine/access.log
            %{__chown} %{tengine_user}:%{tengine_loggroup} %{_localstatedir}/log/tengine/access.log
        fi

        if [ ! -e %{_localstatedir}/log/tengine/error.log ]; then
            touch %{_localstatedir}/log/tengine/error.log
            %{__chmod} 640 %{_localstatedir}/log/tengine/error.log
            %{__chown} %{tengine_user}:%{tengine_loggroup} %{_localstatedir}/log/tengine/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable tengine.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop tengine.service >/dev/null 2>&1 ||:
%else
    /sbin/service tengine stop > /dev/null 2>&1
    /sbin/chkconfig --del tengine
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service tengine status  >/dev/null 2>&1 || exit 0
    /sbin/service tengine upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check tengine's error.log"
fi

%changelog
* Sat Dec 3 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.0-1
- Updated to Tengine 2.2.0.

* Fri Jan 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.2-1
- Updated to Tengine 2.1.2.
- Added http/2.

* Tue Sep 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.1-2
- Fixed wrong preun and postun as repoted by Botao Pan in issue #17.

* Sun Sep 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.1-1
- Updated to Tengine 2.1.1.

* Sun Apr 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.2-1
- Initial release.