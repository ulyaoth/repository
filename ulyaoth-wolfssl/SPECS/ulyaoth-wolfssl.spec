%define debug_package %{nil}

# end of distribution specific definitions

Summary:    The wolfSSL embedded SSL library
Name:       ulyaoth-wolfssl
Version:    3.9.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GNU General Public License
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     wolfSSL Inc
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/wolfSSL/wolfssl/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/wolfssl-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: ulyaoth-openssl1.1.0

%description
The wolfSSL embedded SSL library (formerly CyaSSL) is a lightweight, portable, C-language-based SSL/TLS library targeted at IoT, embedded, and RTOS environments primarily because of its size, speed, and feature set. It works seamlessly in desktop, enterprise, and cloud environments as well. wolfSSL supports industry standards up to the current TLS 1.2 and DTLS 1.2, is up to 20 times smaller than OpenSSL, offers a simple API, an OpenSSL compatibility layer, OCSP and CRL support, is backed by the robust wolfCrypt cryptography library, and much more.

%prep
%setup -q -n wolfssl-%{version}

%build
./autogen.sh
./configure --enable-dtls --enable-keygen --enable-certgen --enable-certreq --enable-certext  --enable-ocsp
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/include/cyassl
%dir /usr/local/include/wolfssl
%dir /usr/local/share/doc/wolfssl
/usr/local/bin/*
/usr/local/lib/*
/usr/local/include/cyassl/*
/usr/local/include/wolfssl/*
/usr/local/share/doc/wolfssl/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-wolfssl!

Please find the official documentation for OpenSSL here:
* https://www.wolfssl.com

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun

%changelog
* Sun Mar 20 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.9.0-1
- Initial release with wolfSSL version 3.9.0.