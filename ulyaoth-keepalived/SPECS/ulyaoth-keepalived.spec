# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
%endif

Summary:    Keepalived a LVS driving daemon.
Name:       ulyaoth-keepalived
Version:    1.4.5
Release:    1%{?dist}
BuildArch: x86_64
License:    GPLv2
Group:      System Environment/Daemons
URL:        https://github.com/acassen/keepalived
Vendor:     Alexandre Cassen
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    https://github.com/acassen/keepalived/archive/v%{version}.tar.gz
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-keepalived/SOURCES/keepalived.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-keepalived/SOURCES/keepalived.service
BuildRoot:  %{_tmppath}/keepalived-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: net-snmp-devel
BuildRequires: libnl3-devel
BuildRequires: ipset-devel
BuildRequires: iptables-devel
BuildRequires: libnfnetlink-devel
BuildRequires: glib2-devel
BuildRequires: automake
BuildRequires: autoconf

Provides: ulyaoth-keepalived
Provides: keepalived

%description
The main goal of the keepalived project is to add a strong & robust keepalive facility to the Linux Virtual Server project.
It implements a multilayer TCP/IP stack checks. 
Keepalived implements a framework based on three family checks : Layer3, Layer4 & Layer5. 
This framework gives the daemon the ability of checking a LVS server pool states. Keepalived can be sumarize as a LVS driving daemon.
Keepalived implementation is based on an I/O multiplexer to handle a strong multi-threading framework. 
All the events process use this I/O multiplexer.

%prep
%setup -q -n keepalived-%{version}

%build
%{__rm} -rf $RPM_BUILD_ROOT
./configure --enable-sha1 --enable-snmp --enable-snmp-rfc --enable-dbus --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}

%install
%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor install
%{__rm} -rf %{buildroot}/%{_datarootdir}/doc/keepalived

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
    $RPM_BUILD_ROOT%{_unitdir}/keepalived.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE2 \
    $RPM_BUILD_ROOT%{_initrddir}/keepalived
%endif

%{__rm} -rf $RPM_BUILD_ROOT/etc/init/keepalived.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf %{_builddir}/*


%files
%defattr(-,root,root,-)
%dir /etc/keepalived
%dir /etc/keepalived/samples

/etc/dbus-1/system.d/org.keepalived.Vrrp1.conf
/etc/keepalived/keepalived.conf
/etc/keepalived/samples/*
/etc/sysconfig/keepalived
/usr/bin/genhash
/usr/sbin/keepalived
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Instance.xml
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Vrrp.xml
/usr/share/man/man1/genhash.1.gz
/usr/share/man/man5/keepalived.conf.5.gz
/usr/share/man/man8/keepalived.8.gz
/usr/share/snmp/mibs/KEEPALIVED-MIB.txt
/usr/share/snmp/mibs/VRRP-MIB.txt
/usr/share/snmp/mibs/VRRPv3-MIB.txt

%if %{use_systemd}
%{_unitdir}/keepalived.service
%else
%{_initrddir}/keepalived
%endif

%post
/sbin/ldconfig
# Register the keepalived service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset keepalived.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add keepalived
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-keepalived!

Please find the official documentation for keepalived here:
* https://github.com/acassen/keepalived

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable keepalived.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop keepalived.service >/dev/null 2>&1 ||:
%else
    /sbin/service keepalived stop > /dev/null 2>&1
    /sbin/chkconfig --del keepalived
%endif
fi

%postun
/sbin/ldconfig
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service keepalived status  >/dev/null 2>&1 || exit 0
    /sbin/service keepalived upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Wed Jun 13 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 1.4.5-1
- Updated Keepalived to 1.4.5.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.4.4-1
- Updated Keepalived to 1.4.4.

* Fri Jan 5 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.4.0-1
- Updated Keepalived to 1.4.0.

* Fri Nov 17 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.3.9-1
- Updated Keepalived to 1.3.9.

* Fri Apr 28 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.5-2
- Fixed init and systemd scripts.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.5-1
- Updated Keepalived to 1.3.5.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.4-1
- Initial release.