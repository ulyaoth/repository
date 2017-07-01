#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm
%define _group System Environment/Daemons

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

%if 0%{?rhel}  == 5
%define _group System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
BuildRequires: perl
BuildRequires: GeoIP-devel
%endif

%if 0%{?rhel}  == 6
%define _group System Environment/Daemons
%define with_http2 1
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-Embed
BuildRequires: GeoIP-devel
%endif

%if 0%{?rhel}  == 7
%define _group System Environment/Daemons
%define perlldopts --with-ld-opt="-Wl,-E"
%define epoch 1
%define with_http2 1
Epoch: %{epoch}
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-Embed
BuildRequires: GeoIP-devel
%endif

%if 0%{?fedora} >= 18
%define _group System Environment/Daemons
%define perlldopts --with-ld-opt="-Wl,-E"
%define epoch 1
%define with_http2 1
Epoch: %{epoch}
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-Embed
BuildRequires: GeoIP-devel
%endif

%if 0%{?suse_version} == 1315
%define _group Productivity/Networking/Web/Servers
%define with_http2 1
%define nginx_loggroup trusted
Requires(pre): shadow
Requires: systemd
BuildRequires: libopenssl-devel
BuildRequires: systemd
BuildRequires: perl
BuildRequires: libGeoIP-devel
%endif

# end of distribution specific definitions

%define main_version                 1.13.2
%define main_release                 1%{?dist}.ngx
%define njs_version                  0.1.11
%define module_xslt_version          %{main_version}
%define module_xslt_release          1%{?dist}.ngx
%define module_geoip_version         %{main_version}
%define module_geoip_release         1%{?dist}.ngx
%define module_image_filter_version  %{main_version}
%define module_image_filter_release  1%{?dist}.ngx
%define module_perl_version          %{main_version}
%define module_perl_release          1%{?dist}.ngx
%define module_njs_version           %{main_version}.%{njs_version}
%define module_njs_release           1%{?dist}.ngx
%define module_echo_version  0.60
%define module_echo_release  8%{?dist}

%define bdir %{_builddir}/nginx-%{main_version}/%{name}-%{main_version}

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags))

