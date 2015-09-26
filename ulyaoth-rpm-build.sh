#!/bin/bash
# Argument = -h (shows the help information)
# Argument = -b (package name .i.e ulyaoth-nginx)
# Argument = -u (user name)
# Argument = -p (port)
# Argument = -r (repository)

arch="$(uname -m)"

serveros="$(grep -Eo '^[^ ]+' /etc/ulyaoth)"

usage()
{
cat << EOF
usage: $0 options

OPTIONS:
   -h  Shows this help information
   -b  Package name input (.i.e ulyaoth-nginx)
   -u  User name input for repository connection
   -p  Port input for ssh
   -r  Repository connection input
EOF
}

# Build the Packages of the Ulyaoth repository.
ulyaoth()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth/build-ulyaoth.sh ; chmod +x build-ulyaoth.sh ; ./build-ulyaoth.sh
}

ulyaoth-hiawatha()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hiawatha/build-ulyaoth-hiawatha.sh ; chmod +x build-ulyaoth-hiawatha.sh ; ./build-ulyaoth-hiawatha.sh
}

ulyaoth-monkey()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-monkey/build-ulyaoth-monkey.sh ; chmod +x build-ulyaoth-monkey.sh ; ./build-ulyaoth-monkey.sh
}

ulyaoth-mbedtls()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-mbedtls/build-ulyaoth-mbedtls.sh ; chmod +x build-ulyaoth-mbedtls.sh ; ./build-ulyaoth-mbedtls.sh
}

ulyaoth-mbedtls2()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-mbedtls/build-ulyaoth-mbedtls2.sh ; chmod +x build-ulyaoth-mbedtls2.sh ; ./build-ulyaoth-mbedtls2.sh
}

ulyaoth-kibana4()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-kibana/build-ulyaoth-kibana4.sh ; chmod +x build-ulyaoth-kibana4.sh ; ./build-ulyaoth-kibana4.sh
}

ulyaoth-tomcat-native()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-native/build-ulyaoth-tomcat-native.sh ; chmod +x build-ulyaoth-tomcat-native.sh ; ./build-ulyaoth-tomcat-native.sh
}

ulyaoth-tomcat8()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat/build-ulyaoth-tomcat8.sh ; chmod +x build-ulyaoth-tomcat8.sh ; ./build-ulyaoth-tomcat8.sh
}

ulyaoth-tomcat7()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat/build-ulyaoth-tomcat7.sh ; chmod +x build-ulyaoth-tomcat7.sh ; ./build-ulyaoth-tomcat7.sh
}

ulyaoth-tomcat6()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat/build-ulyaoth-tomcat6.sh ; chmod +x build-ulyaoth-tomcat6.sh ; ./build-ulyaoth-tomcat6.sh
}

ulyaoth-tomcat8-admin()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-admin/build-ulyaoth-tomcat8-admin.sh ; chmod +x build-ulyaoth-tomcat8-admin.sh ; ./build-ulyaoth-tomcat8-admin.sh
}

ulyaoth-tomcat7-admin()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-admin/build-ulyaoth-tomcat7-admin.sh ; chmod +x build-ulyaoth-tomcat7-admin.sh ; ./build-ulyaoth-tomcat7-admin.sh
}

ulyaoth-tomcat6-admin()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-admin/build-ulyaoth-tomcat6-admin.sh ; chmod +x build-ulyaoth-tomcat6-admin.sh ; ./build-ulyaoth-tomcat6-admin.sh
}

ulyaoth-tomcat8-docs()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-docs/build-ulyaoth-tomcat8-docs.sh ; chmod +x build-ulyaoth-tomcat8-docs.sh ; ./build-ulyaoth-tomcat8-docs.sh
}

ulyaoth-tomcat7-docs()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-docs/build-ulyaoth-tomcat7-docs.sh ; chmod +x build-ulyaoth-tomcat7-docs.sh ; ./build-ulyaoth-tomcat7-docs.sh
}

ulyaoth-tomcat6-docs()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-docs/build-ulyaoth-tomcat6-docs.sh ; chmod +x build-ulyaoth-tomcat6-docs.sh ; ./build-ulyaoth-tomcat6-docs.sh
}

