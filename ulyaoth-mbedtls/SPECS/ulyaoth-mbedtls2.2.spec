%define debug_package %{nil}

# distribution specific definitions

%if 0%{?fedora} >= 18
BuildRequires: pkcs11-helper-devel
%endif

# end of distribution specific definitions

Summary: mbed TLS is an open source and commercial SSL library licensed by ARM Limited.. mbed TLS used to be called PolarSSL,
Name: ulyaoth-mbedtls2.2
Version: 2.2.1
Release: 2%{?dist}
BuildArch: x86_64
Vendor: ARM Limited.
URL: https://tls.mbed.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://github.com/ARMmbed/mbedtls/archive/mbedtls-%{version}.tar.gz

License: GPLv2 or proprietary

BuildRoot: %{_tmppath}/mbedtls-%{version}-%{release}-root
BuildRequires: cmake
BuildRequires: zlib-devel
BuildRequires: openssl-devel

Provides: mbedtls
Provides: ulyaoth-mbedtls2.2

Conflicts: ulyaoth-mbedtls
Conflicts: ulyaoth-mbedtls2.1

%description
mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers to include cryptographic and SSL/TLS capabilities in their (embedded) products, facilitating this functionality with a minimal coding footprint.

%prep
%setup -q -n mbedtls-mbedtls-%{version}
sed -i 's|//\(#define MBEDTLS_THREADING_C\)|\1|' include/mbedtls/config.h
sed -i 's|//\(#define MBEDTLS_THREADING_PTHREAD\)|\1|' include/mbedtls/config.h

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
%{_includedir}/mbedtls/*
%{_libdir}/*
%dir %{_includedir}/mbedtls

%pre

%post
# print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-mbedtls2.2!

Please find the official documentation for mbedtls here:
* https://tls.mbed.org

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.1-2
- Removed obsoletes due to problems.

* Fri Jan 8 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.1-1
- Updated to mbed TLS 2.2.1.

* Sat Nov 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.0-1
- Initial release for version 2.2.0.
