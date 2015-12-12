
%define tomcat_group tomcat
%define tomcat_user tomcat

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Tomcat multiple instances
Name:       ulyaoth-tomcat-multi
Version:    1.0.0
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.ulyaoth.net
Vendor:     Ulyaoth
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/functions
Source1:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/preamble
Source2:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/server
Source3:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/tomcat%40.service
BuildRoot:  %{_tmppath}/tomcat-multi-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-jsvc

Provides: ulyaoth-tomcat-multi
Provides: tomcat-multi

%description
This module adds all the scripts to a server so you can use a ulyaoth tomcat installation with multiple instances.
This rpm is based on the scripts that Fedora 23 provides for their tomcat but changed to fit ulyaoth tomcat.


%prep

%build

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/libexec/tomcat

%{__install} -m 644 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/functions
%{__install} -m 755 -p %{SOURCE1} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/preamble
%{__install} -m 755 -p %{SOURCE2} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/server

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/tomcat@.service
%endif
   
 
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/libexec/tomcat/functions
/usr/libexec/tomcat/preamble
/usr/libexec/tomcat/server

%if %{use_systemd}
%{_unitdir}/tomcat.service
%endif

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