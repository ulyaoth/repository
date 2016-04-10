
Summary:    FUSE (Filesystem in Userspace) is an interface for userspace programs to export a filesystem to the Linux kernel.
Name:       ulyaoth-libfuse
Version:    2.9.5
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv2
Group:      Applications/Internet
URL:        https://github.com/libfuse/libfuse
Vendor:     libfuse
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/libfuse/libfuse/releases/download/fuse_%{version}/fuse-%{version}.tar.gz
BuildRoot:  %{_tmppath}/libfuse-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc
BuildRequires: libstdc++-devel
BuildRequires: gcc-c++
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: mailcap
BuildRequires: automake
BuildRequires: libcurl-devel
BuildRequires: git
BuildRequires: make

Provides: fuse-libs
Provides: fuse-devel
Provides: ulyaoth-libfuse

%description
FUSE (Filesystem in Userspace) is an interface for userspace programs to export a filesystem to the Linux kernel. The FUSE project consists of two components: the fuse kernel module (maintained in the regular kernel repositories) and the libfuse userspace library (maintained in this repository). libfuse provides the reference implementation for communicating with the FUSE kernel module.

%prep
%setup -q -n libfuse-%{version}

%build
./autogen.sh 
./configure --prefix=/usr 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-libfuse!

Please find the official documentation for libfuse here:
* https://github.com/libfuse/libfuse

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Apr 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.5-1
- Initial release.