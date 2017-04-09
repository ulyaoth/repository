%define debug_package %{nil}

Summary:    the programming language Lua
Name:       ulyaoth-lua5.3
Version:    5.3.4
Release:    2%{?dist}
BuildArch: x86_64
License:    MIT
Group:      Development/Languages
URL:        https://www.lua.org
Vendor:     PUC-Rio
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://www.lua.org/ftp/lua-%{version}.tar.gz
BuildRoot:  %{_tmppath}/lua5.3-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: readline-devel

Provides: lua
Provides: lua5.3
Provides: ulyaoth-lua5.3

%description
Lua is a powerful, fast, lightweight, embeddable scripting language developed by a team at PUC-Rio, the Pontifical Catholic University of Rio de Janeiro in Brazil. Lua is free software used in many products and projects around the world.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       ulyaoth-lua5.3
%description devel
This package contains development files for %{name}.

%package static
Summary:        Static library for %{name}
Group:          System Environment/Libraries
Requires:       ulyaoth-lua5.3
%description static
This package contains the static version of liblua for %{name}.

%prep
%setup -q -n lua-%{version}

%build
make linux %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL_TOP=$RPM_BUILD_ROOT%{_prefix} INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} INSTALL_INC=$RPM_BUILD_ROOT%{_includedir} INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1  

mv $RPM_BUILD_ROOT/usr/lib/lua $RPM_BUILD_ROOT/usr/lib64/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%{_bindir}/lua
%{_bindir}/luac
%{_mandir}/man1/lua*.1*
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.3
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.3

%files devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp

%files static
%{_libdir}/*.a

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lua5.3!

Please find the official documentation for Lua here:
* https://www.lua.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post devel
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lua5.3-devel!

Please find the official documentation for Lua here:
* https://www.lua.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%post static
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lua5.3-static!

Please find the official documentation for Lua here:
* https://www.lua.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun
/sbin/ldconfig

%changelog
* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.4-2
- Installing Lua to default locations.
- Splitting to create a devel and static package.

* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.4-1
- Initial release for Lua 5.3 version 5.3.4.

* Wed Oct 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.3-1
- Initial release for Lua 5.3 version 5.3.3.