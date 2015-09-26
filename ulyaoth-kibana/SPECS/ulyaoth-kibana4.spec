
%global __os_install_post %{nil}

%define __jar_repack %{nil}
%define debug_package %{nil}
%define kibana_home /opt/kibana
%define kibana_group kibana
%define kibana_user kibana

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

Summary:    Kibana explore and visualize your data
Name:       ulyaoth-kibana4
Version:    4.1.2
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://www.elasticsearch.org/overview/kibana/
Vendor:     Elasticsearch BV
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

%ifarch x86_64
Source0:    kibana-%{version}-linux-x64.tar.gz
%endif

%ifarch i386
Source0:    kibana-%{version}-linux-x86.tar.gz
%endif

%ifarch i686
Source0:    kibana-%{version}-linux-x86.tar.gz
%endif

Source1:    kibana.service
Source2:    kibana.init
BuildRoot:  %{_tmppath}/kibana-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: kibana
Provides: kibana4
Provides: ulyaoth-kibana
Provides: ulyaoth-kibana4

%description
Kibana is an open source (Apache Licensed), browser based analytics and search dashboard for Elasticsearch. Kibana is a snap to setup and start using. Kibana strives to be easy to get started with, while also being flexible and powerful, just like Elasticsearch.

%prep
%ifarch x86_64
%setup -q -n kibana-%{version}-linux-x64
%endif

%ifarch i386
%setup -q -n kibana-%{version}-linux-x86
%endif

%ifarch i686
%setup -q -n kibana-%{version}-linux-x86
%endif


%build

%install
install -d -m 755 %{buildroot}/%{kibana_home}/
cp -R * %{buildroot}/%{kibana_home}/

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/kibana.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/kibana
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{kibana_group} >/dev/null || groupadd -r %{kibana_group}
getent passwd %{kibana_user} >/dev/null || /usr/sbin/useradd --comment "Kibana Daemon User" --shell /bin/bash -M -r -g %{kibana_group} --home %{kibana_home} %{kibana_user}

%files
%defattr(-,%{kibana_user},%{kibana_group})
%{kibana_home}/*
%dir %{kibana_home}
%config(noreplace) %{kibana_home}/config/kibana.yml

%defattr(-,root,root)
%if %{use_systemd}
%{_unitdir}/kibana.service
%else
%{_initrddir}/kibana
%endif


%post
# Register the kibana service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset kibana.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add kibana
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-kibana4!

Please find the official documentation for kibana here:
* http://www.elasticsearch.org/overview/kibana/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable kibana.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop kibana.service >/dev/null 2>&1 ||:
%else
    /sbin/service kibana stop > /dev/null 2>&1
    /sbin/chkconfig --del kibana
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service kibana status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sun Sep 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 4.1.2-1
- Updating to Kibana 4.1.2.

* Mon Jul 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.1.1-1
- Updating to Kibana 4.1.1.

* Sun Jun 21 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.1.0-1
- Updating to Kibana 4.1.0.

* Fri Apr 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.0.2-1
- Updating to Kibana 4.0.2.
- Fixed 32-bit support.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.0.1-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.0.1-2
- Support for Fedora 22 and CentOS 6 & 7.
- i386 support.
- Cleaned spec file slightly to remove double things.

* Sun Mar 08 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.0.1-1
- Updating to Kibana 4.0.1.

* Sun Feb 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 4.0.0-1
- Creating initial spec file for Kibana 4.0.0.