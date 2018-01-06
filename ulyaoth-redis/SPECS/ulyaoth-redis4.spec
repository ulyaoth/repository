
%define debug_package %{nil}
%define redis_home /var/lib/redis
%define redis_group redis
%define redis_user redis
%define redis_loggroup adm

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
%endif

%if 0%{?fedora} >= 18
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Redis is an in-memory data structure store, used as a database, cache and message broker.
Name:       ulyaoth-redis4
Version:    4.0.6
Release:    1%{?dist}
BuildArch: x86_64
License:    three clause BSD license
Group:      Applications/Databases
URL:        http://redis.io/
Vendor:     Salvatore Sanfilippo
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://download.redis.io/releases/redis-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SOURCES/redis4.conf
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SOURCES/sentinel4.conf
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SOURCES/redis.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SOURCES/redis.init
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SOURCES/COPYING
BuildRoot:  %{_tmppath}/redis-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  tcl

Provides:  redis
Provides:  redis4
provides:  ulyaoth-redis4

%description
Redis is an open source (BSD licensed), in-memory data structure store, used as database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.


%prep
%setup -q -n redis-%{version}

%build
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install PREFIX=$RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/licenses/redis
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/redis
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/redis
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/redis

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/redis/redis.conf
%{__install} -m 644 -p %{SOURCE2} \
   $RPM_BUILD_ROOT%{_sysconfdir}/redis/sentinel.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT/usr/share/licenses/redis/COPYING

mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT/usr/bin/
%{__rm} -rf $RPM_BUILD_ROOT/bin

%if %{use_systemd}
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/redis.service
%else
sed -i '/#daemonize yes/c\daemonize yes' $RPM_BUILD_ROOT%{_sysconfdir}/redis/redis.conf
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE4} \
   $RPM_BUILD_ROOT%{_initrddir}/redis
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/redis-benchmark
/usr/bin/redis-check-aof
/usr/bin/redis-cli
/usr/bin/redis-sentinel
/usr/bin/redis-server
/usr/bin/redis-check-rdb
%dir /usr/share/licenses/redis
/usr/share/licenses/redis/COPYING

%attr(0755,redis,redis) %config(noreplace) %{_sysconfdir}/redis/redis.conf
%attr(0755,redis,redis) %config(noreplace) %{_sysconfdir}/redis/sentinel.conf
%attr(0755,redis,redis) %dir %{_localstatedir}/lib/redis
%attr(0755,redis,adm) %dir %{_localstatedir}/log/redis
%attr(0755,redis,redis) %dir %{_sysconfdir}/redis

%if %{use_systemd}
%{_unitdir}/redis.service
%else
%{_initrddir}/redis
%endif

%pre
# Add the "redis" user
getent group %{redis_group} >/dev/null || groupadd -r %{redis_group}
getent passwd %{redis_user} >/dev/null || \
    useradd -r -g %{redis_group} -s /sbin/nologin \
    -d %{redis_home} -c "redis user"  %{redis_user}
exit 0

%post
# Register the redis service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset redis.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add redis
%endif
    # print site info
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-redis4!

Please find the official documentation for redis here:
* http://redis.io

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/redis ]; then
        if [ ! -e %{_localstatedir}/log/redis/redis.log ]; then
		    touch %{_localstatedir}/log/redis/redis.log
            %{__chmod} 644 %{_localstatedir}/log/redis/redis.log
            %{__chown} redis:%{redis_loggroup} %{_localstatedir}/log/redis/redis.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable redis.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop redis.service >/dev/null 2>&1 ||:
%else
    /sbin/service redis stop > /dev/null 2>&1
    /sbin/chkconfig --del redis
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif

%changelog
* Sat Jan 6 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 4.0.6-1
- Updated Redis 4 to 4.0.6.

* Sun Nov 19 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 4.0.2-1
- Initial Release.