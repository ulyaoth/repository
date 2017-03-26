%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl1.0.1
Version:    1.0.1u
Release:    2%{?dist}
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
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SOURCES/ulyaoth-openssl1.0.1.conf
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-openssl1.0.1-libs

Provides: ulyaoth-openssl1.0.1
Provides: ulyaoth-openssl1.0.1u

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Provides: ulyaoth-openssl1.0.1-libs
%description libs
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-libs package contains the libraries that are used by various applications which support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl1.0.1-libs
Provides: ulyaoth-openssl1.0.1-devel
%description devel
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-devel package contains include files needed to develop applications which support various cryptographic algorithms and protocols.

%package static
Summary: Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl1.0.1-devel
Provides: ulyaoth-openssl1.0.1-static
%description static
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-static package contains static libraries needed for static linking of applications which support various cryptographic algorithms and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: ulyaoth-openssl1.0.1
%description perl
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-perl package provides Perl scripts for converting certificates and keys from other formats to the formats used by the OpenSSL toolkit.


%prep
%setup -q -n openssl-%{version}

%build
export C_INCLUDE_PATH=/usr/local/ulyaoth/openssl1.0.1/include
export LIBRARY_PATH=/usr/local/ulyaoth/openssl1.0.1/lib
export LD_RUN_PATH=/usr/local/ulyaoth/openssl1.0.1/lib

./config -Wl,-rpath=/usr/local/ulyaoth/openssl1.0.1/lib --openssldir=/usr/local/ulyaoth/openssl1.0.1 no-ssl2 no-ssl3 shared
make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.0.1

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-openssl1.0.1.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.0.1
/usr/local/ulyaoth/openssl1.0.1/bin/openssl
/usr/local/ulyaoth/openssl1.0.1/man/man1*/*
/usr/local/ulyaoth/openssl1.0.1/man/man5*/*
/usr/local/ulyaoth/openssl1.0.1/man/man7*/*
%exclude /usr/local/ulyaoth/openssl1.0.1/man/man1*/*.pl*
%exclude /usr/local/ulyaoth/openssl1.0.1/man/man1*/c_rehash*
%exclude /usr/local/ulyaoth/openssl1.0.1/man/man1*/tsget*


%files libs
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.0.1
/usr/local/ulyaoth/openssl1.0.1/openssl.cnf.dist
%config(noreplace) /usr/local/ulyaoth/openssl1.0.1/openssl.cnf
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.0.1/lib/libcrypto.so.1.1
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.0.1/lib/libssl.so.1.1
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.0.1/lib/engines-1.1/*
/etc/ld.so.conf.d/ulyaoth-openssl1.0.1.conf

%files devel
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.0.1
%dir /usr/local/ulyaoth/openssl1.0.1/lib/pkgconfig
/usr/local/ulyaoth/openssl1.0.1/lib/*.so
/usr/local/ulyaoth/openssl1.0.1/include/*
/usr/local/ulyaoth/openssl1.0.1/man/man3*/*
/usr/local/ulyaoth/openssl1.0.1/lib/pkgconfig/*.pc

%files static
/usr/local/ulyaoth/openssl1.0.1/lib/*.a

%files perl
/usr/local/ulyaoth/openssl1.0.1/bin/c_rehash
/usr/local/ulyaoth/openssl1.0.1/bin/CA.pl
/usr/local/ulyaoth/openssl1.0.1/bin/tsget
/usr/local/ulyaoth/openssl1.0.1/man/man1*/*.pl*
/usr/local/ulyaoth/openssl1.0.1/man/man1*/c_rehash*
/usr/local/ulyaoth/openssl1.0.1/man/man1*/tsget*

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.0.1!

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

Thank you for using ulyaoth-openssl1.0.1-libs!

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

Thank you for using ulyaoth-openssl1.0.1-devel!

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

Thank you for using ulyaoth-openssl1.0.1-static!

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

Thank you for using ulyaoth-openssl1.0.1-perl!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun -p /sbin/ldconfig

%changelog
* Sun Mar 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1u-3
- Changed directory structure.
- ld fixes.
- split into sub packages, perl, static, libs, devel.

* Mon Oct 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1u-2
- Added ldd fixes.

* Mon Sep 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1u-1
- Updated to OpenSSL version 1.0.1u.

* Tue May 3 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1t-1
- Updated to OpenSSL version 1.0.1t.

* Tue Mar 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1s-1
- Updated to OpenSSL version 1.0.1s.

* Thu Jan 28 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1r-1
- Updated to OpenSSL version 1.0.1r.

* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1q-2
- added "shared" to compile options.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.1q-1
- Initial release with openssl 1.0.1q.