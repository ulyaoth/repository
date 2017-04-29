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
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lua/SOURCES/ulyaoth-lua5.3.conf
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
export C_INCLUDE_PATH=/usr/local/ulyaoth/lua5.3/include
export LIBRARY_PATH=/usr/local/ulyaoth/lua5.3/lib64
export LD_RUN_PATH=/usr/local/ulyaoth/lua5.3/lib64

make linux %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL_TOP=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3 INSTALL_BIN=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/bin INSTALL_INC=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/include INSTALL_LIB=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/lib64 INSTALL_MAN=$RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/man/man1  

rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/share

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/lib/lua $RPM_BUILD_ROOT/usr/local/ulyaoth/lua5.3/lib64/

%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-lua5.3.conf
	
ln -s /usr/local/ulyaoth/lua5.3/bin/lua $RPM_BUILD_ROOT/usr/bin/lua5.3
ln -s /usr/local/ulyaoth/lua5.3/bin/luac $RPM_BUILD_ROOT/usr/bin/luac5.3

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
/usr/local/ulyaoth/lua5.3/bin/lua
/usr/local/ulyaoth/lua5.3/bin/luac
%doc /usr/local/ulyaoth/lua5.3/man/man1/lua*.1*
%dir /usr/local/ulyaoth/lua5.3/lib64/lua
%dir /usr/local/ulyaoth/lua5.3/lib64/lua/5.3
%config(noreplace) /etc/ld.so.conf.d/ulyaoth-lua5.3.conf
/usr/bin/lua5.3
/usr/bin/luac5.3

%files devel
/usr/local/ulyaoth/lua5.3/include/l*.h
/usr/local/ulyaoth/lua5.3/include/l*.hpp

%files static
/usr/local/ulyaoth/lua5.3/lib64/*.a

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-lua5.3!

Please find the official documentation for Lua here:
* https://www.lua.org/

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

Thank you for using ulyaoth-lua5.3-devel!

Please find the official documentation for Lua here:
* https://www.lua.org/

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

Thank you for using ulyaoth-lua5.3-static!

Please find the official documentation for Lua here:
* https://www.lua.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun
/sbin/ldconfig

%changelog
* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.4-2
- Fixed directory structure.
- Splitting to create a devel and static package.

* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.4-1
- Initial release for Lua 5.3 version 5.3.4.

* Wed Oct 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.3-1
- Initial release for Lua 5.3 version 5.3.3.