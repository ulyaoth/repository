
%define __jar_repack %{nil}
%define debug_package %{nil}
%define solr_home /opt/solr
%define solr_group solr
%define solr_user solr

Summary:    Apache Solr Documentations
Name:       ulyaoth-solr5-docs
Version:    5.5.5
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://lucene.apache.org/solr/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    solr-%{version}.tar.gz
BuildRoot:  %{_tmppath}/solr-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-solr5

Provides: solr-docs
Provides: solr5-docs
Provides: ulyaoth-solr-docs
Provides: ulyaoth-solr5-docs

Conflicts: ulyaoth-solr4-docs
Conflicts: ulyaoth-solr6-docs

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
%{solr_home}/docs/*
%dir %{solr_home}/docs

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-solr5-docs!

Please find the official documentation for solr here:
* https://lucene.apache.org/solr/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%changelog
* Wed Nov 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.com> 5.5.5-1
- Updated to Solr 5.5.5.

* Wed Feb 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.4-1
- Updated to Solr 5.5.4.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.3-1
- Updated to Solr 5.5.3.

* Sat Jul 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.2-1
- Updated to Solr 5.5.2.

* Fri May 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.1-1
- Updated to Solr 5.5.1.

* Sat Feb 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.5.0-1
- Updated to Solr 5.5.0.

* Sun Jan 24 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.4.1-1
- Updated to Solr 5.4.1.

* Tue Dec 29 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.4.0-1
- Updated to Solr 5.4.0.

* Sun Oct 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.1-1
- Updated to Solr 5.3.1.

* Sun Aug 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.3.0-1
- Updated to Solr 5.3.0.

* Mon Jun 22 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.2.1-1
- Updated to Solr 5.2.1.

* Tue Jun 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.2.0-1
- Updated to Solr 5.2.0.

* Thu Apr 16 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.1.0-1
- Updated to Solr 5.1.0.

* Sat Mar 21 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.0-1
- Initial release.
