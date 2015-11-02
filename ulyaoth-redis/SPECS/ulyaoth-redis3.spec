
%define debug_package %{nil}
%define redis_home /var/lib/redis
%define redis_group redis
%define redis_user redis

Summary:    Tomcat native library
Name:       ulyaoth-redis
Version:    3.0.5
Release:    1%{?dist}
BuildArch: x86_64
License:    three clause BSD license
Group:      Applications/Databases
URL:        http://redis.io/
Vendor:     Salvatore Sanfilippo
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://download.redis.io/releases/redis-%{version}.tar.gz
Source1:    redis.conf
Source2:    sentinel.conf
Source3:    redis.service
Source4:    redis.init
Source5:    COPYING
BuildRoot:  %{_tmppath}/redis-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  tcl

Provides:  redis
Provides:  redis3
provides:  ulyaoth-redis3

%description
Redis is an open source (BSD licensed), in-memory data structure store, used as database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.


%prep
%setup -q -n redis-%{version}

%build
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%make_install

mkdir -p $RPM_BUILD_ROOT/var/log/redis
mkdir -p $RPM_BUILD_ROOT/var/lib/redis
mkdir -p $RPM_BUILD_ROOT/usr/bin

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT/etc/tmpfiles.d/ironbee.conf

mv $RPM_BUILD_ROOT/usr/local/bin/* $RPM_BUILD_ROOT/usr/bin/


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/local/bin/redis-benchmark
/usr/local/bin/redis-check-aof
/usr/local/bin/redis-check-dump
/usr/local/bin/redis-cli
/usr/local/bin/redis-sentinel
/usr/local/bin/redis-server

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-redis3!

Please find the official documentation for redis here:
* http://redis.io

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Mon Nov 2 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.0.5-1
- Initial Release.