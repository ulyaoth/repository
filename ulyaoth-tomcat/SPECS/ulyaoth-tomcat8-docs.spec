
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat8-docs
Version:    8.0.43
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat8

Provides: tomcat-docs
Provides: apache-tomcat-docs
Provides: ulyaoth-tomcat-docs
Provides: ulyaoth-tomcat8-docs

%description
The package contains the official Apache Tomcat "webapps/docs" directory.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Delete all files except webapp docs
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
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/examples
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/ROOT
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/host-manager
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/manager

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}/webapps/docs
%{tomcat_home}/webapps/docs/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat8-docs!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.43-1
- Updated to Tomcat 8.0.43.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.42-1
- Updated to Tomcat 8.0.42.

* Mon Feb 13 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.41-1
- Updated to Tomcat 8.0.41.

* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.39-1
- Updated to Tomcat 8.0.39.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.38-1
- Updated to Tomcat 8.0.38.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.37-1
- Updated to Tomcat 8.0.37.

* Thu Jun 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.36-1
- Updated to Tomcat 8.0.36.

* Sat May 21 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.35-1
- Updated to Tomcat 8.0.35.

* Mon Mar 28 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.33-1
- Updated to Tomcat 8.0.33.

* Fri Feb 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.32-1
- Updated to Tomcat 8.0.32.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.30-1
- Updated to Tomcat 8.0.30.

* Sat Nov 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.29-1
- Updated to Tomcat 8.0.29.

* Sat Oct 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.28-1
- Updated to Tomcat 8.0.28.

* Mon Oct 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.27-1
- Updated to Tomcat 8.0.27.

* Sun Aug 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.0.26-1
- Updated to Tomcat 8.0.26.

* Thu Jul 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.24-1
- Updated to Tomcat 8.0.24.

* Wed Jun 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.23-1
- Update to Tomcat 8.0.23.

* Thu May 7 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.22-1
- Update to Tomcat 8.0.22.

* Tue Mar 31 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.21-1
- Update to Tomcat 8.0.21.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.20-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.20-2
- Removal of some things from spec file.
- Support for Fedora 22 and CentOS 6 & 7.
- i386 Support.

* Wed Feb 25 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.20-1
- Update to tomcat 8.0.20.

* Fri Feb 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.18-1
- Update to tomcat 8.0.18.

* Mon Nov 17 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 8.0.15-1
- Creating separate package for the documentation.
