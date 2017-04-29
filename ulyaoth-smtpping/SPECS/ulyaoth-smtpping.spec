Summary:    A simple, portable tool for measuring SMTP server delay, delay variation and throughput.
Name:       ulyaoth-smtpping
Version:    1.1.3
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv2
Group:      Applications/System
URL:        https://github.com/halonsecurity/smtpping
Vendor:     halonsecurity
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/halonsecurity/smtpping/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/smtpping-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake

Provides: smtpping
Provides: ulyaoth-smtpping

%description
A simple, portable tool for measuring SMTP server delay, delay variation and throughput.

%prep
%setup -q -n smtpping-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE:String="Release" -DMAN_INSTALL_DIR=%{_mandir} -DBIN_INSTALL_DIR=%{_bindir}  . 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
%{_bindir}/smtpping
%{_mandir}/man1/smtpping.1.gz

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-smtpping!

Please find the official documentation for smtpping here:
* https://github.com/halonsecurity/smtpping

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Wed Jun 8 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.3-1
- Initial release.