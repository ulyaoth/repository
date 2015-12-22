%define __jar_repack %{nil}
%define debug_package %{nil}
%define zookeeper_home /opt/zookeeper
%define zookeeper_group zookeeper
%define zookeeper_user hadoop

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

Summary:    Apache ZooKeeper is an effort to develop and maintain an open-source server which enables highly reliable distributed coordination.
Name:       ulyaoth-zookeeper3.4
Version:    3.4.7
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://zookeeper.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/log4j.properties
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zoo.cfg
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper-env.sh
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/myid
BuildRoot:  %{_tmppath}/zookeeper-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: zookeeper
Provides: zookeeper3.4
Provides: apache-zookeeper
Provides: ulyaoth-zookeeper3.4

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them ,which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%setup -q -n zookeeper-%{version}

%build
cd %_builddir/zookeeper-%{version}/src/c
%configure
make %{?_smp_mflags}

%install
cd %_builddir/zookeeper-%{version}/src/c
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT/usr/lib64/*.la
%{__rm} -rf $RPM_BUILD_ROOT/usr/lib64/*.a

%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/zookeeper
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/zookeeper
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/zookeeper
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/zookeeper
%{__mkdir} -p $RPM_BUILD_ROOT/usr/libexec
%{__mkdir} -p $RPM_BUILD_ROOT/etc/zookeeper

cp -rf %_builddir/zookeeper-%{version}/bin/*.sh $RPM_BUILD_ROOT/usr/bin/
mv $RPM_BUILD_ROOT/usr/bin/zkEnv.sh $RPM_BUILD_ROOT/usr/libexec/zkEnv.sh
cp -rf %_builddir/zookeeper-%{version}/docs/*  $RPM_BUILD_ROOT/usr/share/doc/zookeeper/
cp -rf %_builddir/zookeeper-%{version}/zookeeper-%{version}.jar $RPM_BUILD_ROOT/usr/share/zookeeper/
cp -rf %_builddir/zookeeper-%{version}/lib/*.jar $RPM_BUILD_ROOT/usr/share/zookeeper/

%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%/etc/zookeeper/log4j.properties
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT%/etc/zookeeper/zoo.cfg
%{__install} -m644 %SOURCE5 \
        $RPM_BUILD_ROOT%/etc/zookeeper/zookeeper-env.sh
%{__install} -m644 %SOURCE6 \
        $RPM_BUILD_ROOT%/var/lib/zookeeper/myid

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/zookeeper
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{zookeeper_group} >/dev/null || groupadd -r %{zookeeper_group}
getent passwd %{zookeeper_user} >/dev/null || /usr/sbin/useradd --comment "Zookeeper Daemon User" --shell /bin/bash -M -r -g %{zookeeper_group} --home %{zookeeper_home} %{zookeeper_user}

%files
%defattr(-,%{zookeeper_user},%{zookeeper_group})
%{zookeeper_home}/*
%dir %{zookeeper_home}
%dir %{_localstatedir}/log/zookeeper
%config(noreplace) %{zookeeper_home}/conf/web.xml
%config(noreplace) %{zookeeper_home}/conf/tomcat-users.xml
%config(noreplace) %{zookeeper_home}/conf/server.xml
%config(noreplace) %{zookeeper_home}/conf/logging.properties
%config(noreplace) %{zookeeper_home}/conf/context.xml
%config(noreplace) %{zookeeper_home}/conf/catalina.properties
%config(noreplace) %{zookeeper_home}/conf/catalina.policy

%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%if %{use_systemd}
%{_unitdir}/zookeeper.service
%else
%{_initrddir}/zookeeper
%endif

%post
# Register the zookeeper service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset zookeeper.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add zookeeper
%endif

cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-zookeeper3.4!

Please find the official documentation for zookeeper here:
* http://tomcat.apache.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable zookeeper.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop zookeeper.service >/dev/null 2>&1 ||:
%else
    /sbin/service zookeeper stop > /dev/null 2>&1
    /sbin/chkconfig --del zookeeper
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service zookeeper status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Tue Dec 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.4.7-1
- Initial rpm release.