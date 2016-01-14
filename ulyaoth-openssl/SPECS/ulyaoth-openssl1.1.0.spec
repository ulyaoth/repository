AutoReqProv: no
%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl1.1.0
Version:    1.1.0
Release:    0.3.pre2%{?dist}
BuildArch: x86_64
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
%if 0%{?fedora}  == 19
Source0:    http://www.openssl.org/source/openssl-%{version}-pre2.tar.gz
%else
Source0:    https://www.openssl.org/source/openssl-%{version}-pre2.tar.gz
%endif
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora}  == 19
BuildRequires: perl-Pod-MinimumVersion
%endif

Provides: ulyaoth-openssl1.1.0

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%prep
%setup -q -n openssl-%{version}-pre2

%build

# Temp fix for 1.1.0 Alpha 2 see: https://github.com/openssl/openssl/issues/551
wget -O $RPM_BUILD_ROOT/openssl-1.1.0-pre2/util/mkdef.pl https://raw.githubusercontent.com/openssl/openssl/master/util/mkdef.pl
# end temp fix.

./config --openssldir=/usr/local/ulyaoth/ssl/openssl1.1.0 shared
make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/ssl/openssl1.1.0

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/ssl
%dir /usr/local/ulyaoth/ssl/openssl1.1.0
/usr/local/ulyaoth/ssl/openssl1.1.0/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-openssl1.1.0!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun

%changelog
* Thu Jan 14 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.3.pre2
- Updated to OpenSSL 1.1.0 Alpha 2.

* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.2.pre1
- added "shared" to compile options.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.1.pre1
- Initial release with openssl 1.1.0-pre1.