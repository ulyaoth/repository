Summary:    Commons Daemon
Name:       ulyaoth-jsvc
Version:    1.1.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      System Environment/Daemons
URL:        https://www.ulyaoth.net
Vendor:     Ulyaoth
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net//commons/daemon/source/commons-daemon-%{version}-src.tar.gz
BuildRoot:  %{_tmppath}/jsvc-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: libcap-devel

Provides: ulyaoth-jsvc
Provides: jsvc

%description
Jsvc is a set of libraries and applications for making Java applications run on UNIX more easily.

%prep
%setup -q -n commons-daemon-%{version}-src

%build
%{__rm} -rf $RPM_BUILD_ROOT
cd %{_builddir}/commons-daemon-%{version}-src/src/native/unix
./configure --with-java=/usr/lib/jvm/java-openjdk
make %{?_smp_mflags}

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mv} %{_builddir}/commons-daemon-%{version}-src/src/native/unix/jsvc $RPM_BUILD_ROOT/usr/bin/


%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf %{_builddir}/*


%files
%defattr(-,root,root,-)
/usr/bin/jsvc

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-jsvc

Please find the official documentation for jsvc here:
* http://commons.apache.org/proper/commons-daemon/jsvc.html

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Thu Nov 30 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.1.0-1
- Update jsvc to 1.1.0.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.15-1
- Initial release.