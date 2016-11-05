#!/bin/bash
 
if [ $# -lt 1 ]; then
  echo "Usage: $1 (module name, example: headers-more)"
  exit 1
fi

# headers-more
if [ "$1" = "headers-more" ]; then
module="headers-more-module"
moduleversion=0.32
# echo
elif [ "$1" = "echo" ]; then
module="echo-module"
moduleversion=0.60
# pam
elif [ "$1" = "pam" ]; then
module="pam-module"
moduleversion=1.5.1
# form-input
elif [ "$1" = "form-input" ]; then
module="form-input-module"
moduleversion=0.12
develkitversion=0.3.0
# devel-kit
elif [ "$1" = "devel-kit" ]; then
module="devel-kit-module"
moduleversion=0.3.0
# encrypted-session
elif [ "$1" = "encrypted-session" ]; then
module="encrypted-session-module"
moduleversion=0.06
develkitversion=0.3.0
# array var
elif [ "$1" = "array-var" ]; then
module="array-var-module"
moduleversion=0.05
develkitversion=0.3.0
# naxsi
elif [ "$1" = "naxsi" ]; then
module="naxsi-module"
moduleversion=0.55.1
else
echo "We only support limited modules please see the Github readme for more information."
exit 1
fi

ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 7" /etc/oracle-release
then
yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm
else
echo No extra installation required for this OS!
fi

useradd ulyaoth
cd /home/ulyaoth/

# headers-more
if [ "$module" = "headers-more-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/headers-more-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv headers-more-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
# echo
elif [ "$module" = "echo-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/echo-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv echo-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
#pam
elif [ "$module" = "pam-module" ]; then
su ulyaoth -c "wget https://github.com/stogh/ngx_http_auth_pam_module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv ngx_http_auth_pam_module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
# form-input
elif [ "$module" = "form-input-module" ]; then
su ulyaoth -c "wget https://github.com/calio/form-input-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv form-input-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
su ulyaoth -c "wget https://github.com/simpl/ngx_devel_kit/archive/v$develkitversion.tar.gz"
su ulyaoth -c "tar xvf v$develkitversion.tar.gz"
su ulyaoth -c "mv ngx_devel_kit-$develkitversion /home/ulyaoth/devel-kit-module"
su ulyaoth -c "rm -rf v$develkitversion.tar.gz"
# devel-kit
elif [ "$module" = "devel-kit-module" ]; then
su ulyaoth -c "wget https://github.com/simpl/ngx_devel_kit/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv ngx_devel_kit-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
# encrypted-session
elif [ "$module" = "encrypted-session-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/encrypted-session-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv encrypted-session-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
su ulyaoth -c "wget https://github.com/simpl/ngx_devel_kit/archive/v$develkitversion.tar.gz"
su ulyaoth -c "tar xvf v$develkitversion.tar.gz"
su ulyaoth -c "mv ngx_devel_kit-$develkitversion /home/ulyaoth/devel-kit-module"
su ulyaoth -c "rm -rf v$develkitversion.tar.gz"
# array-var
elif [ "$module" = "array-var-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/array-var-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv array-var-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
su ulyaoth -c "wget https://github.com/simpl/ngx_devel_kit/archive/v$develkitversion.tar.gz"
su ulyaoth -c "tar xvf v$develkitversion.tar.gz"
su ulyaoth -c "mv ngx_devel_kit-$develkitversion /home/ulyaoth/devel-kit-module"
su ulyaoth -c "rm -rf v$develkitversion.tar.gz"
# naxsi
elif [ "$module" = "naxsi-module" ]; then
su ulyaoth -c "wget https://github.com/nbs-system/naxsi/archive/$moduleversion.tar.gz"
su ulyaoth -c "tar xvf $moduleversion.tar.gz"
su ulyaoth -c "mv naxsi-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf $moduleversion.tar.gz"
fi

su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-$module.spec"
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-mainline-$module.spec"


if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-$module.spec
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-$module.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-$module.spec
  dnf builddep -y ulyaoth-nginx-mainline-$module.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-$module.spec
  yum-builddep -y ulyaoth-nginx-mainline-$module.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-$module.spec -g -R"
su ulyaoth -c "spectool ulyaoth-nginx-mainline-$module.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-$module.spec"
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-mainline-$module.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/*$1* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/*$1* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/*$1* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/*$1* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/*$1* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/*$1* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/*$1* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/*$1* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/$module
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/devel-kit-module