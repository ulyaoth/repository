
Summary:    iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks.
Name:       ulyaoth-iperf3
Version:    3.3
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD
Group:      Applications/Internet
URL:        https://github.com/esnet/iperf
Vendor:     University of California
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    https://github.com/esnet/iperf/archive/%{version}.tar.gz
BuildRoot:  %{_tmppath}/iperf3-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: iperf3
Provides: ulyaoth-iperf3

%description
iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, protocols, and buffers. For each test it reports the bandwidth, loss, and other parameters.

This version, sometimes referred to as iperf3, is a redesign of an original version developed at NLANR/DAST. iperf3 is a new implementation from scratch, with the goal of a smaller, simpler code base, and a library version of the functionality that can be used in other programs. iperf3 also has a number of features found in other tools such as nuttcp and netperf, but were missing from the original iperf. These include, for example, a zero-copy mode and optional JSON output. Note that iperf3 is not backwards compatible with the original iperf.

%package libs
Summary: FLibrary files for applications which will use iperf3
Group: System Environment/Libraries
Provides: ulyaoth-iperf3-libs
%description libs
The iperf3-libs package contains the libraries that are used by various applications which support iperf3.

%package devel
Summary: Files for development of applications which will use iperf3
Group: Development/Libraries
Requires: ulyaoth-iperf3-libs
Provides: ulyaoth-iperf3-devel
%description devel
The %{name}-devel package contains libraries and header files for developing applications that use %{name}.

%package static
Summary: Libraries for static linking of applications which will use iperf3
Group: Development/Libraries
Requires: ulyaoth-iperf3-devel
Provides: ulyaoth-iperf3-static
%description static
The openssl-iperf3 package contains static libraries needed for static linking of applications which support iperf3.

%prep
%setup -q -n iperf-%{version}

%build
./configure --prefix=/usr --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} --sharedstatedir=%{_sharedstatedir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datarootdir} --datadir=%{_datadir} --infodir=%{_infodir} --mandir=%{_mandir} --docdir=/usr/share/doc
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/bin/iperf3
%doc /usr/share/man/man1/iperf3.1.gz
%doc /usr/share/man/man3/libiperf.3.gz

%files libs
/usr/lib64/libiperf.so
/usr/lib64/libiperf.so.0
/usr/lib64/libiperf.so.0.0.0

%files devel
/usr/include/iperf_api.h
/usr/lib64/libiperf.so
/usr/lib64/libiperf.so.0
/usr/lib64/libiperf.so.0.0.0

%files static
/usr/lib64/libiperf.a
/usr/lib64/libiperf.la

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-iperf3!

Please find the official documentation for iperf3 here:
* https://github.com/esnet/iperf

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

Thank you for using ulyaoth-iperf3-libs!

Please find the official documentation for iperf3 here:
* https://github.com/esnet/iperf

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

Thank you for using ulyaoth-iperf3-devel!

Please find the official documentation for iperf3 here:
* https://github.com/esnet/iperf

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

Thank you for using ulyaoth-iperf3-static!

Please find the official documentation for iperf3 here:
* https://github.com/esnet/iperf

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 3.3-1
- Updated to Iperf 3.3.

* Sat Jul 1 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.2-1
- Updated to Iperf 3.2.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.1.7-1
- Initial release.