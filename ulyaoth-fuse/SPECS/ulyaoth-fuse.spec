%define fuse_download_version 2_9_7

Summary:    FUSE (Filesystem in Userspace) is an interface for userspace programs to export a filesystem to the Linux kernel.
Name:       ulyaoth-fuse
Version:    2.9.7
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv2
Group:      System Environment/Kernel
URL:        https://github.com/libfuse/libfuse
Vendor:     FUSE
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:	https://github.com/libfuse/libfuse/releases/download/fuse-%{version}/fuse-%{version}.tar.gz
BuildRoot:  %{_tmppath}/fuse-%{version}-%{release}-root-%(%{__id_u} -n)

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

Requires: curl
Requires: openssl
Requires: mailcap
Requires: libxml2
Requires: libstdc++

Provides: fuse-libs
Provides: fuse-devel
Provides: ulyaoth-fuse

%description
FUSE (Filesystem in Userspace) is an interface for userspace programs to export a filesystem to the Linux kernel. The FUSE project consists of two components: the fuse kernel module (maintained in the regular kernel repositories) and the libfuse userspace library (maintained in this repository). libfuse provides the reference implementation for communicating with the FUSE kernel module.

%prep
%setup -q -n fuse-%{version}

%build
export MOUNT_FUSE_PATH=%{_sbindir}
./configure --enable-lib --enable-util --enable-example --prefix=%{_prefix} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir} --bindir=%{_bindir} --sbindir=%{_sbindir} --mandir=%{_mandir} 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
%dir %{_includedir}/fuse

%{_sysconfdir}/init.d/fuse
%{_sysconfdir}/udev/rules.d/99-fuse.rules
%{_sbindir}/mount.fuse
%{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%{_includedir}/fuse.h
%{_includedir}/fuse/cuse_lowlevel.h
%{_includedir}/fuse/fuse.h
%{_includedir}/fuse/fuse_common.h
%{_includedir}/fuse/fuse_common_compat.h
%{_includedir}/fuse/fuse_compat.h
%{_includedir}/fuse/fuse_lowlevel.h
%{_includedir}/fuse/fuse_lowlevel_compat.h
%{_includedir}/fuse/fuse_opt.h
%{_includedir}/ulockmgr.h
%{_libdir}/libfuse.a
%{_libdir}/libfuse.la
%{_libdir}/libfuse.so
%{_libdir}/libfuse.so.2
%{_libdir}/libfuse.so.%{version}
%{_libdir}/libulockmgr.a
%{_libdir}/libulockmgr.la
%{_libdir}/libulockmgr.so
%{_libdir}/libulockmgr.so.1
%{_libdir}/libulockmgr.so.1.0.1
%{_libdir}/pkgconfig/fuse.pc
%{_mandir}/man1/fusermount.1.gz
%{_mandir}/man1/ulockmgr_server.1.gz
%{_mandir}/man8/mount.fuse.8.gz


%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-fuse!

Please find the official documentation for fuse here:
* https://github.com/libfuse/libfuse

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sat Jun 25 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.7-1
- Updated Fuse to 2.9.7.

* Sun May 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.6-1
- Updated Fuse to 2.9.6.

* Sun Apr 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.5-1
- Initial release.