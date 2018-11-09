
Summary:    Msktutil creates user or computer accounts in Active Directory.
Name:       ulyaoth-msktutil
Version:    1.1.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv3
Group:      Applications/System
URL:        https://sourceforge.net/projects/msktutil/
Vendor:     GNU
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.com>
Source0:    https://sourceforge.net/projects/msktutil/files/msktutil-1.1.tar.bz2
BuildRoot:  %{_tmppath}/msktutil-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: openldap-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: krb5-devel

Requires: openldap
Requires: krb5-libs
Requires: cyrus-sasl-lib

Provides: msktutil
Provides: ulyaoth-msktutil

%description
Msktutil creates user or computer accounts in Active Directory, creates Kerberos keytabs on Unix/Linux systems, adds and removes principals to and from keytabs and changes the user or computer account's password.

%prep
%setup -q -n msktutil-1.1

%build
./configure --prefix=/usr --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} --sharedstatedir=%{_sharedstatedir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datarootdir} --datadir=%{_datadir} --infodir=%{_infodir} --mandir=%{_mandir} --docdir=/usr/share/doc
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/sbin/msktutil
%doc /usr/share/man/man1/msktutil.1.gz

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-msktutil!

Please find the official documentation for msktutil here:
* https://sourceforge.net/projects/msktutil/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sbagmeijer@ulyaoth.com> 1.1.0-1
- Updated to version 1.1.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.0-1
- Initial release.