%define varnish5_user varnish5
%define varnish5_group varnish5
%define varnish5_loggroup adm
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
Name:       ulyaoth-varnish5
Version:    5.0.0
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD
Group:      System Environment/Daemons
URL:        https://varnish-cache.org
Vendor:     Varnish Software AS
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/varnishcache/varnish-cache/archive/varnish-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/default.vlc
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5.service
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5log.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5ncsa.service
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5.initrc
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5.initrc
Source7:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5.initrc
Source8:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish5-environment
Source9:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/ulyaoth-varnish5.conf
Source10:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/varnish_reload_vcl
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

Provides: varnish5
Provides: ulyaoth-varnish5

%description
Varnish is an HTTP accelerator designed for content-heavy dynamic web sites as well as heavily consumed APIs.

%prep
%setup -q -n varnish-%{version}

%build
cd %_builddir/varnish-cache-varnish-5.0.0
./autogen.sh
./configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5
mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/examples
mkdir -p $RPM_BUILD_ROOT/usr/sbin

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr/local/ulyaoth/varnish/varnish5 install

%{__install} -m 644 -p %{SOURCE10} \
    $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/sbin/varnish_reload_vcl

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/share/man $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/
mv $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/share/doc $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/
mv $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/share/aclocal $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/
mv $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/share/varnish/* $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/examples/
mv $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/doc/varnish/* $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/examples/vcl/
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/share
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/var
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/varnish/varnish5/doc

%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE9} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-varnish5.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/varnish5
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/varnish5/default.vcl

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE8} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/varnish5
	
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/varnish5
	
ln -s /usr/local/ulyaoth/varnish/varnish5/sbin/varnishd $RPM_BUILD_ROOT/usr/sbin/varnish5d
ln -s /usr/local/ulyaoth/varnish/varnish5/sbin/varnish_reload_vcl $RPM_BUILD_ROOT/usr/sbin/varnish5_reload_vcl
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishadm $RPM_BUILD_ROOT/usr/bin/varnish5adm
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishhist $RPM_BUILD_ROOT/usr/bin/varnish5hist
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishlog $RPM_BUILD_ROOT/usr/bin/varnish5log
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishncsa $RPM_BUILD_ROOT/usr/bin/varnish5ncsa
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishstat $RPM_BUILD_ROOT/usr/bin/varnish5stat
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishtest $RPM_BUILD_ROOT/usr/bin/varnish5test
ln -s /usr/local/ulyaoth/varnish/varnish5/bin/varnishtop $RPM_BUILD_ROOT/usr/bin/varnish5top

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE2 \
    $RPM_BUILD_ROOT%{_unitdir}/varnish5.service
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/varnish5log.service
%{__install} -m644 %SOURCE4 \
    $RPM_BUILD_ROOT%{_unitdir}/varnish5ncsa.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE5 \
    $RPM_BUILD_ROOT%{_initrddir}/varnish5
%{__install} -m755 %SOURCE6 \
    $RPM_BUILD_ROOT%{_initrddir}/varnish5log
%{__install} -m755 %SOURCE7 \
    $RPM_BUILD_ROOT%{_initrddir}/varnish5ncsa
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
# Add the "varnish5" user
getent group %{varnish5_group} >/dev/null || groupadd -r %{varnish5_group}
getent passwd %{varnish5_user} >/dev/null || \
    useradd -r -g %{vanrish5_group} -s /sbin/nologin \
    -d %{varnish5_home} -c "varnish5 user"  %{varnish5_user}
exit 0

%files
%defattr(-,root,root,-)
/usr/sbin/varnish5d
/usr/sbin/varnish5_reload_vcl
/usr/bin/varnish5adm
/usr/bin/varnish5hist
/usr/bin/varnish5log
/usr/bin/varnish5ncsa
/usr/bin/varnish5stat
/usr/bin/varnish5test
/usr/bin/varnish5top

%attr(0755,root,root) %dir %{_localstatedir}/log/varnish5

%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/varnish
%dir /usr/local/ulyaoth/varnish/varnish5

%dir %{_sysconfdir}/varnish5
%config(noreplace) %{_sysconfdir}/varnish5/default.vcl

%dir /usr/local/ulyaoth/varnish/varnish5/sbin
/usr/local/ulyaoth/varnish/varnish5/sbin/varnishd
/usr/local/ulyaoth/varnish/varnish5/sbin/varnish_reload_vcl

%dir /usr/local/ulyaoth/varnish/varnish5/bin
/usr/local/ulyaoth/varnish/varnish5/bin/varnishadm
/usr/local/ulyaoth/varnish/varnish5/bin/varnishhist
/usr/local/ulyaoth/varnish/varnish5/bin/varnishlog
/usr/local/ulyaoth/varnish/varnish5/bin/varnishncsa
/usr/local/ulyaoth/varnish/varnish5/bin/varnishstat
/usr/local/ulyaoth/varnish/varnish5/bin/varnishtest
/usr/local/ulyaoth/varnish/varnish5/bin/varnishtop

%dir /usr/local/ulyaoth/varnish/varnish5/aclocal
/usr/local/ulyaoth/varnish/varnish5/aclocal/varnish-legacy.m4
/usr/local/ulyaoth/varnish/varnish5/aclocal/varnish.m4

%dir /usr/local/ulyaoth/varnish/varnish5/examples
/usr/local/ulyaoth/varnish/varnish5/examples/vmodtool.py

%dir /usr/local/ulyaoth/varnish/varnish5/examples/vcl
/usr/local/ulyaoth/varnish/varnish5/examples/vcl/builtin.vcl
/usr/local/ulyaoth/varnish/varnish5/examples/vcl/example.vcl
/usr/local/ulyaoth/varnish/varnish5/examples/vcl/devicedetect.vcl

%dir /usr/local/ulyaoth/varnish/varnish5/man
%dir /usr/local/ulyaoth/varnish/varnish5/man/man1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishadm.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishd.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishhist.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishlog.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishncsa.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishstat.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishtest.1
/usr/local/ulyaoth/varnish/varnish5/man/man1/varnishtop.1

%dir /usr/local/ulyaoth/varnish/varnish5/man/man3
/usr/local/ulyaoth/varnish/varnish5/man/man3/vmod_directors.3
/usr/local/ulyaoth/varnish/varnish5/man/man3/vmod_std.3

%dir /usr/local/ulyaoth/varnish/varnish5/man/man7
/usr/local/ulyaoth/varnish/varnish5/man/man7/varnish-cli.7
/usr/local/ulyaoth/varnish/varnish5/man/man7/varnish-counters.7
/usr/local/ulyaoth/varnish/varnish5/man/man7/vcl.7
/usr/local/ulyaoth/varnish/varnish5/man/man7/vsl.7
/usr/local/ulyaoth/varnish/varnish5/man/man7/vsl-query.7
/usr/local/ulyaoth/varnish/varnish5/man/man7/vtc.7

%dir /usr/local/ulyaoth/varnish/varnish5/include
%dir /usr/local/ulyaoth/varnish/varnish5/include/varnish
/usr/local/ulyaoth/varnish/varnish5/include/varnish/*

%dir /usr/local/ulyaoth/varnish/varnish5/lib
/usr/local/ulyaoth/varnish/varnish5/lib/libvarnishapi.la
/usr/local/ulyaoth/varnish/varnish5/lib/libvarnishapi.so
/usr/local/ulyaoth/varnish/varnish5/lib/libvarnishapi.so.1
/usr/local/ulyaoth/varnish/varnish5/lib/libvarnishapi.so.1.0.4

%dir /usr/local/ulyaoth/varnish/varnish5/lib/pkgconfig
/usr/local/ulyaoth/varnish/varnish5/lib/pkgconfig/varnishapi.pc

%dir /usr/local/ulyaoth/varnish/varnish5/lib/varnish
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvarnishcompat.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvarnishcompat.so
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvarnish.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvarnish.so
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvcc.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvcc.so
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvgz.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/libvgz.so

%dir /usr/local/ulyaoth/varnish/varnish5/lib/varnish/vmods
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/vmods/libvmod_directors.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/vmods/libvmod_directors.so
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/vmods/libvmod_std.la
/usr/local/ulyaoth/varnish/varnish5/lib/varnish/vmods/libvmod_std.so

%if %{use_systemd}
%{_unitdir}/varnish5.service
%{_unitdir}/varnish5ncsa.service
%{_unitdir}/varnish5log.service
%else
%{_initrddir}/varnish5
%{_initrddir}/varnish5ncsa
%{_initrddir}/varnish5log
%endif

%post
/sbin/ldconfig
dd if=/dev/random of=/etc/varnish5/secret count=1
# Register the varnish5 service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset varnish5.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add varnish5
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-varnish5!

Please find the official documentation for HAProxy here:
* https://www.varnish-cache.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/varnish5 ]; then
        if [ ! -e %{_localstatedir}/log/varnish5/varnish.log ]; then
            touch %{_localstatedir}/log/varnish5/varnish.log
            %{__chmod} 640 %{_localstatedir}/log/varnish/varnish.log
            %{__chown} varnish5:%{varnish5_loggroup} %{_localstatedir}/log/varnish/varnish.log
        fi

        if [ ! -e %{_localstatedir}/log/varnish5/varnishncsa.log ]; then
            touch %{_localstatedir}/log/varnish5/varnishncsa.log
            %{__chmod} 640 %{_localstatedir}/log/varnish5/varnishncsa.log
            %{__chown} varnish5:%{varnish5_loggroup} %{_localstatedir}/log/varnish5/varnishncsa.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable varnish5.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop varnish5.service >/dev/null 2>&1 ||:
%else
    /sbin/service varnish5 stop > /dev/null 2>&1
    /sbin/chkconfig --del haproxy1.6
%endif
fi

%postun
/sbin/ldconfig
rm -rf /etc/varnish5/secret
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service varnish5 status  >/dev/null 2>&1 || exit 0
    /sbin/service varnish5 upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.0-1
- Initial release for Varnish 5 version 5.0.0.