%define fuse_download_version 3_0_0

Summary:    FUSE (Filesystem in Userspace) is an interface for userspace programs to export a filesystem to the Linux kernel.
Name:       ulyaoth-fuse
Version:    3.0.0
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

%dir %{_includedir}/fuse3

/etc/init.d/fuse3

/usr/bin/fusermount3
/usr/sbin/mount.fuse3

%{_includedir}/fuse3/cuse_lowlevel.h
%{_includedir}/fuse3/fuse.h
%{_includedir}/fuse3/fuse_common.h
%{_includedir}/fuse3/fuse_lowlevel.h
%{_includedir}/fuse3/fuse_opt.h

%{_libdir}/libfuse3.a
%{_libdir}/libfuse3.la
%{_libdir}/libfuse3.so
%{_libdir}/libfuse3.so.3
%{_libdir}/libfuse3.so.3.0.0
%{_libdir}/pkgconfig/fuse3.pc
%{_libdir}/udev/rules.d/99-fuse3.rules

%{_mandir}/man1/fusermount3.1.gz
%{_mandir}/man8/mount.fuse.8.gz


%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-fuse!

Please find the official documentation for fuse here:
* https://github.com/libfuse/libfuse

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.0.0-1
- Updated Fuse to 3.0.0.

* Sat Jun 25 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.7-1
- Updated Fuse to 2.9.7.

* Sun May 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.6-1
- Updated Fuse to 2.9.6.

* Sun Apr 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.9.5-1
- Initial release.