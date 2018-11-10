%define debug_package %{nil}
%define httpdiff_home /usr/bin

# end of distribution specific definitions

Summary:    Perform the same request against two HTTP servers and diff the results. For best results use in a terminal that supports ANSI escape sequences.
Name:       ulyaoth-httpdiff
Version:    1.0.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GNU GENERAL PUBLIC LICENSE Version 2
Group:      Applications/Internet
URL:        https://github.com/jgrahamc/httpdiff
Vendor:     John Graham-Cumming
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    httpdiff
BuildRoot:  %{_tmppath}/ulyaoth-httpdiff-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: httpdiff
Provides: ulyaoth-httpdiff

Obsoletes: ulyaoth-httpdiff-masterbuild
Obsoletes: ulyaoth-httpdiff = 20160615
Obsoletes: ulyaoth-httpdiff = 20150614
Obsoletes: ulyaoth-httpdiff = 20150404
Obsoletes: ulyaoth-httpdiff = 20150325

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

Thank you for using ulyaoth-httpdiff!

Please find the official documentation for httpdiff here:
* https://github.com/jgrahamc/httpdiff

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER


%preun


%postun


%changelog
* Sun Jun 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 20160615-1
- Updating to today's master branch.
- Renamed rpm to ulyaoth-httpdiff.

* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150614-1
- Updating to today's master branch.

* Sat Apr 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150404-1
- Updating to today's master branch.

* Wed Mar 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 20150325-1
- Initial release for httpdiff.