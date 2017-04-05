
Summary:    Let's Encrypt client and ACME library written in Go.
Name:       ulyaoth-lego
Version:    0.3.1
Release:    1%{?dist}
BuildArch: x86_64
License:    The MIT License (MIT)
Group:      Applications/Internet
URL:        https://github.com/xenolf/lego
Vendor:     xenolf
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    lego
BuildRoot:  %{_tmppath}/lego-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: lego
Provides: ulyaoth-lego

%description
Let's Encrypt client and ACME library written in Go.

%prep

%build

%install

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/bin/lego
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
/usr/bin/lego

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lego!

Please find the official documentation for lego here:
* https://github.com/xenolf/lego

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Thu Apr 6 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.3.1-1
- Initial release.