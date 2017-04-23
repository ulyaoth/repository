
Summary:    a Just-In-Time Compiler for Lua.
Name:       ulyaoth-luajit
Version:    2.0.4
Release:    1%{?dist}
BuildArch: x86_64
License:    mit
Group:      Applications/Internet
URL:        https://luajit.org/
Vendor:     Mike Pall
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://luajit.org/download/LuaJIT-%{version}.tar.gz
BuildRoot:  %{_tmppath}/luajit-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: luajit
Provides: ulyaoth-luajit

%description
LuaJIT is a Just-In-Time Compiler (JIT) for the Lua programming language. Lua is a powerful, dynamic and light-weight programming language. It may be embedded or used as a general-purpose, stand-alone language.

%package libs
Summary: FLibrary files for applications which will use luajit
Group: System Environment/Libraries
Provides: ulyaoth-luajit-libs
%description libs
The luajit-libs package contains the libraries that are used by various applications which support luajit.

%package devel
Summary: Files for development of applications which will use luajit
Group: Development/Libraries
Requires: ulyaoth-luajit-libs
Provides: ulyaoth-luajit-devel
%description devel
The %{name}-devel package contains libraries and header files for developing applications that use %{name}.

%package static
Summary: Libraries for static linking of applications which will use luajit
Group: Development/Libraries
Requires: ulyaoth-luajit-devel
Provides: ulyaoth-luajit-static
%description static
The openssl-luajit package contains static libraries needed for static linking of applications which support luajit.

%prep
%setup -q -n LuaJIT-%{version}

%build
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)

%files libs

%files devel

%files static

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-luajit!

Please find the official documentation for luajit here:
* https://luajit.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%post libs
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-luajit-libs!

Please find the official documentation for luajit here:
* https://luajit.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%post devel
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-luajit-devel!

Please find the official documentation for luajit here:
* https://luajit.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%post static
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-luajit-static!

Please find the official documentation for luajit here:
* https://luajit.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.0.4-1
- Initial release.