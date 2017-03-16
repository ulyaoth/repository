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
./configure --prefix=/usr/ --enable-sha1 --enable-snmp --enable-dbus
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf %{_builddir}/*


%files
%defattr(-,root,root,-)

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