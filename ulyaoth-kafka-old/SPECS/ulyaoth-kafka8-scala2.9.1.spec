
%define __jar_repack %{nil}
%define debug_package %{nil}
%define kafka_home /var/lib/kafka
%define kafka_group hadoop
%define kafka_user kafka
%define scala_version 2.9.1

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
Name:       ulyaoth-kafka8-scala%{scala_version}
Version:    0.8.2.2
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://kafka.apache.org
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/kafka/%{version}/kafka_%{scala_version}-%{version}.tgz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.init
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-zookeeper.service
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-zookeeper.init

%if %{use_systemd}
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-sysconfig-systemd
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-zookeeper-sysconfig-systemd
%else
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-sysconfig-initd
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka-zookeeper-sysconfig-initd
%endif

BuildRoot:  %{_tmppath}/kafka8-%{version}_%{scala_version}-%{release}-root-%(%{__id_u} -n)

Provides: kafka
Provides: kafka8
Provides: apache-kafka
Provides: ulyaoth-kafka8
Provides: ulyaoth-kafka8-scala%{scala_version}

Conflicts: ulyaoth-kafka8-scala2.9.2
Conflicts: ulyaoth-kafka8-scala2.10
Conflicts: ulyaoth-kafka8-scala2.11
Conflicts: ulyaoth-kafka9-scala2.10
Conflicts: ulyaoth-kafka9-scala2.11

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers.

%prep
%setup -q -n kafka_%{scala_version}-%{version}

%build

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/etc/kafka
%{__mkdir} -p $RPM_BUILD_ROOT/etc/sysconfig

cp -rf %_builddir/kafka_%{scala_version}-%{version}/bin/*.sh $RPM_BUILD_ROOT/usr/bin/
cp -rf %_builddir/kafka_%{scala_version}-%{version}/config/*.properties $RPM_BUILD_ROOT/etc/kafka/
cp -rf %_builddir/kafka_%{scala_version}-%{version}/libs/*.jar $RPM_BUILD_ROOT/usr/share/kafka/

sed -i 's#/tmp/kafka-logs#/var/lib/kafka#g' $RPM_BUILD_ROOT/etc/kafka/server.properties

%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT/etc/sysconfig/kafka
%{__install} -m644 %SOURCE6 \
        $RPM_BUILD_ROOT/etc/sysconfig/kafka-zookeeper

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/kafka.service
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT%{_unitdir}/kafka-zookeeper.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/kafka
%{__install} -m755 %{SOURCE5} \
   $RPM_BUILD_ROOT%{_initrddir}/kafka-zookeeper
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{kafka_group} >/dev/null || groupadd -r %{kafka_group}
getent passwd %{kafka_user} >/dev/null || /usr/sbin/useradd --comment "Kafka Daemon User" --shell /bin/bash -M -r -g %{kafka_group} --home %{kafka_home} %{kafka_user}

%files
%defattr(-,%{kafka_user},%{kafka_group})
%dir %{kafka_home}
%dir %{_localstatedir}/log/kafka
%dir %{_localstatedir}/lib/kafka
%dir /etc/kafka
%dir /usr/share/kafka
%config(noreplace) /etc/kafka/consumer.properties
%config(noreplace) /etc/kafka/log4j.properties
%config(noreplace) /etc/kafka/producer.properties
%config(noreplace) /etc/kafka/server.properties
%config(noreplace) /etc/kafka/test-log4j.properties
%config(noreplace) /etc/kafka/tools-log4j.properties
%config(noreplace) /etc/kafka/zookeeper.properties
/usr/share/kafka/jopt-simple-3.2.jar
/usr/share/kafka/kafka-clients-0.8.2.2.jar
/usr/share/kafka/kafka_2.9.1-0.8.2.2-javadoc.jar
/usr/share/kafka/kafka_2.9.1-0.8.2.2-scaladoc.jar
/usr/share/kafka/kafka_2.9.1-0.8.2.2-sources.jar
/usr/share/kafka/kafka_2.9.1-0.8.2.2-test.jar
/usr/share/kafka/kafka_2.9.1-0.8.2.2.jar
/usr/share/kafka/log4j-1.2.16.jar
/usr/share/kafka/lz4-1.2.0.jar
/usr/share/kafka/metrics-core-2.2.0.jar
/usr/share/kafka/scala-library-2.9.1.jar
/usr/share/kafka/slf4j-api-1.7.6.jar
/usr/share/kafka/slf4j-log4j12-1.6.1.jar
/usr/share/kafka/snappy-java-1.1.1.7.jar
/usr/share/kafka/zkclient-0.3.jar
/usr/share/kafka/zookeeper-3.4.6.jar

%defattr(-,root,root)
/etc/sysconfig/kafka
/etc/sysconfig/kafka-zookeeper
%{_bindir}/kafka-console-consumer.sh
%{_bindir}/kafka-console-producer.sh
%{_bindir}/kafka-consumer-offset-checker.sh
%{_bindir}/kafka-consumer-perf-test.sh
%{_bindir}/kafka-mirror-maker.sh
%{_bindir}/kafka-preferred-replica-election.sh
%{_bindir}/kafka-producer-perf-test.sh
%{_bindir}/kafka-reassign-partitions.sh
%{_bindir}/kafka-replay-log-producer.sh
%{_bindir}/kafka-replica-verification.sh
%{_bindir}/kafka-run-class.sh
%{_bindir}/kafka-server-start.sh
%{_bindir}/kafka-server-stop.sh
%{_bindir}/kafka-simple-consumer-shell.sh
%{_bindir}/kafka-topics.sh
%{_bindir}/zookeeper-server-start.sh
%{_bindir}/zookeeper-server-stop.sh
%{_bindir}/zookeeper-shell.sh

%if %{use_systemd}
%{_unitdir}/kafka.service
%{_unitdir}/kafka-zookeeper.service
%else
%{_initrddir}/kafka
%{_initrddir}/kafka-zookeeper
%endif

%post
# Register the kafka & kafka-zookeeper service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset kafka.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl preset kafka-zookeeper.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add kafka
	/sbin/chkconfig --add kafka-zookeeper
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-kafka8 with Scale 2.9.1!

Please find the official documentation for kafka here:
* https://kafka.apache.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable kafka.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl --no-reload disable kafka-zookeeper.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop kafka.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl stop kafka-zookeeper.service >/dev/null 2>&1 ||:
%else
    /sbin/service kafka stop > /dev/null 2>&1
	/sbin/service kafka-zookeeper stop > /dev/null 2>&1
    /sbin/chkconfig --del kafka
	/sbin/chkconfig --del kafka-zookeeper
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service kafka status  >/dev/null 2>&1 || exit 0
	/sbin/service kafka-zookeeper status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sun Apr 3 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.8.2.2-1
- Initial rpm release.
- Kafka 0.8.2.2 build with Scala 2.9.1.