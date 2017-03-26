%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl0.9.8
Version:    0.9.8zh
Release:    4%{?dist}
BuildArch: x86_64
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
%if 0%{?fedora}  == 19
Source0:    http://www.openssl.org/source/openssl-%{version}.tar.gz
%else
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
%endif
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SOURCES/ulyaoth-openssl0.9.8.conf
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-openssl0.9.8-libs

Provides: ulyaoth-openssl0.9.8
Provides: ulyaoth-openssl0.9.8zh

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Provides: ulyaoth-openssl0.9.8-libs
%description libs
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-libs package contains the libraries that are used by various applications which support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl0.9.8-libs
Provides: ulyaoth-openssl0.9.8-devel
%description devel
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-devel package contains include files needed to develop applications which support various cryptographic algorithms and protocols.

%package static
Summary: Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl0.9.8-devel
Provides: ulyaoth-openssl0.9.8-static
%description static
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-static package contains static libraries needed for static linking of applications which support various cryptographic algorithms and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: ulyaoth-openssl0.9.8
%description perl
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-perl package provides Perl scripts for converting certificates and keys from other formats to the formats used by the OpenSSL toolkit.


%prep
%setup -q -n openssl-%{version}

%build
export C_INCLUDE_PATH=/usr/local/ulyaoth/openssl0.9.8/include
export LIBRARY_PATH=/usr/local/ulyaoth/openssl0.9.8/lib
export LD_RUN_PATH=/usr/local/ulyaoth/openssl0.9.8/lib

./config -Wl,-rpath=/usr/local/ulyaoth/openssl0.9.8/lib --openssldir=/usr/local/ulyaoth/openssl0.9.8 no-ssl2 no-ssl3 shared
make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8/misc/* $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8/bin/
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8/certs
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8/private
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl0.9.8/misc


%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-openssl0.9.8.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl0.9.8
/usr/local/ulyaoth/openssl0.9.8/bin/openssl
/usr/local/ulyaoth/openssl0.9.8/man/man1*/*
/usr/local/ulyaoth/openssl0.9.8/man/man5*/*
/usr/local/ulyaoth/openssl0.9.8/man/man7*/*
%exclude /usr/local/ulyaoth/openssl0.9.8/man/man1*/*.pl*

%files libs
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl0.9.8
%config(noreplace) /usr/local/ulyaoth/openssl0.9.8/openssl.cnf
%attr(0755,root,root) /usr/local/ulyaoth/openssl0.9.8/lib/libcrypto.so.0.9.8
%attr(0755,root,root) /usr/local/ulyaoth/openssl0.9.8/lib/libssl.so.0.9.8
%attr(0755,root,root) /usr/local/ulyaoth/openssl0.9.8/lib/engines/*
/etc/ld.so.conf.d/ulyaoth-openssl0.9.8.conf

%files devel
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl0.9.8
%dir /usr/local/ulyaoth/openssl0.9.8/lib/pkgconfig
/usr/local/ulyaoth/openssl0.9.8/lib/*.so
/usr/local/ulyaoth/openssl0.9.8/include/*
/usr/local/ulyaoth/openssl0.9.8/man/man3*/*
/usr/local/ulyaoth/openssl0.9.8/lib/pkgconfig/*.pc

%files static
/usr/local/ulyaoth/openssl0.9.8/lib/*.a

%files perl
/usr/local/ulyaoth/openssl0.9.8/bin/c_rehash
/usr/local/ulyaoth/openssl0.9.8/bin/CA.pl
/usr/local/ulyaoth/openssl0.9.8/bin/CA.sh
/usr/local/ulyaoth/openssl0.9.8/bin/c_hash
/usr/local/ulyaoth/openssl0.9.8/bin/c_info
/usr/local/ulyaoth/openssl0.9.8/bin/c_issuer
/usr/local/ulyaoth/openssl0.9.8/bin/c_name
/usr/local/ulyaoth/openssl0.9.8/man/man1*/*.pl*

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-openssl0.9.8!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post libs
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl0.9.8-libs!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post devel
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl0.9.8-devel!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post static
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl0.9.8-static!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post perl
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl0.9.8-perl!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun -p /sbin/ldconfig

%changelog
* Sun Mar 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-4
- Changed directory structure.
- ld fixes.
- split into sub packages, perl, static, libs, devel.

* Mon Oct 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-3
- Added ldd fixes.

* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-2
- added "shared" to compile options.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-1
- Initial release with openssl 0.9.8zh.