#
%define debug_package %{nil}

Summary:    iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks.
Name:       ulyaoth-iperf2
Version:    2.0.10
Release:    1%{?dist}
BuildArch: x86_64
License:    BSD
Group:      Applications/Internet
URL:        http://sourceforge.net/projects/iperf2
Vendor:     University of California
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://sourceforge.net/projects/iperf2/files/iperf-%{version}.tar.gz
BuildRoot:  %{_tmppath}/iperf2-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: iperf2
Provides: ulyaoth-iperf2

%description
iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, protocols, and buffers. For each test it reports the bandwidth, loss, and other parameters.

Iperf 2 vs iperf 3 major differences: Iperf 3 is a rewrite which does not support interoperability with iperf 2. The iperf 2 code base supports threaded operation where iperf 3 is single threaded.

%prep
%setup -q -n iperf-%{version}

%build
./configure --prefix=/usr --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} --sharedstatedir=%{_sharedstatedir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datarootdir} --datadir=%{_datadir} --infodir=%{_infodir} --mandir=%{_mandir} --docdir=/usr/share/doc
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
/usr/bin/iperf
/usr/share/man/man1/iperf.1.gz

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-iperf2!

Please find the official documentation for iperf2 here:
* http://sourceforge.net/projects/iperf2

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.0.10-1
- Updated to Iperf 2.0.10.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.0.9-1
- Initial release.