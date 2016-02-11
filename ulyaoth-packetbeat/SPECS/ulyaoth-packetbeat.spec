%define debug_package %{nil}
%define packetbeat_home /etc/packetbeat
%define packetbeat_group packetbeat
%define packetbeat_user packetbeat
%define packetbeat_loggroup adm

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
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Change the way you put your network packet data to work with Packetbeat.
Name:       ulyaoth-packetbeat
Version:    1.1.1
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.elastic.co/products/beats/packetbeat
Vendor:     Elasticsearch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    packetbeat
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-packetbeat/SOURCES/packetbeat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-packetbeat/SOURCES/packetbeat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-packetbeat/SOURCES/packetbeat.yml
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-packetbeat/SOURCES/packetbeat.template.json
BuildRoot:  %{_tmppath}/packetbeat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: libpcap

Provides: packetbeat
Provides: ulyaoth-packetbeat

%description
Change the way you put your network packet data to work with Packetbeat. 

%prep

%build

%install

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/packetbeat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/packetbeat
%endif

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/packetbeat
   
# install configuration file
%{__mkdir} -p $RPM_BUILD_ROOT/etc/packetbeat
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT/etc/packetbeat/packetbeat.yml
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT/etc/packetbeat/packetbeat.template.json
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/packetbeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/packetbeat
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{packetbeat_group} >/dev/null || groupadd -r %{packetbeat_group}
getent passwd %{packetbeat_user} >/dev/null || /usr/sbin/useradd --comment "Packetbeat Daemon User" --shell /bin/bash -M -r -g %{packetbeat_group} --home %{packetbeat_home} %{packetbeat_user}

%files
%defattr(-,%{packetbeat_user},%{packetbeat_group})
%dir /etc/packetbeat
%config(noreplace) /etc/packetbeat/packetbeat.yml
/etc/packetbeat/packetbeat.template.json
/usr/bin/packetbeat

%attr(0755,%{packetbeat_user},%{packetbeat_loggroup}) %dir %{_localstatedir}/log/packetbeat
%attr(0755,%{packetbeat_user},%{packetbeat_group}) %dir %{_localstatedir}/lib/packetbeat

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/packetbeat.service
%else
%{_initrddir}/packetbeat
%endif


%post
# Register the packetbeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset packetbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add packetbeat
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-packetbeat!

Please find the official documentation for packetbeat here:
* https://www.elastic.co/guide/en/beats/packetbeat/current/index.html

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable packetbeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop packetbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service packetbeat stop > /dev/null 2>&1
    /sbin/chkconfig --del packetbeat
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl packetbeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service packetbeat status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Fri Feb 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.1-1
- Updated Packetbeat to 1.1.1.

* Thu Feb 4 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-1
- Updated Packetbeat to 1.1.0.

* Sat Jan 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1-1
- Initial release.