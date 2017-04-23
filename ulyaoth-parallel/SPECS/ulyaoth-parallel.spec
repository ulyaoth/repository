
Summary:    GNU parallel is a shell tool for executing jobs in parallel using one or more computers.
Name:       ulyaoth-parallel
Version:    20170422
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv3
Group:      Applications/System
URL:        https://www.gnu.org/software/parallel/
Vendor:     GNU
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://ftp.gnu.org/gnu/parallel/parallel-%{version}.tar.bz2
BuildRoot:  %{_tmppath}/parallel-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: parallel
Provides: ulyaoth-parallel

%description
GNU parallel is a shell tool for executing jobs in parallel using one or more computers. A job can be a single command or a small script that has to be run for each of the lines in the input. The typical input is a list of files, a list of hosts, a list of users, a list of URLs, or a list of tables. A job can also be a command that reads from a pipe. GNU parallel can then split the input and pipe it into commands in parallel.

%prep
%setup -q -n parallel-%{version}

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

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-parallel!

Please find the official documentation for parallel here:
* https://www.gnu.org/software/parallel/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 20170422-1
- Initial release.