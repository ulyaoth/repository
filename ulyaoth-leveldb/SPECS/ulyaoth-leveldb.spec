
Summary:    LevelDB is a fast key-value storage library written at Google that provides an ordered mapping from string keys to string values.
Name:       ulyaoth-leveldb
Version:    1.18
Release:    1%{?dist}
BuildArch: x86_64
License:    Contributor License Agreement (CLA)
Group:      Development/Libraries
URL:        https://github.com/google/leveldb
Vendor:     Google
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://github.com/google/leveldb/archive/v%{version}.tar.gz
BuildRoot:  %{_tmppath}/leveldb-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: snappy-devel

Provides: leveldb
Provides: ulyaoth-leveldb

%description
LevelDB is a fast key-value storage library written at Google that provides an ordered mapping from string keys to string values.

%prep
%setup -q -n leveldb-%{version}

%build
make %{?_smp_mflags}

%install
%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}
%{__mkdir} -p $RPM_BUILD_ROOT/usr/local
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/licenses/leveldb
%{__mkdir} -p $RPM_BUILD_ROOT%{_docdir}/leveldb
%{__mv} %{_builddir}/leveldb-%{version}/libleveldb.a $RPM_BUILD_ROOT%{_libdir}
%{__mv} %{_builddir}/leveldb-%{version}/libleveldb.so $RPM_BUILD_ROOT%{_libdir}
%{__mv} %{_builddir}/leveldb-%{version}/libleveldb.so.1 $RPM_BUILD_ROOT%{_libdir}
%{__mv} %{_builddir}/leveldb-%{version}/libleveldb.so.%{version} $RPM_BUILD_ROOT%{_libdir}
%{__mv} %{_builddir}/leveldb-%{version}/include/leveldb $RPM_BUILD_ROOT/usr/local/
%{__mv} %{_builddir}/leveldb-%{version}/LICENSE $RPM_BUILD_ROOT/usr/share/licenses/leveldb/
%{__mv} %{_builddir}/leveldb-%{version}/doc/* $RPM_BUILD_ROOT%{_docdir}/leveldb/
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root)
%{_libdir}/libleveldb.a
%{_libdir}/libleveldb.so
%{_libdir}/libleveldb.so.1
%{_libdir}/libleveldb.so.%{version}
%dir /usr/local/leveldb
%dir /usr/share/licenses/leveldb
%dir %{_docdir}/leveldb
%dir %{_docdir}/leveldb/bench
%doc /usr/share/licenses/leveldb/LICENSE
%doc %{_docdir}/leveldb/benchmark.html
%doc %{_docdir}/leveldb/doc.css
%doc %{_docdir}/leveldb/impl.html
%doc %{_docdir}/leveldb/index.html
%doc %{_docdir}/leveldb/log_format.txt
%doc %{_docdir}/leveldb/table_format.txt
%doc %{_docdir}/leveldb/bench/db_bench_sqlite3.cc
%doc %{_docdir}/leveldb/bench/db_bench_tree_db.cc
/usr/local/leveldb/cache.h
/usr/local/leveldb/c.h
/usr/local/leveldb/comparator.h
/usr/local/leveldb/db.h
/usr/local/leveldb/dumpfile.h
/usr/local/leveldb/env.h
/usr/local/leveldb/filter_policy.h
/usr/local/leveldb/iterator.h
/usr/local/leveldb/options.h
/usr/local/leveldb/slice.h
/usr/local/leveldb/status.h
/usr/local/leveldb/table_builder.h
/usr/local/leveldb/table.h
/usr/local/leveldb/write_batch.h

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-leveldb!

Please find the official documentation for leveldb here:
* https://github.com/google/leveldb

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%preun

%postun

%changelog
* Sun Jun 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.18-1
- Initial release.