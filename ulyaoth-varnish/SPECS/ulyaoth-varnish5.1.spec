%define varnish_home /var/lib/varnish
%define varnish_user varnish
%define varnish_group varnish
%define varnish_loggroup adm
%define debug_package %{nil}

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
BuildRequires: systemd-devel
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
%endif

# end of distribution specific definitions

Summary:    Varnish HTTP Cache
Name:       ulyaoth-varnish5.1
Version:    5.1.1
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD
Group:      System Environment/Daemons
URL:        https://varnish-cache.org
Vendor:     Varnish Software AS
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/varnishcache/varnish-cache/archive/varnish-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/default.vcl
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish.service
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnishlog.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnishncsa.service
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish.initrc
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnishlog.initrc
Source7:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnishncsa.initrc
Source8:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish-initrc.sysconfig
Source9:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish_reload_vcl
Source10:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish-systemd.sysconfig
Source11:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish-limits.conf
BuildRoot:  %{_tmppath}/varnish5-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: jemalloc-devel
BuildRequires: libedit-devel
BuildRequires: libtool
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
BuildRequires: python-sphinx
BuildRequires: graphviz

Requires: jemalloc
Requires: pcre
Requires: libedit

Provides: varnish
Provides: varnish5.1
Provides: ulyaoth-varnish5.1

Conflicts: ulyaoth-varnish3
Conflicts: ulyaoth-varnish4
Conflicts: ulyaoth-varnish4.1
Conflicts: ulyaoth-varnish5

%description
Varnish is an HTTP accelerator designed for content-heavy dynamic web sites as well as heavily consumed APIs.

%prep
%setup -q -n varnish-cache-varnish-%{version}

%build
./autogen.sh
./configure --prefix=/usr --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} --sharedstatedir=%{_sharedstatedir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datarootdir} --datadir=%{_datadir} --infodir=%{_infodir} --mandir=%{_mandir} --docdir=/usr/share/doc  
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

mkdir -p $RPM_BUILD_ROOT/var/lib/varnish

%{__install} -m 755 -p %{SOURCE9} \
    $RPM_BUILD_ROOT/usr/sbin/varnish_reload_vcl

mkdir -p $RPM_BUILD_ROOT/etc/security/limits.d/
%{__install} -m 644 -p %{SOURCE11} \
    $RPM_BUILD_ROOT/etc/security/limits.d/varnish.conf
	
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/varnish
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/varnish/default.vcl

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE10} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/varnish
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE8} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/varnish
%endif
	
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/varnish
	
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE2 \
    $RPM_BUILD_ROOT%{_unitdir}/varnish.service
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/varnishlog.service
%{__install} -m644 %SOURCE4 \
    $RPM_BUILD_ROOT%{_unitdir}/varnishncsa.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE5 \
    $RPM_BUILD_ROOT%{_initrddir}/varnish
%{__install} -m755 %SOURCE6 \
    $RPM_BUILD_ROOT%{_initrddir}/varnishlog
%{__install} -m755 %SOURCE7 \
    $RPM_BUILD_ROOT%{_initrddir}/varnishncsa
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
# Add the "varnish" user
getent group %{varnish_group} >/dev/null || groupadd -r %{varnish_group}
getent passwd %{varnish_user} >/dev/null || \
    useradd -r -g %{varnish_group} -s /sbin/nologin \
    -d %{varnish_home} -c "varnish user"  %{varnish_user}
exit 0

%files
%defattr(-,root,root,-)
/usr/sbin/varnishd
/usr/sbin/varnish_reload_vcl
/usr/bin/varnishadm
/usr/bin/varnishhist
/usr/bin/varnishlog
/usr/bin/varnishncsa
/usr/bin/varnishstat
/usr/bin/varnishtest
/usr/bin/varnishtop
/etc/sysconfig/varnish
/etc/security/limits.d/varnish.conf

%dir %{_sysconfdir}/varnish
%config(noreplace) %{_sysconfdir}/varnish/default.vcl

