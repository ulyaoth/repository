%define debug_package %{nil}

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
BuildRequires: systemd-devel
%endif

# end of distribution specific definitions

Summary:    Hitch is a libev-based high performance SSL/TLS proxy by Varnish Software.
Name:       ulyaoth-hitch
Version:    1.4.4
Release:    1%{?dist}
BuildArch: x86_64
License:    GPL/LGPL
Group:      System Environment/Daemons
URL:        https://hitch-tls.org/
Vendor:     Hitch
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/varnish/hitch/archive/hitch-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hitch/SOURCES/hitch.conf
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hitch/SOURCES/hitch.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hitch/SOURCES/hitch.service
BuildRoot:  %{_tmppath}/hitch-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: flex
BuildRequires: bison
BuildRequires: python-docutils
BuildRequires: libev-devel
BuildRequires: ulyaoth-openssl1.1.0

Requires: ulyaoth-openssl1.1.0

Provides: hitch
Provides: ulyaoth-hitch

%description
hitch is a network proxy that terminates TLS/SSL connections and forwards the unencrypted traffic to some backend. It's designed to handle 10s of thousands of connections efficiently on multicore machines.

%prep
%setup -q -n hitch-hitch-%{version}

%build
export SSL_CFLAGS="-I/usr/local/ulyaoth/ssl/openssl1.1.0/include -L/usr/local/ulyaoth/ssl/openssl1.1.0/lib"
export SSL_LIBS=-lssl
export CRYPTO_CFLAGS="-I/usr/local/ulyaoth/ssl/openssl1.1.0/include -L/usr/local/ulyaoth/ssl/openssl1.1.0/lib"
export CRYPTO_LIBS=-lcrypto
export C_INCLUDE_PATH=/usr/local/ulyaoth/ssl/openssl1.1.0/include
export LIBRARY_PATH=/usr/local/ulyaoth/ssl/openssl1.1.0/lib
./configure --prefix=/usr --bindir=%{_bindir} --sbindir=%{_sbindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} --sharedstatedir=%{_sharedstatedir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datarootdir} --datadir=%{_datadir} --infodir=%{_infodir} --mandir=%{_mandir} --docdir=/usr/share/doc 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

mkdir -p $RPM_BUILD_ROOT/var/lib/hitch

	%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/hitch
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/hitch/hitch.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/hitch
	
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
    $RPM_BUILD_ROOT%{_unitdir}/hitch.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %SOURCE2 \
    $RPM_BUILD_ROOT%{_initrddir}/hitch
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)


%if %{use_systemd}
%{_unitdir}/hitch.service
%else
%{_initrddir}/hitch
%endif

%post
/sbin/ldconfig
# Register the hitch service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset hitch.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add hitch
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-hitch!

Please find the official documentation for Hitch here:
* https://hitch-tls.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable hitch.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop hitch.service >/dev/null 2>&1 ||:
%else
    /sbin/service hitch stop > /dev/null 2>&1
    /sbin/chkconfig --del hitch
%endif
fi

%postun
/sbin/ldconfig
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service hitch status  >/dev/null 2>&1 || exit 0
    /sbin/service hitch upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed."
fi

%changelog
* Sun Mar 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.4.4-1
- Initial release for Hitch.