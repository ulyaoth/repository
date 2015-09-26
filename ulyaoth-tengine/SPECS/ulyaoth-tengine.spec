#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm

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
Version: 2.1.1
Release: 2%{?dist}
BuildArch: x86_64
Vendor: Taobao
URL: http://tengine.taobao.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: http://tengine.taobao.org/download/tengine-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/logrotate
Source2: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/tengine.init
Source3: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.sysconf
Source4: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.conf
Source5: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.vh.default.conf
Source6: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.vh.example_ssl.conf
Source7: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.suse.init
Source8: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/tengine.service
Source9: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.upgrade.sh
Source10: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/SOURCES/nginx.suse.logrotate

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

Provides: webserver
Provides: tengine
Provides: nginx
Provides: ulyaoth-tengine
Provides: ulyaoth-nginx

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
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
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
		--with-http_spdy_module \
		--dso-path=%{_sysconfdir}/nginx/modules \
		--dso-tool-path=%{_sbindir} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/tengine-%{version}/objs/nginx \
        %{_builddir}/tengine-%{version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
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
		--with-http_spdy_module \
		--dso-path=%{_sysconfdir}/nginx/modules \
		--dso-tool-path=%{_sbindir} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-enabled
   
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/tengine.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/tengine
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/tengine-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx
%{_sbindir}/dso_tool

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/modules
%dir %{_sysconfdir}/nginx/include
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/sites-available
%dir %{_sysconfdir}/nginx/sites-enabled

%{_sysconfdir}/nginx/modules/*
%{_sysconfdir}/nginx/include/*

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf
%config %{_sysconfdir}/nginx/browsers
%config %{_sysconfdir}/nginx/module_stubs

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/tengine.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/tengine
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
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

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/error.log
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
* Tue Sep 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.1-2
- Fixed wrong preun and postun as repoted by Botao Pan in issue #17.

* Sun Sep 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.1-1
- Updated to Tengine 2.1.1.

* Sun Apr 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.2-1
- Initial release.