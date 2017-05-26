Summary:    The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP Legacy binary databases.
Name:       ulyaoth-geoipupdate
Version:    2.4.0
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv2
Group:      Applications/System
URL:        http://dev.maxmind.com/geoip/geoipupdate/
Vendor:     MaxMind, Inc
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    https://github.com/maxmind/geoipupdate/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/geoipupdate-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: zlib-devel
BuildRequires: curl-devel

Requires: zlib
Requires: curl

Provides: geoipupdate
Provides: ulyaoth-geoipupdate

%description
The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP Legacy binary databases. CSV databases are not supported.

%prep
%setup -q -n geoipupdate-%{version}

%build
./bootstrap
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/doc/geoipupdate
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/GeoIP
%{__mv} %{_builddir}/geoipupdate-%{version}/ChangeLog.md $RPM_BUILD_ROOT%{_datadir}/doc/geoipupdate/
%{__mv} %{_builddir}/geoipupdate-%{version}/LICENSE $RPM_BUILD_ROOT%{_datadir}/doc/geoipupdate/
%{__mv} %{_builddir}/geoipupdate-%{version}/README.md $RPM_BUILD_ROOT%{_datadir}/doc/geoipupdate/
  
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
%docdir /usr/share/doc/geoipupdate

%dir %{_datadir}/GeoIP

%{_bindir}/geoipupdate
%{_mandir}/man1/geoipupdate.1.gz
%{_mandir}/man5/GeoIP.conf.5.gz
%{_sysconfdir}/GeoIP.conf

%doc %{_datadir}/doc/geoipupdate/ChangeLog.md
%doc %{_datadir}/doc/geoipupdate/GeoIP.conf.default
%doc %{_datadir}/doc/geoipupdate/LICENSE
%doc %{_datadir}/doc/geoipupdate/README.md

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-geoipupdate!

Please find the official documentation for geoipupdate here:
* http://dev.maxmind.com/geoip/geoipupdate/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Fri May 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.4.0-1
- Updated GeoIP Update to 2.4.0.

* Mon Apr 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.3.1-1
- Updated to GeoIP Update 2.3.1.

* Thu Dec 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.2-3
- Missed creating required dir "/usr/share/GeoIP".

* Thu Dec 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.2-2
- Fixed mistake with config directory.

* Wed Nov 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 2.2.2-1
- Initial release.