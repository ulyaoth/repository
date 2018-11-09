
%define __jar_repack %{nil}
%define debug_package %{nil}
%define solr_home /opt/solr
%define solr_group solr
%define solr_user solr

Summary:    Apache Solr Documentations
Name:       ulyaoth-solr7-docs
Version:    7.5.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://lucene.apache.org/solr/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    solr-%{version}.tar.gz
BuildRoot:  %{_tmppath}/solr-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-solr7

Provides: solr-docs
Provides: solr7-docs
Provides: ulyaoth-solr-docs
Provides: ulyaoth-solr7-docs

Conflicts: ulyaoth-solr4-docs
Conflicts: ulyaoth-solr5-docs
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

Thank you for using ulyaoth-solr7-docs!

Please find the official documentation for solr here:
* https://lucene.apache.org/solr/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 7.5.0-1
- Updated Solr 7 to 7.5.0.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.3.1-1
- Updated Solr 7 to 7.3.1.

* Mon Feb 12 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.2.1-1
- Updated Solr 7 to 7.2.1.

* Fri Jan 5 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.2.0-1
- Updated Solr 7 to 7.2.0.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.1.0-1
- Updated Solr 7 to 7.1.0.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.1-1
- Initial release.