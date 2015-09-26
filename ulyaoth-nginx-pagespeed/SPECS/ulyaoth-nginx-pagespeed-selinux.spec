%define package_name ulyaoth-nginx-pagespeed

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
# end of distribution specific definitions

Summary: Selinux policy for Ulyaoth-Nginx-Pagespeed.
Name: ulyaoth-nginx-pagespeed-selinux
Version: 1.0.2
Release: 1%{?dist}
BuildArch: x86_64
Vendor: Ulyaoth
URL: https://www.ulyaoth.net
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr>
License: GNU General Public License (GPL)

Source0: ulyaoth-nginx-pagespeed.pp

BuildRequires: selinux-policy-targeted
Requires(post): policycoreutils, %{package_name}
Requires(preun): policycoreutils, %{package_name}
Requires(postun): policycoreutils
Requires: ulyaoth-nginx-pagespeed

Provides: ulyaoth-nginx-pagespeed-selinux

%description
This package opens up selinux so you can use the package ulyaoth-nginx-pagespeed.

%install
install -p -m 644 -D %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{package_name}/ulyaoth-nginx-pagespeed.pp

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_datadir}/selinux/packages/%{package_name}
%{_datadir}/selinux/packages/%{package_name}/ulyaoth-nginx-pagespeed.pp

%pre

%post
if [ $1 -eq 1 ]; then
semodule -i %{_datadir}/selinux/packages/%{package_name}/ulyaoth-nginx-pagespeed.pp 2>/dev/null || :
%if %{use_systemd}
    /usr/bin/systemctl restart nginx.service >/dev/null 2>&1 ||:
%else
    /etc/init.d/nginx restart
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-nginx-pagespeed-selinux!

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
semodule -r ulyaoth-nginx-pagespeed 2>/dev/null || :
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
if [ "$1" -ge "1" ] ; then # Upgrade
semodule -i %{_datadir}/selinux/packages/%{package_name}/ulyaoth-nginx-pagespeed.pp 2>/dev/null || :
fi

%changelog
* Fri Apr 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.2-1
- Spec file had a wrong postun, changed it to correct one for upgrading package.

* Fri Apr 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.1-1
- Fixed a mistake so the policy file is created on the actual OS.

* Fri Apr 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.0-1
- Initial release for fixing selinux when using package ulyaoth-nginx-pagespeed.