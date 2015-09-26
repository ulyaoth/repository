#
%define fcgiwrap_home %{_sbindir}
%define fcgiwrap_user fcgiwrap
%define fcgiwrap_group fcgiwrap

Summary: Simple FastCGI wrapper for CGI scripts.
Name: ulyaoth-fcgiwrap
Version: 1.1.0
Release: 1%{?dist}
BuildArch: x86_64
Vendor: Grzegorz Nosek <root@localdomain.pl>
URL: http://nginx.localdomain.pl/wiki/FcgiWrap
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
License: MIT
Group: System Environment/Daemons

Source0: fcgiwrap.tar.gz

BuildRoot: %{_tmppath}/fcgiwrap-root
BuildRequires: autoconf
BuildRequires: fcgi-devel
Requires: spawn-fcgi

Provides: fcgiwrap
Provides: ulyaoth-fcgiwrap

%description
fcgiwrap is a simple server for running CGI applications over FastCGI. It hopes to provide clean CGI support to Nginx (and other web servers that may need it).

%prep
%setup -q -n fcgiwrap

%build
autoreconf -i
%configure --prefix=""
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?fedora} == 19
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
cp %{_builddir}%{_unitdir}/fcgiwrap.service $RPM_BUILD_ROOT%{_unitdir}
cp %{_builddir}%{_unitdir}/fcgiwrap.socket $RPM_BUILD_ROOT%{_unitdir}
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_unitdir}/fcgiwrap.service
%{_unitdir}/fcgiwrap.socket
%doc README.rst
%{_sbindir}/fcgiwrap
%{_mandir}/man8/fcgiwrap.8*

%pre
# Add the "fcgiwrap" user
getent group %{fcgiwrap_group} >/dev/null || groupadd -r %{fcgiwrap_group}
getent passwd %{fcgiwrap_user} >/dev/null || \
    useradd -r -g %{fcgiwrap_group} -s /sbin/nologin \
    -d %{fcgiwrap_home} -c "fcgiwrap user"  %{fcgiwrap_user}
exit 0

%post
# Register the fcgiwrap service
/usr/bin/systemctl preset fcgiwrap.service >/dev/null 2>&1 ||:
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-fcgiwrap!

Please find the official documentation for fcgiwrap here:
* https://nginx.localdomain.pl/wiki/FcgiWrap

For any additional help please visit my forum at:
* http://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun
if [ $1 -eq 0 ]; then
/usr/bin/systemctl --no-reload disable fcgiwrap.service >/dev/null 2>&1 ||:
/usr/bin/systemctl stop fcgiwrap.service >/dev/null 2>&1 ||:

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:


%changelog
* Sun Oct 12 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> - 1.1.0-1
- Initial release
