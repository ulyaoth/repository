# This script is supposed to run as the user "ulyaoth".

# Get os version
ulyaothos=`cat /etc/ulyaoth`

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tmux/SPECS/ulyaoth-tmux.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tmux.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tmux.spec -g -R

# Install additional files
if [ "$ulyaothos" == "scientificlinux6" ]
then
  yum install http://mirror.centos.org/centos/6/os/x86_64/Packages/libevent2-2.0.21-2.el6.x86_64.rpm http://mirror.centos.org/centos/6/os/x86_64/Packages/libevent2-devel-2.0.21-2.el6.x86_64.rpm -y
fi

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tmux.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tmux.spec
fi

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tmux.spec





