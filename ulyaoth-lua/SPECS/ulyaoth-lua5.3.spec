%define debug_package %{nil}

Summary:    the programming language Lua
Name:       ulyaoth-lua5.3
Version:    5.3.3
Release:    1%{?dist}
BuildArch: x86_64
License:    MIT
Group:      Development/Languages
URL:        https://www.lua.org
Vendor:     PUC-Rio
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://www.lua.org/ftp/lua-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lua/SOURCES/ulyaoth-lua5.3.conf
BuildRoot:  %{_tmppath}/lua5.3-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: readline-devel

Requires: readline

Provides: lua5.3
Provides: ulyaoth-lua5.3

%description
Lua is a powerful, fast, lightweight, embeddable scripting language developed by a team at PUC-Rio, the Pontifical Catholic University of Rio de Janeiro in Brazil. Lua is free software used in many products and projects around the world.

%prep
%setup -q -n lua-%{version}

%build
make linux %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/lua/5.3
mkdir -p $RPM_BUILD_ROOT/usr/bin

make DESTDIR=$RPM_BUILD_ROOT INSTALL_TOP=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua/5.3 install

rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/lua/5.3/lib/lua
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/lua/5.3/share

%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-lua5.3.conf
	
ln -s /usr/local/ulyaoth/lua/5.3/bin/lua $RPM_BUILD_ROOT/usr/bin/lua5.3
ln -s /usr/local/ulyaoth/lua/5.3/bin/luac $RPM_BUILD_ROOT/usr/bin/luac5.3

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/bin/lua5.3
/usr/bin/luac5.3
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/ulyaoth-lua5.3.conf

%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/lua
%dir /usr/local/ulyaoth/lua/5.3

%dir /usr/local/ulyaoth/lua/5.3/bin
/usr/local/ulyaoth/lua/5.3/bin/lua
/usr/local/ulyaoth/lua/5.3/bin/luac

%dir /usr/local/ulyaoth/lua/5.3/lib
/usr/local/ulyaoth/lua/5.3/lib/liblua.a

%dir /usr/local/ulyaoth/lua/5.3/include
/usr/local/ulyaoth/lua/5.3/include/lauxlib.h
/usr/local/ulyaoth/lua/5.3/include/luaconf.h
/usr/local/ulyaoth/lua/5.3/include/lua.h
/usr/local/ulyaoth/lua/5.3/include/lua.hpp
/usr/local/ulyaoth/lua/5.3/include/lualib.h

%dir /usr/local/ulyaoth/lua/5.3/man
%dir /usr/local/ulyaoth/lua/5.3/man/man1
/usr/local/ulyaoth/lua/5.3/man/man1/lua.1
/usr/local/ulyaoth/lua/5.3/man/man1/luac.1

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lua5.3!

Please find the official documentation for Lua here:
* https://www.lua.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun
/sbin/ldconfig

%changelog
* Wed Oct 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.3-1
- Initial release for Lua 5.3 version 5.3.3.