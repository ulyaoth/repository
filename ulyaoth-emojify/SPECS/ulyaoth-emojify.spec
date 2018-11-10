%define debug_package %{nil}

Summary:    Emoji on the command line
Name:       ulyaoth-emojify
Version:    2.0.0
Release:    1%{?dist}
BuildArch: x86_64
License:    The MIT License (MIT)
Group:      Applications/Internet
URL:        https://github.com/mrowa44/emojify
Vendor:     mrowa44
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    https://github.com/mrowa44/emojify/archive/%{version}.tar.gz
BuildRoot:  %{_tmppath}/emojify-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: emojify
Provides: ulyaoth-emojify

%description
THIS IS A VERY USEFUL SCRIPT. IT WILL ABSOLUTELY BOOST YOUR PRODUCTIVITY AND HELP YOU IN YOUR DAILY WORK.

%prep
%setup -q -n emojify-%{version}

%build

%install

# install binary file
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mv} %{_builddir}/emojify-%{version}/emojify $RPM_BUILD_ROOT/usr/bin/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%attr(755, root, root) /usr/bin/emojify

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-emojify!

Please find the official documentation for emojify here:
* https://github.com/mrowa44/emojify

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sat May 6 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.0.0-1
- Updated Emojify to 2.0.0.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.2-1
- Initial release.