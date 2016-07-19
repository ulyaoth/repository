
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat9-examples
Version:    9.0.0
Release:    6%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://www.eu.apache.org/dist/tomcat/tomcat-9/v%{version}.M9/bin/apache-tomcat-%{version}.M9.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}.M9-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat9

Provides: tomcat-examples
Provides: apache-tomcat-examples
Provides: ulyaoth-tomcat-examples
Provides: ulyaoth-tomcat9-examples

%description
The package contains the official Apache Tomcat "webapps/examples" and "webapps/ROOT" directories.

%prep
%setup -q -n apache-tomcat-%{version}.M9

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Delete all files except webapp admin
%{__rm} -rf %{buildroot}/%{tomcat_home}/bin
%{__rm} -rf %{buildroot}/%{tomcat_home}/conf
%{__rm} -rf %{buildroot}/%{tomcat_home}/lib
%{__rm} -rf %{buildroot}/%{tomcat_home}/LICENSE
%{__rm} -rf %{buildroot}/%{tomcat_home}/NOTICE
%{__rm} -rf %{buildroot}/%{tomcat_home}/RELEASE-NOTES
%{__rm} -rf %{buildroot}/%{tomcat_home}/RUNNING.txt
%{__rm} -rf %{buildroot}/%{tomcat_home}/temp
%{__rm} -rf %{buildroot}/%{tomcat_home}/work
%{__rm} -rf %{buildroot}/%{tomcat_home}/logs
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/docs
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/host-manager
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/manager

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}/webapps/examples
%dir %{tomcat_home}/webapps/ROOT
%{tomcat_home}/webapps/examples/*
%{tomcat_home}/webapps/ROOT/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat9-examples!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Tue Jul 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-6
- Updating to Tomcat 9.0.0.M9.

* Thu Jun 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-5
- Updating to Tomcat 9.0.0.M8.

* Sat May 21 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-4
- Updating to Tomcat 9.0.0.M6.

* Fri Mar 18 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-3
- Updating to Tomcat 9.0.0.M4.

* Fri Feb 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-2
- Updating to Tomcat 9.0.0.M3.

* Sat Nov 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-1
- Initial release for Tomcat 9.0.0.M1.