ulyaoth-tomcat8-examples()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-examples/build-ulyaoth-tomcat8-examples.sh ; chmod +x build-ulyaoth-tomcat8-examples.sh ; ./build-ulyaoth-tomcat8-examples.sh
}

ulyaoth-tomcat7-examples()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-examples/build-ulyaoth-tomcat7-examples.sh ; chmod +x build-ulyaoth-tomcat7-examples.sh ; ./build-ulyaoth-tomcat7-examples.sh
}

ulyaoth-tomcat6-examples()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tomcat-examples/build-ulyaoth-tomcat6-examples.sh ; chmod +x build-ulyaoth-tomcat6-examples.sh ; ./build-ulyaoth-tomcat6-examples.sh
}

ulyaoth-fcgiwrap()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-fcgiwrap/build-ulyaoth-fcgiwrap.sh ; chmod +x build-ulyaoth-fcgiwrap.sh ; ./build-ulyaoth-fcgiwrap.sh
}

ulyaoth-logstash-forwarder()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-logstash-forwarder/build-ulyaoth-logstash-forwarder.sh ; chmod +x build-ulyaoth-logstash-forwarder.sh ; ./build-ulyaoth-logstash-forwarder.sh
}

spotify()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/spotify/build-ulyaoth-spotify.sh ; chmod +x build-ulyaoth-spotify.sh ; ./build-ulyaoth-spotify.sh
}

ulyaoth-nginx()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx/build-ulyaoth-nginx.sh ; chmod +x build-ulyaoth-nginx.sh ; ./build-ulyaoth-nginx.sh
}

ulyaoth-nginx-naxsi()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/build-ulyaoth-nginx-naxsi.sh ; chmod +x build-ulyaoth-nginx-naxsi.sh ; ./build-ulyaoth-nginx-naxsi.sh
}

ulyaoth-nginx-pagespeed()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-pagespeed.sh ; chmod +x build-ulyaoth-nginx-pagespeed.sh ; ./build-ulyaoth-nginx-pagespeed.sh
}

ulyaoth-nginx-pagespeed-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-pagespeed-selinux.sh ; chmod +x build-ulyaoth-nginx-pagespeed-selinux.sh ; ./build-ulyaoth-nginx-pagespeed-selinux.sh
}

ulyaoth-nginx-modsecurity()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/build-ulyaoth-nginx-modsecurity.sh ; chmod +x build-ulyaoth-nginx-modsecurity.sh ; ./build-ulyaoth-nginx-modsecurity.sh
}

ulyaoth-nginx-naxsi-masterbuild()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/build-ulyaoth-nginx-naxsi-masterbuild.sh ; chmod +x build-ulyaoth-nginx-naxsi-masterbuild.sh ; ./build-ulyaoth-nginx-naxsi-masterbuild.sh
}

ulyaoth-nginx-ironbee-masterbuild()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-ironbee/build-ulyaoth-nginx-ironbee-masterbuild.sh ; chmod +x build-ulyaoth-nginx-ironbee-masterbuild.sh ; ./build-ulyaoth-nginx-ironbee-masterbuild.sh
}

ulyaoth-nginx-passenger4()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger4.sh ; chmod +x build-ulyaoth-nginx-passenger4.sh ; ./build-ulyaoth-nginx-passenger4.sh
}

ulyaoth-nginx-passenger4-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger4-selinux.sh ; chmod +x build-ulyaoth-nginx-passenger4-selinux.sh ; ./build-ulyaoth-nginx-passenger4-selinux.sh
}

ulyaoth-nginx-passenger5()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger5.sh ; chmod +x build-ulyaoth-nginx-passenger5.sh ; ./build-ulyaoth-nginx-passenger5.sh
}

ulyaoth-nginx-passenger5-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger5-selinux.sh ; chmod +x build-ulyaoth-nginx-passenger5-selinux.sh ; ./build-ulyaoth-nginx-passenger5-selinux.sh
}

ulyaoth-nginx-mainline()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx/build-ulyaoth-nginx-mainline.sh ; chmod +x build-ulyaoth-nginx-mainline.sh ; ./build-ulyaoth-nginx-mainline.sh
}

