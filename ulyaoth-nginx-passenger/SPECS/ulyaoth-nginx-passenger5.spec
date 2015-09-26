#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm
%define nginx_version 1.8.0

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
%endif

# end of distribution specific definitions

Summary: High performance web server / Phusion Passenger web & app
Name: ulyaoth-nginx-passenger5
Version: 5.0.18
Release: 1%{?dist}
BuildArch: x86_64
Vendor: nginx inc. / Phusion
URL: https://www.phusionpassenger.com/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: http://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source1: logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source6: nginx.vh.example_ssl.conf
Source7: nginx.suse.init
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: nginx.vh.passenger5.conf
Source11: passenger.tar.gz

License: 2-clause BSD-like license

Requires: openssl
Requires: ruby
Requires: GeoIP

BuildRoot: %{_tmppath}/nginx-%{nginx_version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: curl-devel
BuildRequires: rubygem-rake
BuildRequires: GeoIP
BuildRequires: GeoIP-devel

Provides: webserver
Provides: nginx
Provides: nginx-passenger
Provides: nginx-passenger5
Provides: passenger
Provides: passenger5
Provides: ulyaoth-nginx
Provides: ulyaoth-nginx-passenger
Provides: ulyaoth-nginx-passenger5

%description
nginx [engine x] is an HTTP and reverse proxy server, as well asa mail proxy server.
Phusion Passenger is a multi-language (Ruby, Python, Node) web & app server which can integrate into Apache and Nginx

%package debug
Summary: debug version of nginx with passenger
Group: System Environment/Daemons
Requires: ulyaoth-nginx-passenger5
%description debug
Not stripped version of nginx and passenger built with the debugging log support.

%prep
%setup -q -n nginx-%{nginx_version}

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
        --with-http_geoip_module \
	    --add-module=/etc/nginx/modules/passenger/ext/nginx \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-http_spdy_module \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/nginx-%{nginx_version}/objs/nginx \
        %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug
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
        --with-http_geoip_module \
        --add-module=/etc/nginx/modules/passenger/ext/nginx \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-http_spdy_module \
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
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/passenger
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx/passenger_temp

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf
%{__install} -m 644 -p %{SOURCE10} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/passenger.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

#Create vhost directories
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-enabled   
   
# Install Passenger
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules
tar xvf %{SOURCE11} -C $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules/

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/nginx.service
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
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/sites-available
%dir %{_sysconfdir}/nginx/sites-enabled
%dir %{_sysconfdir}/nginx/modules
%{_sysconfdir}/nginx/modules/*

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/passenger.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx/passenger_temp
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/passenger


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
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-nginx-passenger5!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

Please find the official documentation or the enterprise version for passenger here:
* https://www.phusionpassenger.com/ 

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
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
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
* Sat Sep 12 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.18-1
- Updated to Passenger 5.0.18.

* Mon Aug 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.16-1
- Updated to Passenger 5.0.16.

* Thu Jul 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.15-1
- Updated to Passenger 5.0.15.

* Thu Jul 16 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.14-1
- Updated to Passenger 5.0.14.

* Sun Jul 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.13-1
- Updated to Passenger 5.0.13.

* Fri Jun 26 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.11-1
- Updated to Passenger 5.0.11.

* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.10-1
- Updated to Passenger 5.0.10.

* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.9-1
- Updated to Passenger 5.0.9.

* Wed May 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.8-1
- Updated to Passenger 5.0.8.

* Tue Apr 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.7-1
- Updated to Passenger 5.0.7.

* Wed Apr 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-5
- Updated to Nginx 1.8.0.

* Wed Apr 8 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-4
- Updated to Nginx 1.6.3.

* Sat Apr 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-3
- Removing rubyrails-gem dependency from package.

* Fri Apr 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-2
- Created a temp dir and log dir for passenger as requirement for selinux package.

* Tue Mar 31 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-1
- Update to Passenger 5.0.6.

* Thu Mar 26 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.5-1
- Changing the version numbering.

* Wed Mar 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-1 5.0.5
- Update to Passenger 5.0.5.

* Wed Mar 18 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-1 5.0.4
- Update to Passenger 5.0.4.

* Sun Mar 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-3 5.0.3
- Fixed the missing systemd-devel problem.

* Thu Mar 12 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-2 5.0.3
- Updating to Passenger 5.0.3
- Added support for Fedora 22 and CentOS 6 & 7.
- i386 support.
- Forced EPEL for RHEL6 for GeoIP.
- Cleaned spec file.

* Sun Mar 08 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-1 5.0.2
- Updating to Passenger 5.0.2.

* Thu Mar 05 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.6.2-1 5.0.1
- Creating spec file for Passenger 5.0.1.