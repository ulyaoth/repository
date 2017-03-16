# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

Summary:    Keepalived a LVS driving daemon.
Name:       ulyaoth-keepalived
Version:    1.3.4
Release:    1%{?dist}
BuildArch: x86_64
License:    GPLv2
Group:      System Environment/Daemons
URL:        https://github.com/acassen/keepalived
Vendor:     Alexandre Cassen
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/acassen/keepalived/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/keepalived-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: net-snmp-devel
BuildRequires: libnl3-devel
BuildRequires: ipset-devel
BuildRequires: iptables-devel
BuildRequires: libnfnetlink-devel
BuildRequires: glib2-devel

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
./configure --enable-sha1 --enable-snmp --enable-dbus --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}

%install
%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor install

%if %{use_systemd}
%else
sed -i 's|/usr/local/sbin/keepalived|/usr/sbin/keepalived|' $RPM_BUILD_ROOT/etc/init/keepalived.conf
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf %{_builddir}/*


%files
%defattr(-,root,root,-)
%dir /etc/keepalived
%dir /etc/keepalived/samples

/etc/dbus-1/system.d/org.keepalived.Vrrp1.conf
/etc/keepalived/keepalived.conf
/etc/keepalived/samples/client.pem
/etc/keepalived/samples/dh1024.pem
/etc/keepalived/samples/keepalived.conf.HTTP_GET.port
/etc/keepalived/samples/keepalived.conf.IPv6
/etc/keepalived/samples/keepalived.conf.SMTP_CHECK
/etc/keepalived/samples/keepalived.conf.SSL_GET
/etc/keepalived/samples/keepalived.conf.fwmark
/etc/keepalived/samples/keepalived.conf.inhibit
/etc/keepalived/samples/keepalived.conf.misc_check
/etc/keepalived/samples/keepalived.conf.misc_check_arg
/etc/keepalived/samples/keepalived.conf.quorum
/etc/keepalived/samples/keepalived.conf.sample
/etc/keepalived/samples/keepalived.conf.status_code
/etc/keepalived/samples/keepalived.conf.track_interface
/etc/keepalived/samples/keepalived.conf.virtual_server_group
/etc/keepalived/samples/keepalived.conf.virtualhost
/etc/keepalived/samples/keepalived.conf.vrrp
/etc/keepalived/samples/keepalived.conf.vrrp.localcheck
/etc/keepalived/samples/keepalived.conf.vrrp.lvs_syncd
/etc/keepalived/samples/keepalived.conf.vrrp.routes
/etc/keepalived/samples/keepalived.conf.vrrp.rules
/etc/keepalived/samples/keepalived.conf.vrrp.scripts
/etc/keepalived/samples/keepalived.conf.vrrp.static_ipaddress
/etc/keepalived/samples/keepalived.conf.vrrp.sync
/etc/keepalived/samples/root.pem
/etc/keepalived/samples/sample.misccheck.smbcheck.sh
/etc/sysconfig/keepalived
/usr/bin/genhash
/usr/sbin/keepalived
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Instance.xml
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Vrrp.xml
/usr/share/man/man1/genhash.1.gz
/usr/share/man/man5/keepalived.conf.5.gz
/usr/share/man/man8/keepalived.8.gz
/usr/share/snmp/mibs/KEEPALIVED-MIB.txt

%if %{use_systemd}
%{_unitdir}/keepalived.service
%else
/etc/init/keepalived.conf
%endif

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-keepalived

Please find the official documentation for keepalived here:
* http://www.keepalived.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Thu Mar 16 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.14-1
- Initial release.