%if 0%{?fedora} >= 23
AutoReqProv: yes
%else
AutoReqProv: no
%endif

%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat
%define ulyaoth_openssl_version 1.1.1
%define java_version 1.8.0

Summary:    Tomcat native library
Name:       ulyaoth-tomcat-native1.2
Version:    1.2.17
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-connectors/native/%{version}/source/tomcat-native-%{version}-src.tar.gz
BuildRoot:  %{_tmppath}/tomcat-native-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ulyaoth-apr-devel
%if 0%{?fedora} >= 26
BuildRequires: openssl-devel
%else
BuildRequires: ulyaoth-openssl%{ulyaoth_openssl_version}-devel
%endif
BuildRequires: java-%{java_version}-openjdk-devel
BuildRequires: jpackage-utils

%if 0%{?fedora} >= 23
BuildRequires: openssl-devel
%else
Requires: ulyaoth-openssl%{ulyaoth_openssl_version}
%endif
Requires: ulyaoth-apr

Provides:  tcnative = %{version}-%{release}
Provides:  tomcat-native
provides:  ulyaoth-tomcat-native1.2

Conflicts: ulyaoth-tomcat-native

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat that allows Tomcat to use certain native resources for performance, compatibility, etc.

Specifically, the Apache Tomcat Native Library gives Tomcat access to the Apache Portable Runtime (APR) library's network connection (socket) implementation and random-number generator. See the Apache Tomcat documentation for more information on how to configure Tomcat to use the APR connector.

Features of the APR connector:

Non-blocking I/O for Keep-Alive requests (between requests)
Uses OpenSSL for TLS/SSL capabilities (if supported by linked APR library)
FIPS 140-2 support for TLS/SSL (if supported by linked OpenSSL library)


%prep
%setup -q -n tomcat-native-%{version}-src
f=CHANGELOG.txt ; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f


%build
cd native
%configure \
  --with-apr=%{_bindir}/apr-1-config \
  --with-java-home=/usr/lib/jvm/java \
  --with-ssl=/usr/local/ulyaoth/openssl%{ulyaoth_openssl_version}
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make -C native install DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f $RPM_BUILD_ROOT/usr/lib64/libtcnative*.*a
%{__rm} -rf $RPM_BUILD_ROOT/usr/lib64/pkgconfig
%{__rm} -f $RPM_BUILD_ROOT/usr/lib/libtcnative*.*a
%{__rm} -rf $RPM_BUILD_ROOT/usr/lib/pkgconfig
%{__mkdir} -p $RPM_BUILD_ROOT/usr/lib/
cd %{buildroot}/usr/lib/
%ifarch x86_64
ln -s /usr/lib64/libtcnative-1.so libtcnative-1.so
ln -s /usr/lib64/libtcnative-1.so.0 libtcnative-1.so.0
%endif
cd -

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE NOTICE TODO.txt
%ifarch x86_64
/usr/lib64/libtcnative*.so*
%endif
/usr/lib/libtcnative*.so*


%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat-native1.2!

Please find the official documentation for Tomcat Native here:
* https://tomcat.apache.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Fri Nov 9 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 1.2.17-1
- Updated to Tomcat Native 1.2.17.

* Sun Nov 26 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.2.16-1
- Updated to Tomcat Native 1.2.16.

* Sun Nov 19 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.2.14-1
- Updated to Tomcat Native 1.2.14.
- Fixed spec file to build with new ulyaoth-openssl structure.

* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.12-1
- Updated to Tomcat Native 1.2.12.
- Updated to use OpenSSL 1.1.0.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.10-1
- Updated to Tomcat Native 1.2.10.

* Fri Jul 8 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.8-1
- Updated to Tomcat Native 1.2.8.

* Fri May 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.7-1
- Updated to Tomcat Native 1.2.7.

* Sun May 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.6-1
- Updated to Tomcat Native 1.2.6.

* Fri Mar 18 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.5-1
- Updated to Tomcat Native 1.2.5.

* Wed Jan 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.4-1
- Updated to Tomcat Native 1.2.4.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.2.3-1
- Initial release for Tomcat Native 1.2.