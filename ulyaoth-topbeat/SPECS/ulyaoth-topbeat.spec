%define debug_package %{nil}
%define topbeat_home /etc/topbeat
%define topbeat_group topbeat
%define topbeat_user topbeat
%define topbeat_loggroup adm

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

Summary:    Topbeat is a lightweight way to gather CPU, memory, and other per-process and system wide data, then ship it to Elasticsearch to analyze the results.
Name:       ulyaoth-topbeat
Version:    1.1.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.elastic.co/products/beats/topbeat
Vendor:     Elasticsearch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    topbeat
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-topbeat/SOURCES/topbeat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-topbeat/SOURCES/topbeat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-topbeat/SOURCES/topbeat.yml
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-topbeat/SOURCES/topbeat.template.json
BuildRoot:  %{_tmppath}/topbeat-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: topbeat
Provides: ulyaoth-topbeat

%description
Looking for a better way to understand how your server resources are used? The best place to start is your infrastructure metrics. Topbeat is a lightweight way to gather CPU, memory, and other per-process and system wide data, then ship it to Elasticsearch to analyze the results.

%prep

%build

%install

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/topbeat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/topbeat
%endif

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/topbeat
   
# install configuration file
%{__mkdir} -p $RPM_BUILD_ROOT/etc/topbeat
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT/etc/topbeat/topbeat.yml
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT/etc/topbeat/topbeat.template.json
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/topbeat
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/topbeat
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{topbeat_group} >/dev/null || groupadd -r %{topbeat_group}
getent passwd %{topbeat_user} >/dev/null || /usr/sbin/useradd --comment "Topbeat Daemon User" --shell /bin/bash -M -r -g %{topbeat_group} --home %{topbeat_home} %{topbeat_user}

%files
%defattr(-,%{topbeat_user},%{topbeat_group})
%dir /etc/topbeat
%config(noreplace) /etc/topbeat/topbeat.yml
/etc/topbeat/topbeat.template.json
/usr/bin/topbeat

%attr(0755,%{topbeat_user},%{topbeat_loggroup}) %dir %{_localstatedir}/log/topbeat
%attr(0755,%{topbeat_user},%{topbeat_group}) %dir %{_localstatedir}/lib/topbeat

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/topbeat.service
%else
%{_initrddir}/topbeat
%endif


%post
# Register the topbeat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset topbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add topbeat
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-topbeat!

Please find the official documentation for topbeat here:
* https://www.elastic.co/guide/en/beats/topbeat/current/index.html

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable topbeat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop topbeat.service >/dev/null 2>&1 ||:
%else
    /sbin/service topbeat stop > /dev/null 2>&1
    /sbin/chkconfig --del topbeat
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl topbeat >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service topbeat status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Thu Feb 4 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-1
- Updated to Topbeat 1.1.0.

* Sat Jan 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1-1
- Initial release.