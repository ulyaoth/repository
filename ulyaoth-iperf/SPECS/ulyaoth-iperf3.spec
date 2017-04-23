
Summary:    iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks.
Name:       ulyaoth-iperf3
Version:    3.1.7
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD style license
Group:      Applications/Internet
URL:        https://github.com/esnet/iperf
Vendor:     University of California
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/esnet/iperf/archive/%{version}.tar.gz
BuildRoot:  %{_tmppath}/iperf3-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: iperf
Provides: iperf3
Provides: ulyaoth-iperf3

%description
iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, protocols, and buffers. For each test it reports the bandwidth, loss, and other parameters.

This version, sometimes referred to as iperf3, is a redesign of an original version developed at NLANR/DAST. iperf3 is a new implementation from scratch, with the goal of a smaller, simpler code base, and a library version of the functionality that can be used in other programs. iperf3 also has a number of features found in other tools such as nuttcp and netperf, but were missing from the original iperf. These include, for example, a zero-copy mode and optional JSON output. Note that iperf3 is not backwards compatible with the original iperf.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing applications that use %{name}.

%prep
%setup -q -n iperf-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files

%post
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

%preun

%postun

%changelog
* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 3.1.7-1
- Initial release.