/usr/share/aclocal/varnish-legacy.m4
/usr/share/aclocal/varnish.m4

%dir /usr/share/varnish
%dir /usr/share/varnish/vcl
/usr/share/varnish/vmodtool.py
/usr/share/varnish/vmodtool.pyc
/usr/share/varnish/vmodtool.pyo
/usr/share/varnish/vcl/devicedetect.vcl

/usr/include/varnish/*

%{_libdir}/libvarnishapi.la
%{_libdir}/libvarnishapi.so
%{_libdir}/libvarnishapi.so.1
%{_libdir}/pkgconfig/varnishapi.pc
%{_libdir}/libvarnishapi.la
%{_libdir}/libvarnishapi.so
%{_libdir}/libvarnishapi.so.1.0.6
%{_libdir}/varnish/vmods/libvmod_directors.la
%{_libdir}/varnish/vmods/libvmod_directors.so
%{_libdir}/varnish/vmods/libvmod_std.la
%{_libdir}/varnish/vmods/libvmod_std.so

/usr/share/doc/builtin.vcl
/usr/share/doc/example.vcl
%{_mandir}/man1/varnishadm.1.gz
%{_mandir}/man1/varnishd.1.gz
%{_mandir}/man1/varnishhist.1.gz
%{_mandir}/man1/varnishlog.1.gz
%{_mandir}/man1/varnishncsa.1.gz
%{_mandir}/man1/varnishstat.1.gz
%{_mandir}/man1/varnishtest.1.gz
%{_mandir}/man1/varnishtop.1.gz
%{_mandir}/man3/vmod_directors.3.gz
%{_mandir}/man3/vmod_std.3.gz
%{_mandir}/man7/varnish-cli.7.gz
%{_mandir}/man7/varnish-counters.7.gz
%{_mandir}/man7/vcl.7.gz
%{_mandir}/man7/vsl-query.7.gz
%{_mandir}/man7/vsl.7.gz
%{_mandir}/man7/vtc.7.gz


%if %{use_systemd}
%{_unitdir}/varnish.service
%{_unitdir}/varnishncsa.service
%{_unitdir}/varnishlog.service
%else
%{_initrddir}/varnish
%{_initrddir}/varnishncsa
%{_initrddir}/varnishlog
%endif

%defattr(-,varnish,varnish,-)
%dir /var/lib/varnish
%dir /var/log/varnish

%attr(0755,varnish,varnish) /var/log/varnish

%post
/sbin/ldconfig
dd if=/dev/random of=/etc/varnish/secret count=1
# Register the varnish service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset varnish.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add varnish
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-varnish5.1!

Please find the official documentation for Varnish here:
* https://www.varnish-cache.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/varnish ]; then
        if [ ! -e %{_localstatedir}/log/varnish/varnish.log ]; then
            touch %{_localstatedir}/log/varnish/varnish.log
            %{__chmod} 640 %{_localstatedir}/log/varnish/varnish.log
            %{__chown} varnish:%{varnish_loggroup} %{_localstatedir}/log/varnish/varnish.log
        fi

        if [ ! -e %{_localstatedir}/log/varnish/varnishncsa.log ]; then
            touch %{_localstatedir}/log/varnish/varnishncsa.log
            %{__chmod} 640 %{_localstatedir}/log/varnish/varnishncsa.log
            %{__chown} varnish:%{varnish_loggroup} %{_localstatedir}/log/varnish/varnishncsa.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable varnish.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop varnish.service >/dev/null 2>&1 ||:
%else
    /sbin/service varnish stop > /dev/null 2>&1
    /sbin/chkconfig --del varnish
%endif
fi

%postun
/sbin/ldconfig
rm -rf /etc/varnish/secret
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service varnish status  >/dev/null 2>&1 || exit 0
    /sbin/service varnish upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.1.1-1
- Updated Varnish 5.1 to 5.1.1.

* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.1.0-1
- Initial release for Varnish 5 version 5.1.0.