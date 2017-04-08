
%define __jar_repack %{nil}
%define debug_package %{nil}
%define solr_home /opt/solr
%define solr_group solr
%define solr_user solr

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

Summary:    Apache Solr
Name:       ulyaoth-solr5
Version:    5.5.4
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://lucene.apache.org/solr/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    solr-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr-log4j.properties
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr-solr.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr5-solr.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr.logrotate
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr5-solr.in.sh
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/SOURCES/solr.conf
BuildRoot:  %{_tmppath}/solr-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: solr
Provides: solr5
Provides: ulyaoth-solr
Provides: ulyaoth-solr5

Requires: lsof

Conflicts: ulyaoth-solr4
Conflicts: ulyaoth-solr6

%description
Solr is highly reliable, scalable and fault tolerant, providing distributed indexing, replication and load-balanced querying, automated failover and recovery, centralized configuration and more.

%prep
%setup -q -n solr-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{solr_home}/
cp -R * %{buildroot}/%{solr_home}/

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/solr/data/
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/solr/
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/solr/
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/default
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d

%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{solr_home}/server/resources/log4j.properties

%{__install} -m 755 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{solr_home}/bin/solr.in.sh
   
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT/etc/tmpfiles.d/solr.conf

cp -R %{buildroot}/%{solr_home}/server/solr/solr.xml $RPM_BUILD_ROOT%{_localstatedir}/solr/data/
cp -R %{buildroot}/%{solr_home}/bin/solr.in.sh $RPM_BUILD_ROOT%{_sysconfdir}/default

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/solr.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/solr
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/solr

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{solr_group} >/dev/null || groupadd -r %{solr_group}
getent passwd %{solr_user} >/dev/null || /usr/sbin/useradd --comment "Solr Daemon User" --shell /bin/bash -M -r -g %{solr_group} --home %{solr_home} %{solr_user}

%files
%defattr(-,%{solr_user},%{solr_group})
%{solr_home}/*
%dir %{solr_home}
%dir %{_localstatedir}/log/solr
%dir %{_localstatedir}/solr/data
%dir %{_localstatedir}/solr/
%dir %{_localstatedir}/run/solr/
%config(noreplace) %{solr_home}/server/resources/log4j.properties
%config(noreplace) %{solr_home}/server/contexts/solr-jetty-context.xml
%config(noreplace) %{solr_home}/server/etc/jetty-https-ssl.xml
%config(noreplace) %{solr_home}/server/etc/jetty.xml
%config(noreplace) %{solr_home}/server/etc/webdefault.xml
%config(noreplace) %{solr_home}/server/solr/solr.xml
%config(noreplace) %{solr_home}/server/solr/zoo.cfg
%config(noreplace) %{_localstatedir}/solr/data/solr.xml
%config(noreplace) %{_sysconfdir}/default/solr.in.sh

%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/solr
%config(noreplace) %{_sysconfdir}/tmpfiles.d/solr.conf
%if %{use_systemd}
%{_unitdir}/solr.service
%else
%{_initrddir}/solr
%endif


%post
# Register the solr service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset solr.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add solr
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-solr5!

Please find the official documentation for solr here:
* https://lucene.apache.org/solr/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable solr.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop solr.service >/dev/null 2>&1 ||:
%else
    /sbin/service solr stop > /dev/null 2>&1
    /sbin/chkconfig --del solr
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service solr status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Wed Feb 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.4-1
- Updated to Solr 5.5.4.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.3-1
- Updated to Solr 5.5.3.

* Sat Jul 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.2-1
- Updated to Solr 5.5.2.

* Fri May 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.1-1
- Updated to Solr 5.5.1.

* Sat Feb 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.0-1
- Updated to Solr 5.5.0.

* Sun Jan 24 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.4.1-1
- Updated to Solr 5.4.1.

* Thu Jan 21 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.4.0-2
- Fixed init.d script, taken from ShimiTaNaka on github.
- Added solr.in.sh to /var/solr.
- Added pid filr to /var/run/solr.
- Added tpmfiles.d with solr config for /var/run/solr permissions.
- This release fixes: https://www.ulyaoth.net/threads/patch-for-solr-5-4-0-for-rhel-6-x86_64-startup-script.96095/ & github issue #274.

* Tue Dec 29 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.4.0-1
- Updated to Solr 5.4.0.

* Sun Oct 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.1-1
- Updated to Solr 5.3.1.

* Sun Aug 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.0-1
- Updated to Solr 5.3.0.

* Mon Jun 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.2.1-1
- Updated to Solr 5.2.1.

* Tue Jun 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.2.0-1
- Updated to Solr 5.2.0.

* Thu Apr 16 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.1.0-1
- Updated to Solr 5.1.0.

* Sat Mar 21 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.0-1
- Initial release.
