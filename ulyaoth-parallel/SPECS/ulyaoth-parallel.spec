u%define debug_package %{nil}

Summary:    GNU parallel is a shell tool for executing jobs in parallel using one or more computers.
Name:       ulyaoth-parallel
Version:    20190422
Release:    1%{?dist}
BuildArch: x86_64
License:    GNUv3
Group:      Applications/System
URL:        https://www.gnu.org/software/parallel/
Vendor:     GNU
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
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
/usr/bin/env_parallel
/usr/bin/env_parallel.ash
/usr/bin/env_parallel.bash
/usr/bin/env_parallel.csh
/usr/bin/env_parallel.dash
/usr/bin/env_parallel.fish
/usr/bin/env_parallel.ksh
/usr/bin/env_parallel.pdksh
/usr/bin/env_parallel.sh
/usr/bin/env_parallel.tcsh
/usr/bin/env_parallel.zsh
/usr/bin/niceload
/usr/bin/parallel
/usr/bin/parcat
/usr/bin/sem
/usr/bin/sql
%doc /usr/share/doc/env_parallel.html
%doc /usr/share/doc/env_parallel.pdf
%doc /usr/share/doc/env_parallel.texi
%doc /usr/share/doc/niceload.html
%doc /usr/share/doc/niceload.pdf
%doc /usr/share/doc/niceload.texi
%doc /usr/share/doc/parallel.html
%doc /usr/share/doc/parallel.pdf
%doc /usr/share/doc/parallel.texi
%doc /usr/share/doc/parallel_alternatives.html
%doc /usr/share/doc/parallel_alternatives.pdf
%doc /usr/share/doc/parallel_alternatives.texi
%doc /usr/share/doc/parallel_design.html
%doc /usr/share/doc/parallel_design.pdf
%doc /usr/share/doc/parallel_design.texi
%doc /usr/share/doc/parallel_tutorial.html
%doc /usr/share/doc/parallel_tutorial.pdf
%doc /usr/share/doc/parallel_tutorial.texi
%doc /usr/share/doc/parallel_book.html
%doc /usr/share/doc/parallel_book.pdf
%doc /usr/share/doc/parallel_book.texi
%doc /usr/share/doc/parcat.html
%doc /usr/share/doc/parcat.pdf
%doc /usr/share/doc/parcat.texi
%doc /usr/share/doc/parset.html
%doc /usr/share/doc/parset.pdf
%doc /usr/share/doc/parset.texi
%doc /usr/share/doc/sem.html
%doc /usr/share/doc/sem.pdf
%doc /usr/share/doc/sem.texi
%doc /usr/share/doc/sql.html
%doc /usr/share/doc/sql.pdf
%doc /usr/share/doc/sql.texi
%doc /usr/share/man/man1/env_parallel.1.gz
%doc /usr/share/man/man1/niceload.1.gz
%doc /usr/share/man/man1/parallel.1.gz
%doc /usr/share/man/man1/parcat.1.gz
%doc /usr/share/man/man1/parset.1.gz
%doc /usr/share/man/man1/sem.1.gz
%doc /usr/share/man/man1/sql.1.gz
%doc /usr/share/man/man7/parallel_alternatives.7.gz
%doc /usr/share/man/man7/parallel_design.7.gz
%doc /usr/share/man/man7/parallel_tutorial.7.gz
%doc /usr/share/man/man7/parallel_book.7.gz

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-parallel!

Please find the official documentation for parallel here:
* https://www.gnu.org/software/parallel/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun May 12 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 20190422-1
- Updated Parallel to 20190422.

* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 20181022-1
- Updated Parallel to 20181022.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20180522-1
- Updated Parallel to 20180522.

* Fri Jan 5 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20171222-1
- Updated Parallel to 20171222.

* Sun Nov 26 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20171122-1
- Updated Parallel to 20171122.

* Wed Nov 8 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20171022-1
- Updated Parallel to 20171022.

* Wed Aug 9 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20170722-1
- Updated Parallel to 20170722.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 20170622-1
- Updated Parallel to 20170622.

* Thu May 25 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 20170522-1
- Updated Parallel to 20170522.

* Sun Apr 23 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 20170422-1
- Initial release.