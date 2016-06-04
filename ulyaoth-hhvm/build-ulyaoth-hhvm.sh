#!/bin/bash
# Argument = -h (shows the help information)
# Argument = -l (lists all supported versions)
# Argument = -b (branch .i.e 3.13)
# Argument = -v (version .i.e 3.13.2)
# Created By: Sjir Bagmeijer - 2015/07/08
# Last Edit By: Sjir Bagmeijer - 2016/06/04
# https://www.ulyaoth.net

# Shows the menu when using -h or wrong option.
usage()
{
cat << EOF
usage: $0 options

OPTIONS:
   -h  Shows this help information
   -l  Show list of all supported versions
   -b  Choose to your HHVM branch.
   -v  Choose the HHVM version you wich to install.
EOF
exit 1
}

# Build the rpm for your specifiec HHVM version.
buildrpm()
{
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/

su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/SPECS/ulyaoth-hhvm-'"$hhvmbranchversion"'.spec"

if grep -q -i "release 7" /etc/redhat-release
then
yum install -y  https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
fi

if [ "$hhvmbranchversion" == "3.9" ] || [ "$hhvmbranchversion" == "3.11" ] || [ "$hhvmbranchversion" == "3.12" ] || [ "$hhvmbranchversion" == "3.13" ]
then
  if grep -q -i "release 19" /etc/fedora-release || grep -q -i "release 20" /etc/fedora-release
  then
    yum remove -y ocaml
    yum install -y https://dl.fedoraproject.org/pub/fedora/linux/releases/21/Everything/x86_64/os/Packages/o/ocaml-4.01.0-24.fc21.x86_64.rpm https://dl.fedoraproject.org/pub/fedora/linux/releases/21/Everything/x86_64/os/Packages/o/ocaml-compiler-libs-4.01.0-24.fc21.x86_64.rpm https://dl.fedoraproject.org/pub/fedora/linux/releases/21/Everything/x86_64/os/Packages/o/ocaml-runtime-4.01.0-24.fc21.x86_64.rpm
  fi
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-hhvm-$hhvmbranchversion.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-hhvm-$hhvmbranchversion.spec
fi

su ulyaoth -c "spectool ulyaoth-hhvm-$hhvmbranchversion.spec -g -R"

cd /home/ulyaoth
su ulyaoth -c "git clone -b HHVM-'"$hhvmbranchversion"' git://github.com/facebook/hhvm.git"
mv /home/ulyaoth/hhvm /home/ulyaoth/hhvm-$hhvmversion
cd /home/ulyaoth/hhvm-$hhvmversion
su ulyaoth -c "git checkout HHVM-'"$hhvmversion"'"
su ulyaoth -c "git submodule update --init --recursive"
cd /home/ulyaoth
su ulyaoth -c "tar cvf hhvm-'"$hhvmversion"'.tar.gz hhvm-'"$hhvmversion"'/"
mv /home/ulyaoth/hhvm-$hhvmversion.tar.gz /home/ulyaoth/rpmbuild/SOURCES/

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "QA_SKIP_BUILD_ROOT=1 rpmbuild -bb ulyaoth-hhvm-'"$hhvmbranchversion"'.spec"
}

# Cleaning build directory and script.
clean()
{
if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/

else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild
rm -rf /home/ulyaoth/hhvm-$hhvmversion
cd /root
}

# Shows the available versions when using -l option.
availablehhvmversions()
{
cat <<EOF
Branch 3.13 versions supported: (LTS build)
* 3.13.2
* 3.13.1
* 3.13.0
Branch 3.12 versions supported: (LTS build)
* 3.12.2
* 3.12.1
* 3.12.0
Branch 3.11 versions supported:
* 3.11.1
* 3.11.0
Branch 3.9 versions supported: (LTS build)
* 3.9.3
* 3.9.2
* 3.9.1
* 3.9.0
Branch 3.6 versions supported: (LTS build)
* 3.6.6
* 3.6.5
* 3.6.4
* 3.6.3
* 3.6.2
* 3.6.1
* 3.6.0
Branch 3.3 versions supported: (LTS build) (No longer maintained)
* 3.3.7
* 3.3.6
* 3.3.5
* 3.3.4
* 3.3.3
* 3.3.2
* 3.3.1
* 3.3.0
EOF
exit 1
}

# This function will compare the user input with the arrays for supported versions and supported branches and stops script if non supported input is found.
arraychecker() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            echo "y"
            return 0
        fi
    }
    echo "n"
    return 1
}

# Set some required variables
ulyaothos=`cat /etc/ulyaoth`
hhvmbranchversion=
hhvmversion=
arch="$(uname -m)"
supportedbranches=('3.3' '3.6' '3.9' '3.11' '3.12' '3.13')
supportedversions=('3.13.2' '3.13.1' '3.13.0' '3.12.2' '3.12.1' '3.12.0' '3.11.1' '3.11.0' '3.8.1' '3.8.0' '3.9.3' '3.9.2' '3.9.1' '3.9.0' '3.6.6' '3.6.5' '3.6.4' '3.6.3' '3.6.2' '3.6.1' '3.6.0' '3.3.7' '3.3.6' '3.3.5' '3.3.4' '3.3.3' '3.3.2' '3.3.1' '3.3.0')

# Check if the platform is 64-bit if not stop script.
if [ "$arch" != "x86_64" ];
then
echo Sorry HHVM only supports a 64-bit platform.
exit 1
fi

# Get the option that was in-putted by user.
while getopts ":h :l :b: :v:" opt; do
case $opt in
h)
  usage
;;
l)
  availablehhvmversions
;;
b)
  hhvmbranchversion=$OPTARG
;;
v)
  hhvmversion=$OPTARG
;;
\?)
  usage
;;
:)
  usage
;;
esac
done

# Check if all options are filled in and if the branch and version are correct.
if [ -z "$hhvmbranchversion" ];
then
  usage
elif [ -z "$hhvmversion" ]
then
  usage
elif [[ " ${supportedbranches[*]} " != *" $hhvmbranchversion "* ]]
then
  echo Currently only the following branches are supported: ${supportedbranches[*]}.
exit 1
elif [[ " ${supportedversions[*]} " != *" $hhvmversion "* ]]
then
  echo "Please run the script with the -l option to see a list of supported versions. (.i.e ulyaoth-hhvm.sh -l)"
exit 1
fi

# Create build user
useradd ulyaoth &> /dev/null

# Start the build process by calling the separate functions.
echo "Step 1: Starting the rpmbuild process."
buildrpm
echo "Step 2: Cleaning your build environment."
clean

echo "Your RPM has been created and placed in your root directory."
exit