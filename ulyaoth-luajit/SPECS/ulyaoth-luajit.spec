%global debug_package %{nil}

Summary:    a Just-In-Time Compiler for Lua.
Name:       ulyaoth-luajit
Version:    2.0.5
Release:    1%{?dist}
BuildArch: x86_64
License:    mit
Group:      Applications/Internet
URL:        https://luajit.org/
Vendor:     Mike Pall
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
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
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/bin/luajit
/usr/bin/luajit-2.0.5
%dir /usr/share/luajit-2.0.5
%dir /usr/share/luajit-2.0.5/jit
/usr/share/luajit-2.0.5/jit/bc.lua
/usr/share/luajit-2.0.5/jit/bcsave.lua
/usr/share/luajit-2.0.5/jit/dis_arm.lua
/usr/share/luajit-2.0.5/jit/dis_mips.lua
/usr/share/luajit-2.0.5/jit/dis_mipsel.lua
/usr/share/luajit-2.0.5/jit/dis_ppc.lua
/usr/share/luajit-2.0.5/jit/dis_x64.lua
/usr/share/luajit-2.0.5/jit/dis_x86.lua
/usr/share/luajit-2.0.5/jit/dump.lua
/usr/share/luajit-2.0.5/jit/v.lua
/usr/share/luajit-2.0.5/jit/vmdef.lua
%doc /usr/share/man/man1/luajit.1.gz

%files libs
%{_libdir}/libluajit-5.1.so
%{_libdir}/libluajit-5.1.so.2
%{_libdir}/libluajit-5.1.so.2.0.5

%files devel
%{_libdir}/libluajit-5.1.so
%{_libdir}/libluajit-5.1.so.2
%{_libdir}/libluajit-5.1.so.2.0.5
/usr/include/luajit-2.0/lauxlib.h
/usr/include/luajit-2.0/lua.h
/usr/include/luajit-2.0/lua.hpp
/usr/include/luajit-2.0/luaconf.h
/usr/include/luajit-2.0/luajit.h
/usr/include/luajit-2.0/lualib.h
%{_libdir}/pkgconfig/luajit.pc

%files static
%{_libdir}/libluajit-5.1.a

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
* Sat May 6 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.0.5-1
- Updated LuaJIT to 2.0.5.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.0.4-1
- Initial release.