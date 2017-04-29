Summary:    CMake is an open-source, cross-platform family of tools designed to build, test and package software.
Name:       ulyaoth-cmake
Version:    3.8.0
Release:    1%{?dist}
BuildArch: x86_64
License:    OSI-approved BSD 3-clause License
Group:      System Environment/Libraries
URL:        https://cmake.org/
Vendor:     Kitware, Inc. and Contributors
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/Kitware/CMake/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/cmake-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ncurses-devel

Provides: cmake
Provides: ulyaoth-cmake

%description
CMake is an open-source, cross-platform family of tools designed to build, test and package software. CMake is used to control the software compilation process using simple platform and compiler independent configuration files, and generate native makefiles and workspaces that can be used in the compiler environment of your choice. The suite of CMake tools were created by Kitware in response to the need for a powerful, cross-platform build environment for open-source projects such as ITK and VTK.

%prep
%setup -q -n CMake-%{version}

%build

./configure --prefix=/usr
gmake %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/bin/ccmake
/usr/bin/cmake
/usr/bin/cpack
/usr/bin/ctest

%dir /usr/doc/cmake-3.8  
%doc /usr/doc/cmake-3.8/Copyright.txt
%doc /usr/doc/cmake-3.8/cmcompress/Copyright.txt
%doc /usr/doc/cmake-3.8/cmcurl/COPYING
%doc /usr/doc/cmake-3.8/cmlibarchive/COPYING
%doc /usr/doc/cmake-3.8/cmliblzma/COPYING
%doc /usr/doc/cmake-3.8/cmlibrhash/COPYING
%doc /usr/doc/cmake-3.8/cmlibrhash/README
%doc /usr/doc/cmake-3.8/cmlibuv/LICENSE
%doc /usr/doc/cmake-3.8/cmsys/Copyright.txt
%doc /usr/doc/cmake-3.8/cmzlib/Copyright.txt

/usr/share/aclocal/cmake.m4

%dir /usr/share/cmake-3.8
/usr/share/cmake-3.8/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-cmake!

Please find the official documentation for cmake here:
* https://cmake.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%postun

%changelog
* Mon Apr 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.8.0-1
- Initial release with cmake 3.8.0.