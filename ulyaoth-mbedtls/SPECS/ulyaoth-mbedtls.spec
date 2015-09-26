%define debug_package %{nil}

# distribution specific definitions

%if 0%{?fedora} >= 18
BuildRequires: pkcs11-helper-devel
%endif

# end of distribution specific definitions

Summary: mbed TLS is an open source and commercial SSL library licensed by ARM Limited.. mbed TLS used to be called PolarSSL,
Name: ulyaoth-mbedtls
Version: 1.3.13
Release: 1%{?dist}
BuildArch: x86_64
Vendor: ARM Limited.
URL: https://tls.mbed.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://github.com/ARMmbed/mbedtls/archive/mbedtls-1.3.13.tar.gz

License: GPLv2 or proprietary

BuildRoot: %{_tmppath}/mbedtls-%{version}-%{release}-root
BuildRequires: cmake
BuildRequires: zlib-devel
BuildRequires: openssl-devel

Provides: mbedtls
Provides: ulyaoth-mbedtls

%description
mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers to include cryptographic and SSL/TLS capabilities in their (embedded) products, facilitating this functionality with a minimal coding footprint.

%prep
%setup -q -n mbedtls-mbedtls-%{version}
sed -i 's|//\(#define POLARSSL_THREADING_C\)|\1|' include/polarssl/config.h
sed -i 's|//\(#define POLARSSL_THREADING_PTHREAD\)|\1|' include/polarssl/config.h

%build
%if 0%{?fedora} >= 18
%cmake -DCMAKE_BUILD_TYPE:String="Release" -DUSE_SHARED_MBEDTLS_LIBRARY:BOOL=TRUE -DENABLE_ZLIB_SUPPORT:BOOL=TRUE -DUSE_PKCS11_HELPER_LIBRARY:BOOL=TRUE .
%else
%cmake -DCMAKE_BUILD_TYPE:String="Release" -DUSE_SHARED_MBEDTLS_LIBRARY:BOOL=TRUE -DENABLE_ZLIB_SUPPORT:BOOL=TRUE .
%endif
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libexecdir}/mbedtls

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_libexecdir}/mbedtls/*
%{_includedir}/polarssl/*
%{_libdir}/*
%dir %{_includedir}/polarssl

%pre

%post
# print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-mbedtls!

Please find the official documentation for mbedtls here:
* https://tls.mbed.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Sep 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.13-1
- Updated to version 1.3.13.

* Thu Aug 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.3.12-1
- Updated to version 1.3.12.

* Tue Jun 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.3.11-2
- Added "POLARSSL_THREADING_PTHREAD" and "POLARSSL_THREADING_C" to compile options.
- Support for Hiawatha web server.

* Sat Jun 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.3.11-1
- Updated to version 1.3.11.

* Sun May 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.3.10-1
- Initial release.