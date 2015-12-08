
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Tomcat multiple instances
Name:       ulyaoth-tomcat-multi
Version:    1.0.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    
BuildRoot:  %{_tmppath}/tomcat-multi-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-jsvc

Provides:  ulyaoth-tomcat-multi

%description
This module adds all the scripts to a server so you can use a ulyaoth tomcat installation with multiple instances.
This rpm is based on the scripts that Fedora 23 provides for their tomcat but changed to fit ulyaoth tomcat.


%prep

%build

%install


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE NOTICE TODO.txt
%ifarch x86_64
/usr/lib64/libtcnative*.so*
%endif
/usr/lib/libtcnative*.so*


%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-tomcat-multi!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

Please find the documentation for using tomcat multiple instances here:
* https://www.ulyaoth.net/threads/how-to-configure-multiple-tomcat-instances.82312/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Tue Dec 8 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.0-1
- Initial release.
