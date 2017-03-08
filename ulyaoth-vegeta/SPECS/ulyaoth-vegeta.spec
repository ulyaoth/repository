
Summary:    Vegeta is a versatile HTTP load testing tool built out of a need to drill HTTP services with a constant request rate.
Name:       ulyaoth-vegeta
Version:    6.2.0
Release:    1%{?dist}
BuildArch: x86_64
License:    The MIT License (MIT)
Group:      Applications/Internet
URL:        https://github.com/tsenart/vegeta
Vendor:     Satoshi
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    vegeta
BuildRoot:  %{_tmppath}/vegeta-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: vegeta
Provides: ulyaoth-vegeta

%description
Vegeta is a versatile HTTP load testing tool built out of a need to drill HTTP services with a constant request rate. It can be used both as a command line utility and a library.

%prep

%build

%install

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/vegeta
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
/usr/bin/vegeta

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-vegeta!

Please find the official documentation for vegeta here:
* https://github.com/tsenart/vegeta

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.2.0-1
- Updated to Vegeta 6.2.0.

* Sat Aug 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.1.1-1
- Updated to Vegeta 6.1.1.

* Wed Apr 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.1.0-1
- Initial release.