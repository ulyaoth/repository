%define debug_package %{nil}
%define lforward_home /opt/logstash-forwarder
%define lforward_group logstash-forwarder
%define lforward_user logstash-forwarder

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

Summary:    Logstash Forwarder is a tool to collect logs locally in preparation for processing elsewhere!
Name:       ulyaoth-logstash-forwarder
Version:    0.4.0
Release:    2%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://github.com/elasticsearch/logstash-forwarder
Vendor:     Elasticsearch BV
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
Source0:    logstash-forwarder
Source1:    https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-logstash-forwarder/SOURCES/logstash-forwarder.service
Source2:    https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-logstash-forwarder/SOURCES/logstash-forwarder.init
Source3:    https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-logstash-forwarder/SOURCES/logstash-forwarder.conf
BuildRoot:  %{_tmppath}/logstash-forwarder-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: logstash-forwarder
Provides: lumberjack
Provides: ulyaoth-logstash-forwarder
Provides: ulyaoth-lumberjack

%description
♫ I'm a lumberjack and I'm ok! I sleep when idle, then I ship logs all day! I parse your logs, I eat the JVM agent for lunch! ♫
(This project was recently renamed from 'lumberjack' to 'logstash-forwarder' to make its intended use clear. The 'lumberjack' name now remains as the network protocol, and 'logstash-forwarder' is the name of the program. It's still the same lovely log forwarding program you love.)
Logstash Forwarder is s tool to collect logs locally in preparation for processing elsewhere!

%prep

%build

%install
install -d -m 755 %{buildroot}/%{lforward_home}/
%{__mkdir} -p $RPM_BUILD_ROOT/opt/logstash-forwarder/ssl

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/logstash-forwarder.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/logstash-forwarder
%endif

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/opt/logstash-forwarder/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/opt/logstash-forwarder/bin/logstash-forwarder
   
# install configuration file
%{__mkdir} -p $RPM_BUILD_ROOT/opt/logstash-forwarder/conf
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT/opt/logstash-forwarder/conf/logstash-forwarder.conf
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/logstash-forwarder
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{lforward_group} >/dev/null || groupadd -r %{lforward_group}
getent passwd %{lforward_user} >/dev/null || /usr/sbin/useradd --comment "Logstash Forwarder Daemon User" --shell /bin/bash -M -r -g %{lforward_group} --home %{lforward_home} %{lforward_user}

%files
%defattr(-,%{lforward_user},%{lforward_group})
%{lforward_home}
%{lforward_home}/*
%config(noreplace) %{lforward_home}/conf/logstash-forwarder.conf
%attr(0755,logstash-forwarder,root) %dir %{_localstatedir}/log/logstash-forwarder

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/logstash-forwarder.service
%else
%{_initrddir}/logstash-forwarder
%endif


%post
# Register the logstash-forwarder service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset logstash-forwarder.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add logstash-forwarder
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-logstash-forwarder!

Please find the official documentation for logstash-forwarder here:
* https://github.com/elasticsearch/logstash-forwarder

For any additional help please visit my forum at:
* https://community.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable logstash-forwarder.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop logstash-forwarder.service >/dev/null 2>&1 ||:
%else
    /sbin/service logstash-forwarder stop > /dev/null 2>&1
    /sbin/chkconfig --del logstash-forwarder
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service logstash-forwarder status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Thu Jul 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.4.0-2
- Fix to systemd script to use correct user: logstash-forwarder.

* Tue Jul 7 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.4.0-1
- Creating Stable version from official released "tar.gz" file.
- Thank you Fred Emmott.