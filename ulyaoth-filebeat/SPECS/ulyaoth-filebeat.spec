%define debug_package %{nil}
%define filebeat_home /etc/filebeat
%define filebeat_group filebeat
%define filebeat_user filebeat
%define filebeat_loggroup adm

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

Summary:    Filebeat is a log data shipper initially based on the Logstash-Forwarder source code.
Name:       ulyaoth-filebeat
Version:    1.2.1
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.elastic.co/products/beats/filebeat
Vendor:     Elasticsearch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    filebeat
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-filebeat/SOURCES/filebeat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-filebeat/SOURCES/filebeat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-filebeat/SOURCES/filebeat.yml
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-filebeat/SOURCES/filebeat.template.json
BuildRoot:  %{_tmppath}/filebeat-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: filebeat
Provides: ulyaoth-filebeat

%description
Filebeat is a lightweight, open source shipper for log file data. As the next-generation Logstash Forwarder, Filebeat tails logs and quickly sends this information to Logstash for further parsing and enrichment or to Elasticsearch for centralized storage and analysis.

%prep

%build

%install

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/filebeat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/filebeat
%endif

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/filebeat
   
# install configuration file
%{__mkdir} -p $RPM_BUILD_ROOT/etc/filebeat
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT/etc/filebeat/filebeat.yml
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT/etc/filebeat/filebeat.template.json
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/filebeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/filebeat
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{filebeat_group} >/dev/null || groupadd -r %{filebeat_group}
getent passwd %{filebeat_user} >/dev/null || /usr/sbin/useradd --comment "Filebeat Daemon User" --shell /bin/bash -M -r -g %{filebeat_group} --home %{filebeat_home} %{filebeat_user}

%files
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


%post
# Register the filebeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset filebeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add filebeat
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-filebeat!

Please find the official documentation for filebeat here:
* https://www.elastic.co/guide/en/beats/filebeat/current/index.html

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable filebeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop filebeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service filebeat stop > /dev/null 2>&1
    /sbin/chkconfig --del filebeat
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl filebeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service filebeat status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sat Apr 9 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.1-1
- Updated Filebeat to 1.2.1.

* Wed Mar 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.0-1
- Updated Filebeat to 1.2.0.

* Mon Mar 28 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.2-1
- Updated Filebeat to 1.1.2.

* Fri Feb 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.1-1
- Updated Filebeat to 1.1.1.

* Thu Feb 4 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-1
- Updated Filebeat to 1.1.0.

* Sat Jan 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1-1
- Initial release.