ulyaoth-nginx-mainline-naxsi-masterbuild()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/build-ulyaoth-nginx-mainline-naxsi-masterbuild.sh ; chmod +x build-ulyaoth-nginx-mainline-naxsi-masterbuild.sh ; ./build-ulyaoth-nginx-mainline-naxsi-masterbuild.sh
}

ulyaoth-nginx-mainline-pagespeed()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-mainline-pagespeed.sh ; chmod +x build-ulyaoth-nginx-mainline-pagespeed.sh ; ./build-ulyaoth-nginx-mainline-pagespeed.sh
}

ulyaoth-nginx-mainline-pagespeed-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-mainline-pagespeed-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-pagespeed-selinux.sh ; ./build-ulyaoth-nginx-mainline-pagespeed-selinux.sh
}

ulyaoth-nginx-mainline-passenger4()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger4.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger4.sh ; ./build-ulyaoth-nginx-mainline-passenger4.sh
}

ulyaoth-nginx-mainline-passenger4-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger4-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger4-selinux.sh ; ./build-ulyaoth-nginx-mainline-passenger4-selinux.sh
}

ulyaoth-nginx-mainline-passenger5()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger5.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger5.sh ; ./build-ulyaoth-nginx-mainline-passenger5.sh
}

ulyaoth-nginx-mainline-passenger5-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger5-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger5-selinux.sh ; ./build-ulyaoth-nginx-mainline-passenger5-selinux.sh
}

ulyaoth-hhvm()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh
}

ulyaoth-banana()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-banana/build-ulyaoth-banana.sh ; chmod +x build-ulyaoth-banana.sh ; ./build-ulyaoth-banana.sh
}

ulyaoth-solr5()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-solr/build-ulyaoth-solr5.sh ; chmod +x build-ulyaoth-solr5.sh ; ./build-ulyaoth-solr5.sh
}

ulyaoth-solr5-docs()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-solr/build-ulyaoth-solr5-docs.sh ; chmod +x build-ulyaoth-solr5-docs.sh ; ./build-ulyaoth-solr5-docs.sh
}

ulyaoth-solr5-examples()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-solr/build-ulyaoth-solr5-examples.sh ; chmod +x build-ulyaoth-solr5-examples.sh ; ./build-ulyaoth-solr5-examples.sh
}

ulyaoth-httpdiff-masterbuild()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-httpdiff/build-ulyaoth-httpdiff-masterbuild.sh ; chmod +x build-ulyaoth-httpdiff-masterbuild.sh ; ./build-ulyaoth-httpdiff-masterbuild.sh
}

ulyaoth-tengine()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/build-ulyaoth-tengine.sh ; chmod +x build-ulyaoth-tengine.sh ; ./build-ulyaoth-tengine.sh
}

ulyaoth-tengine-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/build-ulyaoth-tengine-selinux.sh ; chmod +x build-ulyaoth-tengine-selinux.sh ; ./build-ulyaoth-tengine-selinux.sh
}

ulyaoth-tengine-development()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/build-ulyaoth-tengine-development.sh ; chmod +x build-ulyaoth-tengine-development.sh ; ./build-ulyaoth-tengine-development.sh
}

ulyaoth-tengine-development-selinux()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-tengine/build-ulyaoth-tengine-development-selinux.sh ; chmod +x build-ulyaoth-tengine-development-selinux.sh ; ./build-ulyaoth-tengine-development-selinux.sh
}

# Move package to repository server
scppackage()
{
  ssh -i $username.pem -o StrictHostKeyChecking=no -p $port $username@$repository "mkdir -p /home/$username/createrpm/$serveros/$arch"
  scp -i $username.pem -o StrictHostKeyChecking=no -P $port /root/*.rpm $username@$repository:/home/$username/createrpm/$serveros/$arch/
  ssh -i $username.pem -o StrictHostKeyChecking=no -p $port $username@$repository "chown -R $username:$username /home/$username/createrpm/"
}

package=

while getopts h:b:u:p:r:s: opt; do
case $opt in
h)
  usage
;;
b)
  package=$OPTARG
;;
u)
  username=$OPTARG
;;
p)
  port=$OPTARG
;;
r)
  repository=$OPTARG
;;
esac
done

$package
scppackage