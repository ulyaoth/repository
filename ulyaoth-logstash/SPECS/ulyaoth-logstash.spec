
%define __jar_repack %{nil}
%define debug_package %{nil}
%define logstash_home /var/lib/logstash
%define logstash_group logstash
%define logstash_user logstash
%define logstash_loggroup adm

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
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Logstash
Name:       ulyaoth-logstash
Version:    2.1.1
Release:    1%{?dist}
BuildArch: x86_64
License:    ASL 2.0
Group:      System Environment/Daemons
URL:        https://www.elastic.co/products/logstash
Vendor:     Elasticsearch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    logstash-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/SOURCES/logstash.conf
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/SOURCES/logstash.sysconfig
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/SOURCES/logstash.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/SOURCES/logstash.init
BuildRoot:  %{_tmppath}/logstash-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: logstash
provides: ulyaoth-logstash

%description
Logstash is an open source tool for collecting, parsing, and storing logs for future use.

%prep
%setup -q -n logstash-%{version}

%build

%install
install -d -m 755 %{buildroot}/opt/logstash/
cp -R * %{buildroot}/opt/logstash/

%{__mkdir} -p $RPM_BUILD_ROOT/var/log/logstash
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/logstash
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logstash

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logstash/logstash.conf
%{__install} -m 644 -p %{SOURCE2} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/logstash

%if %{use_systemd}
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/logstash.service
%else
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE4} \
   $RPM_BUILD_ROOT%{_initrddir}/logstash
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /opt/logstash
/opt/logstash/*

%attr(0755,logstash,logstash) %config(noreplace) %{_sysconfdir}/logstash/logstash.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/logstash
%attr(0755,logstash,logstash) %dir %{_localstatedir}/lib/logstash
%attr(0755,logstash,adm) %dir %{_localstatedir}/log/logstash
%attr(0755,logstash,logstash) %dir %{_sysconfdir}/logstash

%if %{use_systemd}
%{_unitdir}/logstash.service
%else
%{_initrddir}/logstash
%endif

%pre
# Add the "logstash" user
getent group %{logstash_group} >/dev/null || groupadd -r %{logstash_group}
getent passwd %{logstash_user} >/dev/null || \
    useradd -r -g %{logstash_group} -s /sbin/nologin \
    -d %{logstash_home} -c "logstash user"  %{logstash_user}
exit 0

%post
# Register the logstash service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset logstash.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add logstash
%endif
    # print site info
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-logstash!

Please find the official documentation for logstash here:
* https://www.elastic.co/products/logstash

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/logstash ]; then
        if [ ! -e %{_localstatedir}/log/logstash/logstash.log ]; then
		    touch %{_localstatedir}/log/logstash/logstash.log
            %{__chmod} 644 %{_localstatedir}/log/logstash/logstash.log
            %{__chown} logstash:%{logstash_loggroup} %{_localstatedir}/log/logstash/logstash.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable logstash.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop logstash.service >/dev/null 2>&1 ||:
%else
    /sbin/service logstash stop > /dev/null 2>&1
    /sbin/chkconfig --del logstash
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif

%changelog
* Fri Jan 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.1.1-1
- Initial Release.
- System script based on: https://github.com/guardian/machine-images/blob/master/packer/resources/features/elk-stack/systemd-logstash.service