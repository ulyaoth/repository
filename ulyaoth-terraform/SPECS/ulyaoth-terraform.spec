Summary:    Terraform is a tool for building, changing, and combining infrastructure safely and efficiently.
Name:       ulyaoth-terraform
Version:    0.7.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Mozilla Public License, version 2.0
Group:      Applications/Internet
URL:        https://www.terraform.io/
Vendor:     Hashicorp
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
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

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Mon Jun 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.7.0-1
- Initial release with Terraform 0.7.0-rc1.