
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat7-admin
Version:    7.0.91
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-7/v%{version}/bin/apache-tomcat-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat7

Provides: tomcat-admin
Provides: apache-tomcat-admin
Provides: ulyaoth-tomcat-admin
Provides: ulyaoth-tomcat7-admin

%description
The package contains the official Apache Tomcat "webapps/manager" and "webapps/host-manager" directories.

%prep
%setup -q -n apache-tomcat-%{version}

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
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/examples
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}/webapps/host-manager
%dir %{tomcat_home}/webapps/manager
%{tomcat_home}/webapps/manager/*
%{tomcat_home}/webapps/host-manager/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat7-admin!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 7.0.91-1
- Updated to Tomcat 7.0.91.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.88-1
- Updated to Tomcat 7.0.88.

* Wed Nov 15 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.82-1
- Updated to Tomcat 7.0.82.

* Tue Jul 4 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.79-1
- Updated to Tomcat 7.0.79.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.78-1
- Updated to Tomcat 7.0.78.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.77-1
- Updated to Tomcat 7.0.77.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.76-1
- Updated to Tomcat 7.0.76.

* Mon Feb 13 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.75-1
- Updated to Tomcat 7.0.75.

* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.73-1
- Updated to Tomcat 7.0.73.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.72-1
- Updated to Tomcat 7.0.72.

* Wed Jun 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.70-1
- Updated to Tomcat 7.0.70.

* Tue Apr 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.69-1
- Updated to Tomcat 7.0.69.

* Sat Apr 9 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.68-1
- Updated to Tomcat 7.0.68.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.67-1
- Updated to Tomcat 7.0.67.

* Sat Oct 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.65-1
- Updated to Tomcat 7.0.65.

* Sun Aug 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.64-1
- Updated to Tomcat 7.0.64.

* Thu Jul 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.63-1
- Updated to Tomcat 7.0.63.

* Fri May 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.62-1
- Updated to Tomcat 7.0.62.

* Sat Apr 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.61-1
- Updated to Tomcat 7.0.61.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-2
- Removal of some things from spec file.
- Support for Fedora 22 and CentOS 6 & 7.
- i386 Support.

* Fri Feb 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-1
- Update to tomcat 7.0.59.

* Tue Nov 18 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.57-1
- Update to tomcat 7.0.57.

* Mon Nov 17 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.56-1
- Creating separate package for the admin interface.