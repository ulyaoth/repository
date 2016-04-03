
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
Source0:    http://apache.mirrors.spacedump.net/kafka/%{kafka_version}/kafka_%{scala_version}-%{kafka_version}.tgz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SOURCES/kafka
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
%{__mkdir} -p $RPM_BUILD_ROOT/etc/sysconfig

cp -rf %_builddir/kafka_%{scala_version}-%{kafka_version}/bin/*.sh $RPM_BUILD_ROOT/usr/bin/
cp -rf %_builddir/kafka_%{scala_version}-%{kafka_version}/config/*.properties $RPM_BUILD_ROOT/etc/kafka/
cp -rf %_builddir/kafka_%{scala_version}-%{kafka_version}/libs/*.jar $RPM_BUILD_ROOT/usr/share/kafka/
cp -rf %_builddir/kafka_%{scala_version}-%{kafka_version}/libs/*.asc $RPM_BUILD_ROOT/usr/share/kafka/

sed -i 's#/tmp/kafka-logs#/var/lib/kafka#g' $RPM_BUILD_ROOT/etc/kafka/server.properties

%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT/etc/sysconfig/kafka

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
%dir %{_localstatedir}/log/kafka
%dir %{_localstatedir}/lib/kafka
%dir /etc/kafka
%dir /usr/share/kafka
%config(noreplace) /etc/kafka/connect-console-sink.properties
%config(noreplace) /etc/kafka/connect-console-source.properties
%config(noreplace) /etc/kafka/connect-distributed.properties
%config(noreplace) /etc/kafka/connect-file-sink.properties
%config(noreplace) /etc/kafka/connect-file-source.properties
%config(noreplace) /etc/kafka/connect-log4j.properties
%config(noreplace) /etc/kafka/connect-standalone.properties
%config(noreplace) /etc/kafka/consumer.properties
%config(noreplace) /etc/kafka/log4j.properties
%config(noreplace) /etc/kafka/producer.properties
%config(noreplace) /etc/kafka/server.properties
%config(noreplace) /etc/kafka/test-log4j.properties
%config(noreplace) /etc/kafka/tools-log4j.properties
%config(noreplace) /etc/kafka/zookeeper.properties
/usr/share/kafka/aopalliance-repackaged-2.4.0-b31.jar
/usr/share/kafka/argparse4j-0.5.0.jar
/usr/share/kafka/connect-api-0.9.0.1.jar
/usr/share/kafka/connect-file-0.9.0.1.jar
/usr/share/kafka/connect-json-0.9.0.1.jar
/usr/share/kafka/connect-runtime-0.9.0.1.jar
/usr/share/kafka/hk2-api-2.4.0-b31.jar
/usr/share/kafka/hk2-locator-2.4.0-b31.jar
/usr/share/kafka/hk2-utils-2.4.0-b31.jar
/usr/share/kafka/jackson-annotations-2.5.0.jar
/usr/share/kafka/jackson-core-2.5.4.jar
/usr/share/kafka/jackson-databind-2.5.4.jar
/usr/share/kafka/jackson-jaxrs-base-2.5.4.jar
/usr/share/kafka/jackson-jaxrs-json-provider-2.5.4.jar
/usr/share/kafka/jackson-module-jaxb-annotations-2.5.4.jar
/usr/share/kafka/javassist-3.18.1-GA.jar
/usr/share/kafka/javax.annotation-api-1.2.jar
/usr/share/kafka/javax.inject-1.jar
/usr/share/kafka/javax.inject-2.4.0-b31.jar
/usr/share/kafka/javax.servlet-api-3.1.0.jar
/usr/share/kafka/javax.ws.rs-api-2.0.1.jar
/usr/share/kafka/jersey-client-2.22.1.jar
/usr/share/kafka/jersey-common-2.22.1.jar
/usr/share/kafka/jersey-container-servlet-2.22.1.jar
/usr/share/kafka/jersey-container-servlet-core-2.22.1.jar
/usr/share/kafka/jersey-guava-2.22.1.jar
/usr/share/kafka/jersey-media-jaxb-2.22.1.jar
/usr/share/kafka/jersey-server-2.22.1.jar
/usr/share/kafka/jetty-http-9.2.12.v20150709.jar
/usr/share/kafka/jetty-io-9.2.12.v20150709.jar
/usr/share/kafka/jetty-security-9.2.12.v20150709.jar
/usr/share/kafka/jetty-server-9.2.12.v20150709.jar
/usr/share/kafka/jetty-servlet-9.2.12.v20150709.jar
/usr/share/kafka/jetty-util-9.2.12.v20150709.jar
/usr/share/kafka/jopt-simple-3.2.jar
/usr/share/kafka/kafka_2.11-0.9.0.1.jar
/usr/share/kafka/kafka_2.11-0.9.0.1.jar.asc
/usr/share/kafka/kafka_2.11-0.9.0.1-javadoc.jar
/usr/share/kafka/kafka_2.11-0.9.0.1-javadoc.jar.asc
/usr/share/kafka/kafka_2.11-0.9.0.1-scaladoc.jar
/usr/share/kafka/kafka_2.11-0.9.0.1-scaladoc.jar.asc
/usr/share/kafka/kafka_2.11-0.9.0.1-sources.jar
/usr/share/kafka/kafka_2.11-0.9.0.1-sources.jar.asc
/usr/share/kafka/kafka_2.11-0.9.0.1-test.jar
/usr/share/kafka/kafka_2.11-0.9.0.1-test.jar.asc
/usr/share/kafka/kafka-clients-0.9.0.1.jar
/usr/share/kafka/kafka-log4j-appender-0.9.0.1.jar
/usr/share/kafka/kafka-tools-0.9.0.1.jar
/usr/share/kafka/log4j-1.2.17.jar
/usr/share/kafka/lz4-1.2.0.jar
/usr/share/kafka/metrics-core-2.2.0.jar
/usr/share/kafka/osgi-resource-locator-1.0.1.jar
/usr/share/kafka/scala-library-2.11.7.jar
/usr/share/kafka/scala-parser-combinators_2.11-1.0.4.jar
/usr/share/kafka/scala-xml_2.11-1.0.4.jar
/usr/share/kafka/slf4j-api-1.7.6.jar
/usr/share/kafka/slf4j-log4j12-1.7.6.jar
/usr/share/kafka/snappy-java-1.1.1.7.jar
/usr/share/kafka/validation-api-1.1.0.Final.jar
/usr/share/kafka/zkclient-0.7.jar
/usr/share/kafka/zookeeper-3.4.6.jar

%defattr(-,root,root)
%dir /usr/share/doc/kafka/
/usr/share/doc/kafka/*
/etc/sysconfig/kafka
%{_bindir}/connect-distributed.sh
%{_bindir}/connect-standalone.sh
%{_bindir}/kafka-acls.sh
%{_bindir}/kafka-configs.sh
%{_bindir}/kafka-console-consumer.sh
%{_bindir}/kafka-console-producer.sh
%{_bindir}/kafka-consumer-groups.sh
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
%{_bindir}/kafka-verifiable-consumer.sh
%{_bindir}/kafka-verifiable-producer.sh
%{_bindir}/zookeeper-security-migration.sh
%{_bindir}/zookeeper-server-start.sh
%{_bindir}/zookeeper-server-stop.sh
%{_bindir}/zookeeper-shell.sh

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

Thanks for using ulyaoth-kafka9 with Scale 2.11!

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