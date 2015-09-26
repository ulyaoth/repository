%define package_name ulyaoth-tengine

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
# end of distribution specific definitions

Summary: SELinux policy for ulyaoth-tengine.
Name: ulyaoth-tengine-selinux
Version: 1.0.0
Release: 1%{?dist}
BuildArch: x86_64
Vendor: Ulyaoth
URL: https://www.ulyaoth.net
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
License: GNU General Public License (GPL)

Source0: ulyaoth-tengine.pp

BuildRequires: selinux-policy-targeted
Requires(post): policycoreutils, %{package_name}
Requires(preun): policycoreutils, %{package_name}
Requires(postun): policycoreutils
Requires: ulyaoth-tengine

Provides: ulyaoth-tengine-selinux

%description
This package opens up SELinux so you can use the package ulyaoth-tengine.

%install
install -p -m 644 -D %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{package_name}/ulyaoth-tengine.pp

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_datadir}/selinux/packages/ulyaoth-tengine
%{_datadir}/selinux/packages/ulyaoth-tengine/ulyaoth-tengine.pp

%pre

%post
if [ $1 -eq 1 ]; then
semodule -i /usr/share/selinux/packages/ulyaoth-tengine/ulyaoth-tengine.pp 2>/dev/null || :
%if %{use_systemd}
    /usr/bin/systemctl restart tengine.service >/dev/null 2>&1 ||:
%else
    /etc/init.d/tengine restart
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-tengine-selinux!

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
semodule -r ulyaoth-tengine 2>/dev/null || :
%if %use_systemd
    /usr/bin/systemctl --no-reload disable tengine.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop tengine.service >/dev/null 2>&1 ||:
%else
    /sbin/service tengine stop > /dev/null 2>&1
    /sbin/chkconfig --del tengine
%endif
fi

%postun
if [ "$1" -ge "1" ] ; then # Upgrade
semodule -i /usr/share/selinux/packages/ulyaoth-tengine/ulyaoth-tengine.pp 2>/dev/null || :
fi

%changelog
* Sun Apr 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.0-1
- Initial release.