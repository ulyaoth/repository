%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat
%define java_version 1.8.0

Summary:    Tomcat native library
Name:       ulyaoth-tomcat-native
Version:    1.1.34
Release:    3%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-connectors/native/%{version}/source/tomcat-native-%{version}-src.tar.gz
BuildRoot:  %{_tmppath}/tomcat-native-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-%{java_version}-openjdk-devel
BuildRequires:  jpackage-utils
BuildRequires:  ulyaoth-apr-devel
BuildRequires:  ulyaoth-openssl1.0.2-devel

Requires: ulyaoth-apr
Requires: ulyaoth-openssl1.0.2

Provides:  tcnative = %{version}-%{release}
Provides:  tomcat-native
provides:  ulyaoth-tomcat-native

Conflicts: ulyaoth-tomcat-native1.2

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
cd jni/native
%configure \
    --with-apr=%{_bindir}/apr-1-config \
	--with-ssl=/usr/local/ulyaoth/openssl1.0.2 \
    --with-java-home=/usr/lib/jvm/java \
    --with-java-platform=2
make %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
make -C jni/native install DESTDIR=$RPM_BUILD_ROOT
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

Thanks for using ulyaoth-tomcat-native!

Please find the official documentation for Tomcat Native here:
* https://tomcat.apache.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Sun Nov 19 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.1.34-3
- Using ulyaoth-apr.
- Using ulyaoth-openssl1.0.2.

* Tue Jan 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.34-2
- Added conflict for new Tomcat Native 1.2 rpm.
- Forced build with Java 8, sorry about time.

* Sun Dec 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.34-1
- Updated to Tomcat Native 1.1.34.

* Tue Mar 31 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.33-1
- Updated to Tomcat Native 1.1.33.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.32-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.32-2
- Removal of some things from spec file.
- Support for Fedora 22 and CentOS 6 & 7.
- i386 Support.

* Fri Oct 31 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.32-1
- Update to version 1.1.32.
- http://tomcat.apache.org/native-doc/miscellaneous/changelog.html

* Sat Oct 4 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.31-1
- Support for Fedora 21.

* Wed Sep 17 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.1.31-1
- Creating spec for Tomcat-native 1.1.31.
- Spec file based on spec file from Ville Skyttä <ville.skytta@iki.fi>.