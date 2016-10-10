AutoReqProv: no
%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl1.0.1
Version:    1.0.1u
Release:    1%{?dist}
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

Provides: ulyaoth-openssl1.0.1
Provides: ulyaoth-openssl1.0.1u

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%prep
%setup -q -n openssl-%{version}

%build
./config --openssldir=/usr/local/ulyaoth/ssl/openssl1.0.1 no-ssl2 no-ssl3 shared
make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/ssl/openssl1.0.1

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
%dir /usr/local/ulyaoth/ssl
%dir /usr/local/ulyaoth/ssl/openssl1.0.1
/usr/local/ulyaoth/ssl/openssl1.0.1/*
/etc/ld.so.conf.d/ulyaoth-openssl1.0.1.conf

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.0.1!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun

%changelog
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