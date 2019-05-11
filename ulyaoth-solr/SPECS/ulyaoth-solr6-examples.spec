
%define __jar_repack %{nil}
%define debug_package %{nil}
%define solr_home /opt/solr
%define solr_group solr
%define solr_user solr

Summary:    Apache Solr Examples
Name:       ulyaoth-solr6-examples
Version:    6.6.6
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://lucene.apache.org/solr/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    solr-%{version}.tar.gz
BuildRoot:  %{_tmppath}/solr-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-solr6

Provides: solr-examples
Provides: solr6-examples
Provides: ulyaoth-solr-examples
Provides: ulyaoth-solr6-examples

Conflicts: ulyaoth-solr4-examples
Conflicts: ulyaoth-solr5-examples

%description
Solr is highly reliable, scalable and fault tolerant, providing distributed indexing, replication and load-balanced querying, automated failover and recovery, centralized configuration and more.

%prep
%setup -q -n solr-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{solr_home}/
cp -R * %{buildroot}/%{solr_home}/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{solr_group} >/dev/null || groupadd -r %{solr_group}
getent passwd %{solr_user} >/dev/null || /usr/sbin/useradd --comment "Solr Daemon User" --shell /bin/bash -M -r -g %{solr_group} --home %{solr_home} %{solr_user}

%files
%defattr(-,%{solr_user},%{solr_group})
%{solr_home}/example/*
%dir %{solr_home}/example

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-solr6-examples!

Please find the official documentation for solr here:
* https://lucene.apache.org/solr/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%changelog
* Sat May 11 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 6.6.6-1
- Updated to Solr 6 version 6.6.6.

* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 6.6.5-1
- Updated to Solr 6 version 6.6.5.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 6.6.4-1
- Updated to Solr 6 version 6.6.4.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 6.6.2-1
- Updated to Solr 6 version 6.6.2.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 6.6.0-1
- Updated to Solr 6 version 6.6.0.

* Sat Apr 29 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.5.1-1
- Updated to Solr 6 version 6.5.1.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.5.0-1
- Updated to Solr 6 version 6.5.0.

* Wed Mar 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.4.2-1
- Updated to Solr 6 version 6.4.2.

* Fri Feb 24 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.4.1-1
- Updated to Solr 6 version 6.4.1.

* Sun Feb 19 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.4.0-1
- Updated to Solr 6 version 6.4.0.

* Sun Nov 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.3.0-1
- Updated to Solr 6 version 6.3.0.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.2.1-1
- Updated to Solr 6 version 6.2.1.

* Sat Aug 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.2.0-1
- Updated to Solr 6 version 6.2.0.

* Sat Jun 18 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.1.0-1
- Updated to Solr 6 version 6.1.0.

* Tue May 31 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.0.1-1
- Updated to Solr 6 version 6.0.1.

* Wed Apr 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 6.0.0-1
- Initial release.
