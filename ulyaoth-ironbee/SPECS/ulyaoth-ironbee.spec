#
%define debug_package %{nil}
%define ironbee_home %{_sysconfdir}/ironbee
%define ironbee_user ironbee
%define ironbee_group ironbee

Summary: IronBee WAF Framework
Name: ulyaoth-ironbee
Version: 0.12.2
Release: 1%{?dist}
BuildArch: x86_64
Vendor: Qualys, Inc.
Group: System Environment/Daemons
URL: https://www.ironbee.com/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://github.com/ironbee/ironbee/archive/v%{version}.tar.gz
Source1: https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-ironbee/SOURCES/ironbee.conf

License: 2-clause BSD-like license

Requires: openssl
Requires: geoip
Requires: boost-chrono
Requires: boost-date-time
Requires: boost-filesystem
Requires: boost-iostreams
Requires: boost-program-options
Requires: boost-regex
Requires: boost-system
Requires: boost-thread
Requires: pcre
Requires: zlib
Requires: libxml2
Requires: uuid

BuildRoot: %{_tmppath}/ironbee-%{version}-%{release}-root
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: uuid-devel
BuildRequires: geoip-devel
BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: yajl-devel
BuildRequires: libpcap-devel
BuildRequires: libnet-devel
BuildRequires: ruby-devel
BuildRequires: boost-devel
BuildRequires: boost-build
BuildRequires: protobuf-devel

Provides: ironbee
Provides: ulyaoth-ironbee

%description
The next-generation open source web application firewall engine, designed to be modular, portable, and efficient, and to give you the tools you need to defend sites from attack.

%package debug
Summary: debug version of nginx compiled with Ironbee Open Source WAF. 
Group: System Environment/Daemons
Requires: ulyaoth-ironbee
%description debug
Not stripped version of nginx built with the debugging log support and compiled with Ironbee Open Source WAF.

%prep
%setup -q -n ironbee-%{version}

%build

./autogen.sh
./configure \
  --prefix=/usr \
  --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --sbindir=%{_sbindir} \
  --libexecdir=%{_libexecdir} \
  --sysconfdir=%{_sysconfdir} \
  --sharedstatedir=%{_sharedstatedir} \
  --localstatedir=%{_localstatedir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --oldincludedir=%{_includedir} \
  --datarootdir=%{_datadir} \
  --datadir=%{_datadir} \
  --infodir=%{_infodir} \
  --localedir=/usr/share/locale \
  --mandir=%{_mandir} \
  --docdir=%{_docdir} \
  --htmldir=%{_docdir} \
  --dvidir=%{_docdir} \
  --pdfdir=%{_docdir} \
  --psdir=%{_docdir} \
  --with-manager-control-socket=%{_localstatedir}/run/ironbee/ironbee_manager_controller.sock \
  CFLAGS="-fno-omit-frame-pointer -g" CXXFLAGS="-fno-omit-frame-pointer -g" \
        $*
make %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%make_install

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/ironbee
mkdir -p $RPM_BUILD_ROOT/etc/tmpfiles.d

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT/etc/tmpfiles.d/ironbee.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%attr(0755,%{ironbee_user}, %{ironbee_group}) %dir %{_sysconfdir}/ironbee
%attr(0644,%{ironbee_user}, %{ironbee_group}) %{_sysconfdir}/ironbee/ironbee.conf.example
%config(noreplace) %attr(0644,%{ironbee_user}, %{ironbee_group}) %{_sysconfdir}/ironbee/ironbee.conf
%attr(0755, %{ironbee_user}, %{ironbee_group}) %dir %{_localstatedir}/run/ironbee
%{_includedir}/*
%{_bindir}/*
%{_libexecdir}/*
%{_sysconfdir}/*
%{_libdir}/*
/etc/tmpfiles.d/ironbee.conf


%pre
# Add the "ironbee" user
getent group %{ironbee_group} >/dev/null || groupadd -r %{ironbee_group}
getent passwd %{ironbee_user} >/dev/null || \
    useradd -r -g %{ironbee_group} -s /sbin/nologin \
    -d %{ironbee_home} -c "ironbee user"  %{ironbee_user}
exit 0

%post
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-ironbee!

Please find the official Ironbee documentation here:
* https://www.ironbee.com/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun


%changelog
* Tue Sep 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.12.2-1
- Initial release of Ironbee 0.12.2.