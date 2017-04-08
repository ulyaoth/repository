%define debug_package %{nil}
%define filebeat_home /etc/filebeat
%define filebeat_group filebeat
%define filebeat_user filebeat
%define filebeat_loggroup adm
%define metricbeat_home /etc/metricbeat
%define metricbeat_group metricbeat
%define metricbeat_user metricbeat
%define metricbeat_loggroup adm
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

Name:       ulyaoth
Summary:    Beats is the platform for building lightweight, open source data shippers.
Version:    5.0.0
Release:    1%{?dist}
BuildArch:  x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.elastic.co/products/beats
Vendor:     Elasticsearch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    filebeat
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/filebeat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/filebeat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/filebeat.yml
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/filebeat.template.json
Source5:    packetbeat
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/packetbeat.service
Source7:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/packetbeat.init
Source8:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/packetbeat.yml
Source9:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/packetbeat.template.json
Source10:   metricbeat
Source11:   https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/metricbeat.service
Source12:   https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/metricbeat.init
Source13:   https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/metricbeat.yml
Source14:   https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/SOURCES/metricbeat.template.json
BuildRoot:  %{_tmppath}/beats-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Beats is the platform for building lightweight, open source data shippers for many types of data you want to enrich with Logstash, search and analyze in Elasticsearch, and visualize in Kibana. Whether you’re interested in log files, infrastructure metrics, or network packets, Beats serves as the foundation for keeping a beat on your data.

%package filebeat
Version: %{version}
Release: %{release}
License: %{license}
Group: %{group}
URL: %{url}
Vendor: %{vendor}
Packager: %{packager}
Summary: Filebeat is a log data shipper initially based on the Logstash-Forwarder source code.
Provides: filebeat
Provides: ulyaoth-filebeat
%description filebeat
Filebeat is a lightweight, open source shipper for log file data. As the next-generation Logstash Forwarder, Filebeat tails logs and quickly sends this information to Logstash for further parsing and enrichment or to Elasticsearch for centralized storage and analysis.

%package packetbeat
Version: %{version}
Release: %{release}
License: %{license}
Group: %{group}
URL: %{url}
Vendor: %{vendor}
Packager: %{packager}
Summary: Change the way you put your network packet data to work with Packetbeat.
BuildRequires: libpcap-devel
Requires: libpcap
Provides: packetbeat
Provides: ulyaoth-packetbeat
%description packetbeat
Change the way you put your network packet data to work with Packetbeat.

%package metricbeat
Version: %{version}
Release: %{release}
License: %{license}
Group: %{group}
URL: %{url}
Vendor: %{vendor}
Packager: %{packager}
Summary: Metricbeat is a lightweight way to gather CPU, memory, and other per-process and system wide data, then ship it to Elasticsearch to analyze the results.
Provides: metricbeat
Provides: ulyaoth-metricbeat
%description metricbeat
Looking for a better way to understand how your server resources are used? The best place to start is your infrastructure metrics. Metricbeat is a lightweight way to gather CPU, memory, and other per-process and system wide data, then ship it to Elasticsearch to analyze the results.

%prep

%build

%install

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/filebeat.service
%{__install} -m644 %SOURCE6 \
        $RPM_BUILD_ROOT%{_unitdir}/packetbeat.service
%{__install} -m644 %SOURCE11 \
        $RPM_BUILD_ROOT%{_unitdir}/metricbeat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/filebeat
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/packetbeat
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/metricbeat
%endif

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/filebeat
%{__install} -m 755 -p %{SOURCE5} \
   $RPM_BUILD_ROOT/usr/bin/packetbeat
%{__install} -m 755 -p %{SOURCE10} \
   $RPM_BUILD_ROOT/usr/bin/metricbeat

# install configuration file
%{__mkdir} -p $RPM_BUILD_ROOT/etc/filebeat
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT/etc/filebeat/filebeat.yml
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT/etc/filebeat/filebeat.template.json

%{__mkdir} -p $RPM_BUILD_ROOT/etc/packetbeat
%{__install} -m 644 -p %{SOURCE8} \
   $RPM_BUILD_ROOT/etc/packetbeat/packetbeat.yml
%{__install} -m 644 -p %{SOURCE9} \
   $RPM_BUILD_ROOT/etc/packetbeat/packetbeat.template.json

%{__mkdir} -p $RPM_BUILD_ROOT/etc/metricbeat
%{__install} -m 644 -p %{SOURCE13} \
   $RPM_BUILD_ROOT/etc/metricbeat/metricbeat.yml
