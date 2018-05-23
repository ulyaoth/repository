
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat9-admin
Version:    9.0.8
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-9/v%{version}/bin/apache-tomcat-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat9

Provides: tomcat-admin
Provides: apache-tomcat-admin
Provides: ulyaoth-tomcat-admin
Provides: ulyaoth-tomcat9-admin

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

Thank you for using ulyaoth-tomcat9-admin!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 9.0.8-1
- Updating to Tomcat 9.0.8.

* Fri Jan 5 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 9.0.2-1
- Updating to Tomcat 9.0.2.

* Wed Nov 15 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 9.0.1-1
- Updating to Tomcat 9.0.1.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 9.0.0-15
- Updating to Tomcat 9.0.0.M22.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-14
- Updating to Tomcat 9.0.0.M21.

* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-13
- Updating to Tomcat 9.0.0.M20.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-12
- Updating to Tomcat 9.0.0.M19.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-11
- Updating to Tomcat 9.0.0.M18.

* Mon Feb 13 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-10
- Updating to Tomcat 9.0.0.M17.

* Sun Nov 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-9
- Updating to Tomcat 9.0.0.M13.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-8
- Updating to Tomcat 9.0.0.M11.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 9.0.0-7
- Updating to Tomcat 9.0.0.M10.

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