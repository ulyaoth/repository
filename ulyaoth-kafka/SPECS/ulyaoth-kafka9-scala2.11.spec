
%define __jar_repack %{nil}
%define debug_package %{nil}
%define kafka_home /var/lib/kafka
%define kafka_group hadoop
%define kafka_user kafka
%define scala_version 2.11
%define kafka_version 0.9.0.1

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

Summary:    Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name:       ulyaoth-kafka9
Version:    %{kafka_version}_%{scala_version}
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://kafka.apache.org
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/log4j.properties
BuildRoot:  %{_tmppath}/kafka-%{kafka_version}_%{scala_version}-%{release}-root-%(%{__id_u} -n)

Provides: kafka
Provides: kafka9
Provides: apache-kafka
Provides: ulyaoth-kafka9

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers.

%prep
%setup -q -n kafka_%{scala_version}-%{kafka_version}

%build

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/etc/kafka

cp -rf %_builddir/zookeeper-%{version}/bin/*.sh $RPM_BUILD_ROOT/usr/bin/
mv $RPM_BUILD_ROOT/usr/bin/zkEnv.sh $RPM_BUILD_ROOT/usr/libexec/zkEnv.sh
cp -rf %_builddir/zookeeper-%{version}/docs/*  $RPM_BUILD_ROOT/usr/share/doc/zookeeper/
cp -rf %_builddir/zookeeper-%{version}/zookeeper-%{version}.jar $RPM_BUILD_ROOT/usr/share/zookeeper/
cp -rf %_builddir/zookeeper-%{version}/lib/*.jar $RPM_BUILD_ROOT/usr/share/zookeeper/

%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT/etc/kafka/log4j.properties

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/kafka.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/kafka
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{kafka_group} >/dev/null || groupadd -r %{kafka_group}
getent passwd %{kafka_user} >/dev/null || /usr/sbin/useradd --comment "Kafka Daemon User" --shell /bin/bash -M -r -g %{kafka_group} --home %{kafka_home} %{kafka_user}

%files
%defattr(-,%{kafka_user},%{kafka_group})
%dir %{kafka_home}
%dir %{_localstatedir}/log/zookeeper
%dir /etc/zookeeper
%dir %{_localstatedir}/lib/zookeeper
%dir /usr/share/zookeeper
%config(noreplace) /etc/zookeeper/zoo.cfg
%config(noreplace) /etc/zookeeper/log4j.properties
%config(noreplace) /etc/zookeeper/zookeeper-env.sh
%config(noreplace) %{_localstatedir}/lib/zookeeper/myid
/usr/share/zookeeper/*.jar

%defattr(-,root,root)
%dir /usr/share/doc/zookeeper/
/usr/share/doc/zookeeper/*
%dir /usr/include/zookeeper/
/usr/include/zookeeper/*
/usr/libexec/zkEnv.sh
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen
%{_bindir}/zkCleanup.sh
%{_bindir}/zkCli.sh
%{_bindir}/zkServer.sh
%{_libdir}/libzookeeper_mt.so
%{_libdir}/libzookeeper_mt.so.2
%{_libdir}/libzookeeper_mt.so.2.0.0
%{_libdir}/libzookeeper_st.so
%{_libdir}/libzookeeper_st.so.2
%{_libdir}/libzookeeper_st.so.2.0.0

%if %{use_systemd}
%{_unitdir}/kafka.service
%else
%{_initrddir}/kafka
%endif

%post
# Register the kafka service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset kafka.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add kafka
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-kafka9!

Please find the official documentation for kafka here:
* https://kafka.apache.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable kafka.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop kafka.service >/dev/null 2>&1 ||:
%else
    /sbin/service kafka stop > /dev/null 2>&1
    /sbin/chkconfig --del kafka
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service kafka status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sun Apr 3 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.0.1_2.11-1
- Initial rpm release.
- Kafka 0.9.0.1 build with Scala 2.11.