%{__install} -m 644 -p %{SOURCE14} \
   $RPM_BUILD_ROOT/etc/metricbeat/metricbeat.template.json

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/filebeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/filebeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/packetbeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/packetbeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/metricbeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/metricbeat

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
%pre filebeat
getent group %{filebeat_group} >/dev/null || groupadd -r %{filebeat_group}
getent passwd %{filebeat_user} >/dev/null || /usr/sbin/useradd --comment "Filebeat Daemon User" --shell /bin/bash -M -r -g %{filebeat_group} --home %{filebeat_home} %{filebeat_user}

%pre packetbeat
getent group %{packetbeat_group} >/dev/null || groupadd -r %{packetbeat_group}
getent passwd %{packetbeat_user} >/dev/null || /usr/sbin/useradd --comment "Packetbeat Daemon User" --shell /bin/bash -M -r -g %{packetbeat_group} --home %{packetbeat_home} %{packetbeat_user}

%pre metricbeat
getent group %{metricbeat_group} >/dev/null || groupadd -r %{metricbeat_group}
getent passwd %{metricbeat_user} >/dev/null || /usr/sbin/useradd --comment "Metricbeat Daemon User" --shell /bin/bash -M -r -g %{metricbeat_group} --home %{metricbeat_home} %{metricbeat_user}

%files
%files filebeat
%defattr(-,%{filebeat_user},%{filebeat_group})
%dir /etc/filebeat
%config(noreplace) /etc/filebeat/filebeat.yml
/etc/filebeat/filebeat.template.json
/usr/bin/filebeat

%attr(0755,%{filebeat_user},%{filebeat_loggroup}) %dir %{_localstatedir}/log/filebeat
%attr(0755,%{filebeat_user},%{filebeat_group}) %dir %{_localstatedir}/lib/filebeat

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/filebeat.service
%else
%{_initrddir}/filebeat
%endif

%files packetbeat
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

%files metricbeat
%defattr(-,%{metricbeat_user},%{metricbeat_group})
%dir /etc/metricbeat
%config(noreplace) /etc/metricbeat/metricbeat.yml
/etc/metricbeat/metricbeat.template.json
/usr/bin/metricbeat

%attr(0755,%{metricbeat_user},%{metricbeat_loggroup}) %dir %{_localstatedir}/log/metricbeat
%attr(0755,%{metricbeat_user},%{metricbeat_group}) %dir %{_localstatedir}/lib/metricbeat

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/metricbeat.service
%else
%{_initrddir}/metricbeat
%endif

%post 
%post filebeat
# Register the filebeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset filebeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add filebeat
%endif
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-filebeat!

Please find the official documentation for filebeat here:
* https://www.elastic.co/guide/en/beats/filebeat/current/index.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%post packetbeat
# Register the packetbeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset packetbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add packetbeat
%endif
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-packetbeat!

Please find the official documentation for packetbeat here:
* https://www.elastic.co/guide/en/beats/packetbeat/current/index.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%post metricbeat
# Register the metricbeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset metricbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add metricbeat
%endif
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-metricbeat!

Please find the official documentation for metricbeat here:
* https://www.elastic.co/guide/en/beats/metricbeat/current/index.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
%preun filebeat
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable filebeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop filebeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service filebeat stop > /dev/null 2>&1
    /sbin/chkconfig --del filebeat
%endif
fi

%preun packetbeat
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable packetbeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop packetbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service packetbeat stop > /dev/null 2>&1
    /sbin/chkconfig --del packetbeat
%endif
fi

%preun metricbeat
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable metricbeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop metricbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service metricbeat stop > /dev/null 2>&1
    /sbin/chkconfig --del metricbeat
%endif
fi

%postun
%postun filebeat
%if %use_systemd
/usr/bin/systemctl filebeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service filebeat status  >/dev/null 2>&1 || exit 0
fi

%postun packetbeat
%if %use_systemd
/usr/bin/systemctl packetbeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service packetbeat status  >/dev/null 2>&1 || exit 0
fi

%postun metricbeat
%if %use_systemd
/usr/bin/systemctl metricbeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service metricbeat status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sat Oct 29 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.0-1
- Updated Beats to 5.0.0.

* Fri Sep 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.1-1
- Updated Beats to 1.3.1.

* Sun Sep 4 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.0-1
- Updated Beats to 1.3.0.