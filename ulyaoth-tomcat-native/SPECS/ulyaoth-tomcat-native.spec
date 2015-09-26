
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Tomcat native library
Name:       ulyaoth-tomcat-native
Version:    1.1.33
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
Source0:    tomcat-native-%{version}-src.tar.gz
BuildRoot:  %{_tmppath}/tomcat-native-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  apr-devel >= 1.2.1
BuildRequires:  openssl-devel

Provides:  tcnative = %{version}-%{release}
Provides:  tomcat-native
provides:  ulyaoth-tomcat-native

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
	--with-ssl=yes \
    --with-java-home=%{java_home} \
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

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional help please visit my forum at:
* http://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
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
