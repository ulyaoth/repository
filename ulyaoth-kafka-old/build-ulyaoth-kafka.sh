#!/bin/bash
# Argument = -h (shows the help information)
# Argument = -l (lists all supported versions)
# Argument = -k (kafka version .i.e 0.10.0.0)
# Argument = -s (scala version .i.e 2.11)
# Created By: Sjir Bagmeijer - 2016/05/28
# Last Edit By: Sjir Bagmeijer - 2016/05/28
# https://www.ulyaoth.net

# Shows the menu when using -h or wrong option.
usage()
{
cat << EOF
usage: $0 options

OPTIONS:
   -h  Shows this help information
   -l  Show list of all supported versions
   -k  kafka version .i.e 0.10.0.0.
   -s  scala version .i.e 2.11.
EOF
exit 1
}


# Shows the available versions when using -l option.
availablekafkaversions()
{
cat <<EOF
Kafka versions supported:
* 0.10.0.0 (Scala 2.10 & 2.11)
* 0.9.0.1 (Scala 2.10 & 2.11)
* 0.9.0.0 (Scala 2.10 & 2.11)
* 0.8.2.2 (Scala 2.9.1, 2.9.2, 2.10 & 2.11)
* 0.8.2.1 (Scala 2.9.1, 2.9.2, 2.10 & 2.11)
* 0.8.2.0 (Scala 2.9.1, 2.9.2, 2.10 & 2.11)
* 0.8.1.1 (Scala 2.8.0, 2.9.1, 2.9.2, 2.10 & 2.11)
* 0.8.1 (Scala 2.8.0, 2.8.2, 2.9.1, 2.9.2, 2.10 & 2.11)
* 0.8.0
EOF
exit 1
}

createbuildenvironment()
{
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
}

rpmbuild()
{
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/SPECS/ulyaoth-kafka'"$kafkaversion"'-scala'"$scalaversion"'.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-kafka$kafkaversion-scala$scalaversion.spec
fi

su ulyaoth -c "spectool ulyaoth-kafka'"$kafkaversion"'-scala'"$scalaversion"'.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-kafka'"$kafkaversion"'-scala'"$scalaversion"'.spec"
}

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
kafkaversion=
scalaversion=
arch="$(uname -m)"
supportedkafka=('0.10.0.0' '0.9.0.1' '0.9.0.0' '0.8.2.2' '0.8.2.1' '0.8.2.0')
supportedscala=('2.11' '2.10' '2.9.2' '2.9.1' '2.8.2' '2.8.0')
kafka0.10.0.0scala=('2.11' '2.10')
kafka0.9.0.1scala=('2.11' '2.10')
kafka0.9.0.0scala=('2.11' '2.10')
kafka0.8.2.2scala=('2.11' '2.10' '2.9.2' '2.9.1')
kafka0.8.2.1scala=('2.11' '2.10' '2.9.2' '2.9.1')
kafka0.8.2.0scala=('2.11' '2.10' '2.9.2' '2.9.1')
kafka0.8.1.1scala=('2.11' '2.10' '2.9.2' '2.9.1' '2.8.0')
kafka0.8.1scala=('2.11' '2.10' '2.9.2' '2.9.1' '2.8.2' '2.8.0')

# Get the option that was in-putted by user.
while getopts ":h :l :b: :v:" opt; do
case $opt in
h)
  usage
;;
l)
  availablekafkaversions
;;
k)
  kafkaversion=$OPTARG
;;
s)
  scalaversion=$OPTARG
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
if [ -z "$kafkaversion" ];
then
  usage
elif [[ " ${supportedkafka[*]} " != *" $kafkaversion "* ]]
then
  echo Currently only the following kafka versions are supported: ${supportedkafka[*]}.
exit 1
elif [[ " ${supportedscala[*]} " != *" $scalaversion "* ]]
then
  echo "Please run the script with the -l option to see a list of supported versions. (.i.e ulyaoth-kafka.sh -l)"
exit 1
elif [[ " ${supportedkafka[*]} " != *" $kafka'"$kafkaversion"'scala "* ]]
then
  echo "Your Kafka and Scala combination is not possible please run the script with the -l option to see a list of supported versions. (.i.e ulyaoth-kafka.sh -l)"
exit 1
fi

# Create build user
useradd ulyaoth &> /dev/null

# Set build variables
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# Start the build process by calling the separate functions.
echo "Step 1: Create the build environment."
createbuildenvironment
echo "Step 2: Starting the rpmbuild process."
buildrpm
echo "Step 3: Cleaning your build environment."
clean
echo "Your RPM has been created and placed in your root directory."
exit 1