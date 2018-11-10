%define debug_package %{nil}

# distribution specific definitions

%if 0%{?fedora} >= 18
BuildRequires: pkcs11-helper-devel
%endif

# end of distribution specific definitions

Summary: mbed TLS is an open source and commercial SSL library licensed by ARM Limited.. mbed TLS used to be called PolarSSL,
Name: ulyaoth-mbedtls2.5
Version: 2.5.1
Release: 2%{?dist}
BuildArch: x86_64
Vendor: ARM Limited.
URL: https://tls.mbed.org/
Packager: Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>

Source0: https://github.com/ARMmbed/mbedtls/archive/mbedtls-%{version}.tar.gz

License: GPLv2 or proprietary

BuildRoot: %{_tmppath}/mbedtls-%{version}-%{release}-root
BuildRequires: ulyaoth-cmake
BuildRequires: zlib-devel
BuildRequires: openssl-devel

Provides: mbedtls
Provides: ulyaoth-mbedtls2.5

Conflicts: ulyaoth-mbedtls
Conflicts: ulyaoth-mbedtls2.1
Conflicts: ulyaoth-mbedtls2.2
Conflicts: ulyaoth-mbedtls2.3
Conflicts: ulyaoth-mbedtls2.4
Conflicts: ulyaoth-mbedtls2.6

%description
mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers to include cryptographic and SSL/TLS capabilities in their (embedded) products, facilitating this functionality with a minimal coding footprint.

%prep
%setup -q -n mbedtls-mbedtls-%{version}
sed -i 's|//\(#define MBEDTLS_THREADING_C\)|\1|' include/mbedtls/config.h
sed -i 's|//\(#define MBEDTLS_THREADING_PTHREAD\)|\1|' include/mbedtls/config.h

%build
%if 0%{?fedora} >= 18
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE:String="Release" -DUSE_SHARED_MBEDTLS_LIBRARY:BOOL=TRUE -DENABLE_ZLIB_SUPPORT:BOOL=TRUE -DUSE_PKCS11_HELPER_LIBRARY:BOOL=TRUE .
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE:String="Release" -DUSE_SHARED_MBEDTLS_LIBRARY:BOOL=TRUE -DENABLE_ZLIB_SUPPORT:BOOL=TRUE .
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
%{_includedir}/mbedtls/*
/usr/lib/*
%dir %{_includedir}/mbedtls

%pre

%post
# print site info
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-mbedtls2.5!

Please find the official documentation for mbedtls here:
* https://tls.mbed.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Thu Nov 16 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.5.1-2
- Added conflict for mbed TLS 2.6.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.5.1-1
- Initial release for mbedtls 2.5.
