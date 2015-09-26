%define debug_package %{nil}
%define httpdiff_home /usr/bin

# end of distribution specific definitions

Summary:    Perform the same request against two HTTP servers and diff the results. For best results use in a terminal that supports ANSI escape sequences.
Name:       ulyaoth-httpdiff-masterbuild
Version:    20150614
Release:    1%{?dist}
BuildArch: x86_64
License:    GNU GENERAL PUBLIC LICENSE Version 2
Group:      Applications/Internet
URL:        https://github.com/jgrahamc/httpdiff
Vendor:     John Graham-Cumming
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
Source0:    httpdiff
BuildRoot:  %{_tmppath}/ulyaoth-httpdiff-masterbuild-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: httpdiff
Provides: ulyaoth-httpdiff
Provides: ulyaoth-httpdiff-masterbuild

%description
Perform the same request against two HTTP servers and diff the results. For best results use in a terminal that supports ANSI escape sequences.

%prep

%build

%install

%{__mkdir} -p $RPM_BUILD_ROOT%{httpdiff_home}
%{__install} -m755 %SOURCE0 \
        $RPM_BUILD_ROOT%{httpdiff_home}/httpdiff
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
%{httpdiff_home}/httpdiff


%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-httpdiff-masterbuild!

Please find the official documentation for httpdiff here:
* https://github.com/jgrahamc/httpdiff

For any additional help please visit my forum at:
* http://www.ulyaoth.net

----------------------------------------------------------------------
BANNER


%preun


%postun


%changelog
* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150614-1
- Updating to today's master branch.

* Sat Apr 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150404-1
- Updating to today's master branch.

* Wed Mar 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150325-1
- Initial release for httpdiff.