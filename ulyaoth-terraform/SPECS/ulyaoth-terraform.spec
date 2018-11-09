Summary:    Terraform is a tool for building, changing, and combining infrastructure safely and efficiently.
Name:       ulyaoth-terraform
Version:    0.11.10
Release:    1%{?dist}
BuildArch: x86_64
License:    Mozilla Public License, version 2.0
Group:      Applications/Internet
URL:        https://www.terraform.io/
Vendor:     Hashicorp
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    terraform
BuildRoot:  %{_tmppath}/terraform-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: terraform
Provides: hashicorp-terraform
Provides: ulyaoth-terraform

%description
Terraform is a tool for building, changing, and combining infrastructure safely and efficiently.

%prep

%build

%install

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/terraform
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
/usr/bin/terraform

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-terraform!

Please find the official documentation for Terraform here:
* https://www.terraform.io/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 0.11.10-1
- Updated to Terraform 0.11.10.

* Sat Nov 18 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.11.0-1
- Updated to Terraform 0.11.0.

* Wed Aug 9 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.10.0-1
- Updated to Terraform 0.10.0.

* Tue Jul 4 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.9.11-1
- Updated to Terraform 0.9.11.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.9.10-1
- Updated to Terraform 0.9.10.

* Fri May 26 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 0.9.6-1
- Updated to Terraform 0.9.6.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.5-1
- Updated to Terraform 0.9.5.

* Sat Apr 29 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.4-1
- Updated to Terraform 0.9.4.

* Fri Apr 14 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.3-1
- Updated to Terraform 0.9.3.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.2-1
- Updated to Terraform 0.9.2.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.0-1
- Updated to Terraform 0.9.0.

* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.8.8-1
- Updated to Terraform 0.8.8.

* Wed Feb 15 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.8.6-1
- Updated to Terraform 0.8.6.

* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.13-1
- Updated to Terraform 0.7.13.

* Sun Nov 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.10-1
- Updated to Terraform 0.7.10.

* Sat Nov 5 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.9-1
- Updated to Terraform 0.7.9.

* Sat Oct 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.7-1
- Updated to Terraform 0.7.7.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.6-1
- Updated to Terraform 0.7.6.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.4-1
- Updated to Terraform 0.7.4.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.3-1
- Updated to Terraform 0.7.3.

* Sat Aug 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.2-1
- Updated to Terraform 0.7.2.

* Sat Aug 20 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.1-1
- Updated to Terraform 0.7.1.

* Sat Aug 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-1
- Updated to official release of Terraform 0.7.0.

* Sat Jul 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-0.4.rc4
- Updated to Terraform 0.7.0-rc4.

* Tue Jul 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-0.3.rc3
- Updated to Terraform 0.7.0-rc3.

* Thu Jun 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-0.2.rc2
- Updated to Terraform 0.7.0-rc2.

* Mon Jun 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-0.1.rc1
- Initial release with Terraform 0.7.0-rc1.