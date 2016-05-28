
%define __jar_repack %{nil}
%define debug_package %{nil}
%define banana_home /opt/solr
%define banana_group solr
%define banana_user solr

Summary:    Banana UI
Name:       ulyaoth-banana
Version:    1.6.8
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://github.com/LucidWorks/banana/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    banana.war
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-banana/SOURCES/banana-context.xml
BuildRoot:  %{_tmppath}/banana-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ant

Provides: banana
Provides: ulyaoth-banana

%description
Banana is a tool to create dashboards to visualize data you have stored in Solr. Commonly used with Logstash for log data, any content stored in a Solr index is eligible for visualization in a Banana dashboard.

%install
%{__mkdir} -p $RPM_BUILD_ROOT/opt/solr/server/webapps/
%{__install} -m644 %SOURCE0 \
        $RPM_BUILD_ROOT/%{banana_home}/server/webapps/banana.war

%{__mkdir} -p $RPM_BUILD_ROOT/opt/solr/server/contexts
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT/opt/solr/server/contexts/banana-context.xml

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{banana_group} >/dev/null || groupadd -r %{banana_group}
getent passwd %{banana_user} >/dev/null || /usr/sbin/useradd --comment "Solr Daemon User" --shell /bin/bash -M -r -g %{banana_group} --home %{banana_home} %{banana_user}

%files
%defattr(-,%{banana_user},%{banana_group})
%{banana_home}/server/webapps/banana.war
%{banana_home}/server/contexts/banana-context.xml


%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-banana!

Please find the official documentation for Banana here:
* https://github.com/LucidWorks/banana/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Sat May 28 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.8-1
- Updated to Banana version 1.6.8.

* Sat Mar 5 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.0-1
- Updated to Banana version 1.6.0.

* Sat Feb 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.5.1-1
- Updated to Banana version 1.5.1.

* Tue Jul 7 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.0-2
- Fixed issue #5 from GitHub where I build wrongly against a Branch directly.
- Now building from official release "tar.gz" file.
- Thank you Fred Emmott for reporting and explaining.

* Fri Mar 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.5.0-1
- Initial release for Banana based on version 1.5.0.
