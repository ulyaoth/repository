
%define __jar_repack %{nil}
%define debug_package %{nil}
%define kafka_manager_home /etc/kafka-manager
%define kafka_manager_group hadoop
%define kafka_manager_user kafka-manager

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

Summary:    A tool for managing Apache Kafka.
Name:       ulyaoth-kafka-manager
Version:    1.3.0.8
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://github.com/yahoo/kafka-manager
Vendor:     Yahoo
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    kafka-manager-%{version}.zip
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/SOURCES/kafka-manager.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/SOURCES/kafka-manager.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/SOURCES/application.ini
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/SOURCES/kafka-manager.conf
BuildRoot:  %{_tmppath}/kafka-manager-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-1.8.0-openjdk-devel

Provides: kafka-manager
Provides: ulyaoth-kafka-manager

%description
Kafka Manager is a tool for managing Apache Kafka.

%prep
%setup -q -n kafka-manager-%{version}

%build

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/kafka-manager
%{__mkdir} -p $RPM_BUILD_ROOT%{kafka_manager_home}
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir}
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/kafka-manager
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/kafka-manager
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/kafka-manager
%{__mkdir} -p $RPM_BUILD_ROOT/etc/tmpfiles.d


cp -rf %_builddir/kafka-manager-%{version}/bin/kafka-manager $RPM_BUILD_ROOT%{_bindir}
cp -rf %_builddir/kafka-manager-%{version}/conf/* $RPM_BUILD_ROOT%{kafka_manager_home}
cp -rf %_builddir/kafka-manager-%{version}/lib/* $RPM_BUILD_ROOT/usr/share/kafka-manager/
cp -rf %_builddir/kafka-manager-%{version}/share/doc/api/* $RPM_BUILD_ROOT/usr/share/doc/kafka-manager/

%{__install} -m 644 -p %{SOURCE3} \
	$RPM_BUILD_ROOT%{kafka_manager_home}/application.ini
%{__install} -m 644 -p %{SOURCE4} \
	$RPM_BUILD_ROOT/etc/tmpfiles.d/kafka-manager.conf

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/kafka-manager.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/kafka-manager
%endif

sed -i 's|$(realpath "${app_home}/../lib")|/usr/share/kafka-manager|' $RPM_BUILD_ROOT%{_bindir}/kafka-manager
sed -i 's|${app_home}/../conf/application.ini|/etc/kafka-manager/application.ini|' $RPM_BUILD_ROOT%{_bindir}/kafka-manager
sed -i 's|${application.home}/logs/application.log|/var/log/kafka-manager/application.log|' $RPM_BUILD_ROOT%{kafka_manager_home}/logback.xml
sed -i 's|${application.home}/logs/application.log|/var/log/kafka-manager/application.log|' $RPM_BUILD_ROOT%{kafka_manager_home}/logger.xml

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{kafka_manager_group} >/dev/null || groupadd -r %{kafka_manager_group}
getent passwd %{kafka_manager_user} >/dev/null || /usr/sbin/useradd --comment "Kafka Manager Daemon User" --shell /bin/bash -M -r -g %{kafka_manager_group} --home %{kafka_manager_home} %{kafka_manager_user}

%files
%defattr(-,%{kafka_manager_user},%{kafka_manager_group})
%dir %{kafka_manager_home}
%dir %{_localstatedir}/log/kafka-manager
%dir %{_localstatedir}/run/kafka-manager
%config(noreplace) %{kafka_manager_home}/application.conf
%config(noreplace) %{kafka_manager_home}/logback.xml
%config(noreplace) %{kafka_manager_home}/logger.xml
%config(noreplace) %{kafka_manager_home}/routes
%config(noreplace) %{kafka_manager_home}/application.ini

%dir /usr/share/doc/kafka-manager
/usr/share/doc/kafka-manager/*
%dir /usr/share/kafka-manager/
/usr/share/kafka-manager/*

%defattr(-,root,root)
%{_bindir}/kafka-manager
/etc/tmpfiles.d/kafka-manager.conf
%if %{use_systemd}
%{_unitdir}/kafka-manager.service
%else
%{_initrddir}/kafka-manager
%endif


%post
# Register the kafka-manager service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset kafka-manager.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add kafka-manager
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-kafka-manager!

Please find the official documentation for kafka manager here:
* https://github.com/yahoo/kafka-manager

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable kafka-manager.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop kafka-manager.service >/dev/null 2>&1 ||:
%else
    /sbin/service kafka-manager stop > /dev/null 2>&1
    /sbin/chkconfig --del kafka-manager
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service kafka-manager status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sun Jun 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.0.8-1
- initial Release.