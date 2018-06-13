
AutoReqProv: no
%define __jar_repack %{nil}
%define debug_package %{nil}
%define zookeeper_home /var/lib/zookeeper
%define zookeeper_group hadoop
%define zookeeper_user zookeeper

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
Version:    3.4.12
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://zookeeper.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/log4j.properties
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zoo.cfg
Source5:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/zookeeper-env.sh
Source6:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/SOURCES/myid
BuildRoot:  %{_tmppath}/zookeeper-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: doxygen
BuildRequires: perl
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gawk
BuildRequires: make

Provides: zookeeper
Provides: apache-zookeeper
Provides: ulyaoth-zookeeper
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

%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/*.a

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
        $RPM_BUILD_ROOT/etc/zookeeper/log4j.properties
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT/etc/zookeeper/zoo.cfg
%{__install} -m644 %SOURCE5 \
        $RPM_BUILD_ROOT/etc/zookeeper/zookeeper-env.sh
%{__install} -m644 %SOURCE6 \
        $RPM_BUILD_ROOT/var/lib/zookeeper/myid

sed -i 's#$ZOOBINDIR/../etc/zookeeper#/etc/zookeeper#g' $RPM_BUILD_ROOT/usr/libexec/zkEnv.sh
sed -i 's#$ZOOBINDIR/zkEnv.sh#/usr/libexec/zkEnv.sh#g' $RPM_BUILD_ROOT/usr/bin/zkServer.sh

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

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{zookeeper_group} >/dev/null || groupadd -r %{zookeeper_group}
getent passwd %{zookeeper_user} >/dev/null || /usr/sbin/useradd --comment "Zookeeper Daemon User" --shell /bin/bash -M -r -g %{zookeeper_group} --home %{zookeeper_home} %{zookeeper_user}

%files
%defattr(-,%{zookeeper_user},%{zookeeper_group})
%dir %{zookeeper_home}
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

Thank you for using ulyaoth-zookeeper3.4!

Please find the official documentation for zookeeper here:
* https://zookeeper.apache.org/

For any additional information or help please visit our website at:
* https://ulyaoth.com

Ulyaoth repository could use your help! Please consider a donation:
* https://ulyaoth.com/donate

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
* Wed Jun 13 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 3.4.12-1
- Updating to Zookeeper 3.4.12.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 3.4.11-1
- Updating to Zookeeper 3.4.11.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.4.10-1
- Updating to Zookeeper 3.4.10.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.4.9-1
- Updating to Zookeeper 3.4.9.

* Tue Feb 23 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.4.8-1
- Updating to Zookeeper 3.4.8.

* Tue Dec 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.4.6-1
- Initial rpm release.