%define COMMON_CONFIGURE_ARGS $(echo "\
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --modules-path=%{_libdir}/nginx/modules \
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
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-http_xslt_module=dynamic \
        --with-http_image_filter_module=dynamic \
        --with-http_geoip_module=dynamic \
        --with-http_perl_module=dynamic \
        --add-dynamic-module=njs-%{njs_version}/nginx \
        --with-threads \
        --with-stream \
        --with-stream_ssl_module \
        --with-stream_geoip_module=dynamic \
		--with-stream_ssl_preread_module \
        --with-http_slice_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --add-dynamic-module=/home/ulyaoth/echo-module \
        %{?with_http2:--with-http_v2_module}")

Summary: High performance web server
Name: ulyaoth-nginx-mainline
Version: %{main_version}
Release: %{main_release}
Vendor: Nginx, Inc.
URL: http://nginx.org/
Group: %{_group}
Packager: Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>

Source0: http://nginx.org/download/nginx-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/logrotate
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.init.in
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.sysconf
Source4: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.conf
Source5: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.vh.default.conf
Source7: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx-debug.sysconf
Source8: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.service
Source9: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.upgrade.sh
Source10: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx.suse.logrotate
Source11: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/nginx-debug.service
Source12: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SOURCES/COPYRIGHT
Source13: https://github.com/nginx/njs/archive/%{njs_version}.tar.gz

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{main_version}-%{main_release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: libxslt-devel
BuildRequires: gd-devel
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-Embed
BuildRequires: GeoIP-devel
BuildRequires: openssl-devel

Requires: openssl

Provides: webserver
Provides: nginx
Provides: ulyaoth-nginx-mainline

Conflicts: ulyaoth-nginx
Obsoletes: ulyaoth-nginx-mainline-naxsi

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

%if 0%{?suse_version} == 1315
%debug_package
%endif

%package module-xslt
Version: %{module_xslt_version}
Release: %{module_xslt_release}
Group: %{_group}
Requires: nginx = %{?epoch:%{epoch}:}%{main_version}-%{main_release}
Summary: nginx xslt module
%description module-xslt
Dynamic xslt module for nginx.

%package module-image-filter
Version: %{module_image_filter_version}
Release: %{module_image_filter_release}
Group: %{_group}
Requires: nginx = %{?epoch:%{epoch}:}%{main_version}-%{main_release}
Summary: nginx image filter module
%description module-image-filter
Dynamic image filter module for nginx.

%package module-geoip
Version: %{module_geoip_version}
Release: %{module_geoip_release}
Group: %{_group}
Requires: nginx = %{?epoch:%{epoch}:}%{main_version}-%{main_release}
Summary: nginx geoip module
%description module-geoip
Dynamic geoip module for nginx.

%package module-perl
Version: %{module_perl_version}
Release: %{module_perl_release}
Group: %{_group}
Requires: nginx = %{?epoch:%{epoch}:}%{main_version}-%{main_release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Summary: nginx perl module
%description module-perl
Dynamic perl module for nginx.

%package module-njs
Version: %{module_njs_version}
Release: %{module_njs_release}
Group: %{_group}
Requires: nginx = %{?epoch:%{epoch}:}%{main_version}-%{main_release}
Summary: nginx nJScript module
%description module-njs
Dynamic nJScript module for nginx.

%package module-echo
Version: %{module_echo_version}
Release: %{module_echo_release}
Group: %{_group}
Requires: ulyaoth-nginx-mainline
Summary: nginx echo module
%description module-echo
Dynamic echo module for nginx.

%prep
%setup -q -n nginx-%{main_version}
tar xvzf %SOURCE13
cp %{SOURCE2} .
sed -e 's|%%DEFAULTSTART%%|2 3 4 5|g' -e 's|%%DEFAULTSTOP%%|0 1 6|g' \
    -e 's|%%PROVIDES%%|nginx|g' < %{SOURCE2} > nginx.init
sed -e 's|%%DEFAULTSTART%%||g' -e 's|%%DEFAULTSTOP%%|0 1 2 3 4 5 6|g' \
    -e 's|%%PROVIDES%%|nginx-debug|g' < %{SOURCE2} > nginx-debug.init

%build
./configure %{COMMON_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    %{?perlldopts} \
    --with-debug
make %{?_smp_mflags}
%{__mv} %{_builddir}/nginx-%{main_version}/objs/nginx \
    %{_builddir}/nginx-%{main_version}/objs/nginx-debug
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_xslt_filter_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_xslt_filter_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_image_filter_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_image_filter_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_geoip_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_geoip_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_perl_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_perl_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.so \
    %{_builddir}/nginx-%{main_version}/objs/src/http/modules/perl/blib/arch/auto/nginx/nginx-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_js_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_js_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_stream_js_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_stream_js_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_stream_geoip_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_stream_geoip_module-debug.so
%{__mv} %{_builddir}/nginx-%{main_version}/objs/ngx_http_echo_module.so \
    %{_builddir}/nginx-%{main_version}/objs/ngx_http_echo_module-debug.so
./configure %{COMMON_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    %{?perlldopts}
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor install

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -name nginx.so -exec chmod u+w '{}' \;

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules
cd $RPM_BUILD_ROOT%{_sysconfdir}/nginx && \
    %{__ln_s} ../..%{_libdir}/nginx/modules modules && cd -

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{main_version}
%{__install} -m 644 -p %{SOURCE12} \
    $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{main_version}/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx
%{__install} -m 644 -p %{SOURCE7} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx-debug

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-enabled

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__install} -m644 %SOURCE11 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx-debug.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
    $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 nginx.init $RPM_BUILD_ROOT%{_initrddir}/nginx
%{__install} -m755 nginx-debug.init $RPM_BUILD_ROOT%{_initrddir}/nginx-debug
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%if 0%{?suse_version}
%{__install} -m 644 -p %{SOURCE10} \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%else
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%endif

%{__install} -m755 %{_builddir}/nginx-%{main_version}/objs/nginx-debug \
    $RPM_BUILD_ROOT%{_sbindir}/nginx-debug

%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_xslt_filter_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_xslt_filter_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_image_filter_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_image_filter_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_geoip_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_geoip_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_perl_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_perl_module-debug.so
%{__mkdir} -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto/nginx
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/src/http/modules/perl/blib/arch/auto/nginx/nginx-debug.so \
    $RPM_BUILD_ROOT%{perl_vendorarch}/auto/nginx/nginx-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_js_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_js_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_stream_js_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_stream_js_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_stream_geoip_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_stream_geoip_module-debug.so
%{__install} -m644 %{_builddir}/nginx-%{main_version}/objs/ngx_http_echo_module-debug.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_echo_module-debug.so

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx
%{_sbindir}/nginx-debug

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/sites-available
%dir %{_sysconfdir}/nginx/sites-enabled
%dir %{_sysconfdir}/nginx/conf.d
%{_sysconfdir}/nginx/modules

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx-debug
%if %{use_systemd}
%{_unitdir}/nginx.service
%{_unitdir}/nginx-debug.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%{_initrddir}/nginx-debug
%endif

%attr(0755,root,root) %dir %{_libdir}/nginx
%attr(0755,root,root) %dir %{_libdir}/nginx/modules
%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%dir %{_datadir}/doc/%{name}-%{main_version}
%doc %{_datadir}/doc/%{name}-%{main_version}/COPYRIGHT

%files module-xslt
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_xslt_filter_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_xslt_filter_module-debug.so

%files module-image-filter
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_image_filter_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_image_filter_module-debug.so

%files module-geoip
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_geoip_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_geoip_module-debug.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_stream_geoip_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_stream_geoip_module-debug.so

%files module-perl
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_perl_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_perl_module-debug.so
%dir %{perl_vendorarch}/auto/nginx
%{perl_vendorarch}/nginx.pm
%{perl_vendorarch}/auto/nginx/nginx.so
%{perl_vendorarch}/auto/nginx/nginx-debug.so
%{_mandir}/man3/nginx.3pm*

%files module-njs
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_js_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_js_module-debug.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_stream_js_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_stream_js_module-debug.so

%files module-echo
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_echo_module.so
%attr(0644,root,root) %{_libdir}/nginx/modules/ngx_http_echo_module-debug.so

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset nginx-debug.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
    /sbin/chkconfig --add nginx-debug
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-nginx-mainline!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

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

%post module-xslt
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The XSLT dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_xslt_filter_module.so;

Please refer to the module documentation for further details:
http://nginx.org/en/docs/http/ngx_http_xslt_module.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%post module-geoip
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The GeoIP dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_geoip_module.so;
    load_module modules/ngx_stream_geoip_module.so;

Please refer to the module documentation for further details:
http://nginx.org/en/docs/http/ngx_http_geoip_module.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%post module-image-filter
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The image filter dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_image_filter_module.so;

Please refer to the module documentation for further details:
http://nginx.org/en/docs/http/ngx_http_image_filter_module.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%post module-perl
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The perl dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_perl_module.so;

Please refer to the module documentation for further details:
http://nginx.org/en/docs/http/ngx_http_perl_module.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%post module-njs
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The nJScript dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_js_module.so;
    load_module modules/ngx_stream_js_module.so;

Please refer to the module documentation for further details:
https://www.nginx.com/resources/wiki/nginScript/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%post module-echo
if [ $1 -eq 1 ]; then
    cat <<BANNER
----------------------------------------------------------------------

The echo dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_echo_module.so;

Please refer to the module documentation for further details:
https://github.com/openresty/echo-nginx-module

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
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
    /sbin/chkconfig --del nginx-debug
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%changelog
* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.60-8
- Updated nginx mainline to 1.13.2.

* Tue May 30 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-7
- Updated nginx mainline to 1.13.1.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-6
- Updated nginx mainline to 1.13.0.
- Updated nsj to 0.1.10.

* Sat Feb 25 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-5
- Recompiled with Nginx Mainline 1.11.10.
- Updated nsj to 0.1.9.

* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-4
- Updated to Nginx Mainline 1.11.6.
- Updated nsj to 0.1.5.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-3
- Recompiled with Nginx Mainline 1.11.5.

* Wed Sep 14 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-2
- Recompiled with Nginx Mainline 1.11.4.

* Sat Aug 20 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.60-1
- Updated to echo module 0.60.
- Recompiled with Nginx Mainline 1.11.3.

* Sun Jun 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.59-1
- Initial release for echo module.