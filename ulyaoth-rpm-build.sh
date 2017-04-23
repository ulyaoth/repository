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
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/build-ulyaoth.sh ; chmod +x build-ulyaoth.sh ; ./build-ulyaoth.sh
}

ulyaoth-iperf2()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-iperf/build-ulyaoth-iperf2.sh ; chmod +x build-ulyaoth-iperf2.sh ; ./build-ulyaoth-iperf2.sh
}

ulyaoth-iperf3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-iperf/build-ulyaoth-iperf3.sh ; chmod +x build-ulyaoth-iperf3.sh ; ./build-ulyaoth-iperf3.sh
}

ulyaoth-emojify()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-emojify/build-ulyaoth-emojify.sh ; chmod +x build-ulyaoth-emojify.sh ; ./build-ulyaoth-emojify.sh
}

ulyaoth-cmake()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-cmake/build-ulyaoth-cmake.sh ; chmod +x build-ulyaoth-cmake.sh ; ./build-ulyaoth-cmake.sh
}

ulyaoth-lego()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lego/build-ulyaoth-lego.sh ; chmod +x build-ulyaoth-lego.sh ; ./build-ulyaoth-lego.sh
}

ulyaoth-keepalived()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-keepalived/build-ulyaoth-keepalived.sh ; chmod +x build-ulyaoth-keepalived.sh ; ./build-ulyaoth-keepalived.sh
}

ulyaoth-geoipupdate()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-geoipupdate/build-ulyaoth-geoipupdate.sh ; chmod +x build-ulyaoth-geoipupdate.sh ; ./build-ulyaoth-geoipupdate.sh
}

ulyaoth-lua5.3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lua/build-ulyaoth-lua5.3.sh ; chmod +x build-ulyaoth-lua5.3.sh ; ./build-ulyaoth-lua5.3.sh
}

ulyaoth-hitch()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hitch/build-ulyaoth-hitch.sh ; chmod +x build-ulyaoth-hitch.sh ; ./build-ulyaoth-hitch.sh
}

ulyaoth-varnish5.1()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/build-ulyaoth-varnish5.1.sh ; chmod +x build-ulyaoth-varnish5.1.sh ; ./build-ulyaoth-varnish5.1.sh
}

ulyaoth-varnish5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/build-ulyaoth-varnish5.sh ; chmod +x build-ulyaoth-varnish5.sh ; ./build-ulyaoth-varnish5.sh
}

ulyaoth-varnish4.1()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/build-ulyaoth-varnish4.1.sh ; chmod +x build-ulyaoth-varnish4.1.sh ; ./build-ulyaoth-varnish4.1.sh
}

ulyaoth-varnish4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/build-ulyaoth-varnish4.sh ; chmod +x build-ulyaoth-varnish4.sh ; ./build-ulyaoth-varnish4.sh
}

ulyaoth-varnish3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/build-ulyaoth-varnish3.sh ; chmod +x build-ulyaoth-varnish3.sh ; ./build-ulyaoth-varnish3.sh
}

ulyaoth-haproxy1.7()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/build-ulyaoth-haproxy1.7.sh ; chmod +x build-ulyaoth-haproxy1.7.sh ; ./build-ulyaoth-haproxy1.7.sh
}

ulyaoth-haproxy1.6()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/build-ulyaoth-haproxy1.6.sh ; chmod +x build-ulyaoth-haproxy1.6.sh ; ./build-ulyaoth-haproxy1.6.sh
}

ulyaoth-haproxy1.5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/build-ulyaoth-haproxy1.5.sh ; chmod +x build-ulyaoth-haproxy1.5.sh ; ./build-ulyaoth-haproxy1.5.sh
}

ulyaoth-haproxy1.4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/build-ulyaoth-haproxy1.4.sh ; chmod +x build-ulyaoth-haproxy1.4.sh ; ./build-ulyaoth-haproxy1.4.sh
}

ulyaoth-haproxy1.3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/build-ulyaoth-haproxy1.3.sh ; chmod +x build-ulyaoth-haproxy1.3.sh ; ./build-ulyaoth-haproxy1.3.sh
}

ulyaoth-beats()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-beats/build-ulyaoth-beats.sh ; chmod +x build-ulyaoth-beats.sh ; ./build-ulyaoth-beats.sh
}

ulyaoth-screen()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-screen/build-ulyaoth-screen.sh ; chmod +x build-ulyaoth-screen.sh ; ./build-ulyaoth-screen.sh
}

ulyaoth-tmux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tmux/build-ulyaoth-tmux.sh ; chmod +x build-ulyaoth-tmux.sh ; ./build-ulyaoth-tmux.sh
}

ulyaoth-kafka-manager()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka-manager/build-ulyaoth-kafka-manager.sh ; chmod +x build-ulyaoth-kafka-manager.sh ; ./build-ulyaoth-kafka-manager.sh
}

ulyaoth-leveldb()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-leveldb/build-ulyaoth-leveldb.sh ; chmod +x build-ulyaoth-leveldb.sh ; ./build-ulyaoth-leveldb.sh
}

ulyaoth-smtpping()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-smtpping/build-ulyaoth-smtpping.sh ; chmod +x build-ulyaoth-smtpping.sh ; ./build-ulyaoth-smtpping.sh
}

ulyaoth-httping()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-httping/build-ulyaoth-httping.sh ; chmod +x build-ulyaoth-httping.sh ; ./build-ulyaoth-httping.sh
}

ulyaoth-hhvm3.13()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh -b 3.13 -v 3.13.2
}

ulyaoth-hhvm3.12()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh -b 3.12 -v 3.12.2
}

ulyaoth-hhvm3.11()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh -b 3.11 -v 3.11.1
}

ulyaoth-hhvm3.9()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh -b 3.9 -v 3.9.3
}

ulyaoth-hhvm3.6()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh -b 3.6 -v 3.6.6
}

ulyaoth-fuse-s3fs()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fuse-s3fs/build-ulyaoth-fuse-s3fs.sh ; chmod +x build-ulyaoth-fuse-s3fs.sh ; ./build-ulyaoth-fuse-s3fs.sh
}

ulyaoth-fuse()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fuse/build-ulyaoth-fuse.sh ; chmod +x build-ulyaoth-fuse.sh ; ./build-ulyaoth-fuse.sh
}

ulyaoth-fuse3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fuse/build-ulyaoth-fuse3.sh ; chmod +x build-ulyaoth-fuse3.sh ; ./build-ulyaoth-fuse3.sh
}

ulyaoth-vegeta()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-vegeta/build-ulyaoth-vegeta.sh ; chmod +x build-ulyaoth-vegeta.sh ; ./build-ulyaoth-vegeta.sh
}

ulyaoth-kafka8-scala2.11()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka8-scala2.11.sh ; chmod +x build-ulyaoth-kafka8-scala2.11.sh ; ./build-ulyaoth-kafka8-scala2.11.sh
}

ulyaoth-kafka8-scala2.10()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka8-scala2.10.sh ; chmod +x build-ulyaoth-kafka8-scala2.10.sh ; ./build-ulyaoth-kafka8-scala2.10.sh
}

ulyaoth-kafka8-scala2.9.2()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka8-scala2.9.2.sh ; chmod +x build-ulyaoth-kafka8-scala2.9.2.sh ; ./build-ulyaoth-kafka8-scala2.9.2.sh
}

ulyaoth-kafka8-scala2.9.1()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka8-scala2.9.1.sh ; chmod +x build-ulyaoth-kafka8-scala2.9.1.sh ; ./build-ulyaoth-kafka8-scala2.9.1.sh
}

ulyaoth-kafka9-scala2.11()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka9-scala2.11.sh ; chmod +x build-ulyaoth-kafka9-scala2.11.sh ; ./build-ulyaoth-kafka9-scala2.11.sh
}

ulyaoth-kafka9-scala2.10()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kafka/build-ulyaoth-kafka9-scala2.10.sh ; chmod +x build-ulyaoth-kafka9-scala2.10.sh ; ./build-ulyaoth-kafka9-scala2.10.sh
}

ulyaoth-wolfssl()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-wolfssl/build-ulyaoth-wolfssl.sh ; chmod +x build-ulyaoth-wolfssl.sh ; ./build-ulyaoth-wolfssl.sh
}

ulyaoth-go()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-go/build-ulyaoth-go.sh ; chmod +x build-ulyaoth-go.sh ; ./build-ulyaoth-go.sh
}

ulyaoth-openssl0.9.8()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/build-ulyaoth-openssl0.9.8.sh ; chmod +x build-ulyaoth-openssl0.9.8.sh ; ./build-ulyaoth-openssl0.9.8.sh
}

ulyaoth-openssl1.0.0()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/build-ulyaoth-openssl1.0.0.sh ; chmod +x build-ulyaoth-openssl1.0.0.sh ; ./build-ulyaoth-openssl1.0.0.sh
}

ulyaoth-openssl1.0.1()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/build-ulyaoth-openssl1.0.1.sh ; chmod +x build-ulyaoth-openssl1.0.1.sh ; ./build-ulyaoth-openssl1.0.1.sh
}

ulyaoth-openssl1.0.2()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/build-ulyaoth-openssl1.0.2.sh ; chmod +x build-ulyaoth-openssl1.0.2.sh ; ./build-ulyaoth-openssl1.0.2.sh
}

ulyaoth-openssl1.1.0()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/build-ulyaoth-openssl1.1.0.sh ; chmod +x build-ulyaoth-openssl1.1.0.sh ; ./build-ulyaoth-openssl1.1.0.sh
}

ulyaoth-apr()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-apr/build-ulyaoth-apr.sh ; chmod +x build-ulyaoth-apr.sh ; ./build-ulyaoth-apr.sh
}

ulyaoth-zookeeper3.5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/build-ulyaoth-zookeeper3.5.sh ; chmod +x build-ulyaoth-zookeeper3.5.sh ; ./build-ulyaoth-zookeeper3.5.sh
}

ulyaoth-zookeeper3.4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-zookeeper/build-ulyaoth-zookeeper3.4.sh ; chmod +x build-ulyaoth-zookeeper3.4.sh ; ./build-ulyaoth-zookeeper3.4.sh
}

ulyaoth-redis3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/build-ulyaoth-redis3.sh ; chmod +x build-ulyaoth-redis3.sh ; ./build-ulyaoth-redis3.sh
}

ulyaoth-ironbee()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-ironbee/build-ulyaoth-ironbee.sh ; chmod +x build-ulyaoth-ironbee.sh ; ./build-ulyaoth-ironbee.sh
}

ulyaoth-hiawatha()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hiawatha/build-ulyaoth-hiawatha.sh ; chmod +x build-ulyaoth-hiawatha.sh ; ./build-ulyaoth-hiawatha.sh
}

ulyaoth-monkey()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-monkey/build-ulyaoth-monkey.sh ; chmod +x build-ulyaoth-monkey.sh ; ./build-ulyaoth-monkey.sh
}

ulyaoth-mbedtls()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/build-ulyaoth-mbedtls.sh ; chmod +x build-ulyaoth-mbedtls.sh ; ./build-ulyaoth-mbedtls.sh
}

ulyaoth-mbedtls2.1()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/build-ulyaoth-mbedtls2.1.sh ; chmod +x build-ulyaoth-mbedtls2.1.sh ; ./build-ulyaoth-mbedtls2.1.sh
}

ulyaoth-mbedtls2.2()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/build-ulyaoth-mbedtls2.2.sh ; chmod +x build-ulyaoth-mbedtls2.2.sh ; ./build-ulyaoth-mbedtls2.2.sh
}

ulyaoth-mbedtls2.3()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/build-ulyaoth-mbedtls2.3.sh ; chmod +x build-ulyaoth-mbedtls2.3.sh ; ./build-ulyaoth-mbedtls2.3.sh
}

ulyaoth-mbedtls2.4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/build-ulyaoth-mbedtls2.4.sh ; chmod +x build-ulyaoth-mbedtls2.4.sh ; ./build-ulyaoth-mbedtls2.4.sh
}

ulyaoth-kibana4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kibana/build-ulyaoth-kibana4.sh ; chmod +x build-ulyaoth-kibana4.sh ; ./build-ulyaoth-kibana4.sh
}

ulyaoth-kibana5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-kibana/build-ulyaoth-kibana5.sh ; chmod +x build-ulyaoth-kibana5.sh ; ./build-ulyaoth-kibana5.sh
}

ulyaoth-tomcat-multi()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/build-ulyaoth-tomcat-multi.sh ; chmod +x build-ulyaoth-tomcat-multi.sh ; ./build-ulyaoth-tomcat-multi.sh
}

ulyaoth-tomcat-native()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/build-ulyaoth-tomcat-native.sh ; chmod +x build-ulyaoth-tomcat-native.sh ; ./build-ulyaoth-tomcat-native.sh
}

ulyaoth-tomcat-native1.2()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/build-ulyaoth-tomcat-native1.2.sh ; chmod +x build-ulyaoth-tomcat-native1.2.sh ; ./build-ulyaoth-tomcat-native1.2.sh
}

ulyaoth-tomcat9()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/build-ulyaoth-tomcat9.sh ; chmod +x build-ulyaoth-tomcat9.sh ; ./build-ulyaoth-tomcat9.sh
}

ulyaoth-tomcat8.5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/build-ulyaoth-tomcat8.5.sh ; chmod +x build-ulyaoth-tomcat8.5.sh ; ./build-ulyaoth-tomcat8.5.sh
}

ulyaoth-tomcat8()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/build-ulyaoth-tomcat8.sh ; chmod +x build-ulyaoth-tomcat8.sh ; ./build-ulyaoth-tomcat8.sh
}

ulyaoth-tomcat7()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/build-ulyaoth-tomcat7.sh ; chmod +x build-ulyaoth-tomcat7.sh ; ./build-ulyaoth-tomcat7.sh
}

ulyaoth-tomcat6()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/build-ulyaoth-tomcat6.sh ; chmod +x build-ulyaoth-tomcat6.sh ; ./build-ulyaoth-tomcat6.sh
}

ulyaoth-fcgiwrap()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fcgiwrap/build-ulyaoth-fcgiwrap.sh ; chmod +x build-ulyaoth-fcgiwrap.sh ; ./build-ulyaoth-fcgiwrap.sh
}

ulyaoth-logstash-forwarder()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash-forwarder/build-ulyaoth-logstash-forwarder.sh ; chmod +x build-ulyaoth-logstash-forwarder.sh ; ./build-ulyaoth-logstash-forwarder.sh
}

ulyaoth-logstash()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-logstash/build-ulyaoth-logstash.sh ; chmod +x build-ulyaoth-logstash.sh ; ./build-ulyaoth-logstash.sh
}

spotify()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/spotify/build-ulyaoth-spotify.sh ; chmod +x build-ulyaoth-spotify.sh ; ./build-ulyaoth-spotify.sh
}

ulyaoth-nginx()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/build-ulyaoth-nginx-stable-or-mainline.sh ; chmod +x build-ulyaoth-nginx-stable-or-mainline.sh ; ./build-ulyaoth-nginx-stable-or-mainline.sh stable
}

ulyaoth-nginx-naxsi()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/build-ulyaoth-nginx-naxsi.sh ; chmod +x build-ulyaoth-nginx-naxsi.sh ; ./build-ulyaoth-nginx-naxsi.sh
}

ulyaoth-nginx-pagespeed()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-pagespeed.sh ; chmod +x build-ulyaoth-nginx-pagespeed.sh ; ./build-ulyaoth-nginx-pagespeed.sh
}

ulyaoth-nginx-pagespeed-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-pagespeed-selinux.sh ; chmod +x build-ulyaoth-nginx-pagespeed-selinux.sh ; ./build-ulyaoth-nginx-pagespeed-selinux.sh
}

ulyaoth-nginx-modsecurity()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modsecurity/build-ulyaoth-nginx-modsecurity-with-nginx-fix.sh ; chmod +x build-ulyaoth-nginx-modsecurity-with-nginx-fix.sh ; ./build-ulyaoth-nginx-modsecurity-with-nginx-fix.sh
}

ulyaoth-nginx-naxsi-masterbuild()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/build-ulyaoth-nginx-naxsi-masterbuild.sh ; chmod +x build-ulyaoth-nginx-naxsi-masterbuild.sh ; ./build-ulyaoth-nginx-naxsi-masterbuild.sh
}

ulyaoth-nginx-ironbee()
{
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-ironbee/build-ulyaoth-nginx-ironbee.sh ; chmod +x build-ulyaoth-nginx-ironbee.sh ; ./build-ulyaoth-nginx-ironbee.sh
}

ulyaoth-nginx-passenger4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger4.sh ; chmod +x build-ulyaoth-nginx-passenger4.sh ; ./build-ulyaoth-nginx-passenger4.sh
}

ulyaoth-nginx-passenger4-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger4-selinux.sh ; chmod +x build-ulyaoth-nginx-passenger4-selinux.sh ; ./build-ulyaoth-nginx-passenger4-selinux.sh
}

ulyaoth-nginx-passenger5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger5.sh ; chmod +x build-ulyaoth-nginx-passenger5.sh ; ./build-ulyaoth-nginx-passenger5.sh
}

ulyaoth-nginx-passenger5-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-passenger5-selinux.sh ; chmod +x build-ulyaoth-nginx-passenger5-selinux.sh ; ./build-ulyaoth-nginx-passenger5-selinux.sh
}

ulyaoth-nginx-mainline()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/build-ulyaoth-nginx-stable-or-mainline.sh ; chmod +x build-ulyaoth-nginx-stable-or-mainline.sh ; ./build-ulyaoth-nginx-stable-or-mainline.sh mainline
}

ulyaoth-nginx-mainline-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/build-ulyaoth-nginx-mainline-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-selinux.sh ; ./build-ulyaoth-nginx-mainline-selinux.sh
}

ulyaoth-nginx-mainline-pagespeed()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-mainline-pagespeed.sh ; chmod +x build-ulyaoth-nginx-mainline-pagespeed.sh ; ./build-ulyaoth-nginx-mainline-pagespeed.sh
}

ulyaoth-nginx-mainline-pagespeed-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-pagespeed/build-ulyaoth-nginx-mainline-pagespeed-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-pagespeed-selinux.sh ; ./build-ulyaoth-nginx-mainline-pagespeed-selinux.sh
}

ulyaoth-nginx-mainline-passenger4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger4.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger4.sh ; ./build-ulyaoth-nginx-mainline-passenger4.sh
}

ulyaoth-nginx-mainline-passenger4-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger4-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger4-selinux.sh ; ./build-ulyaoth-nginx-mainline-passenger4-selinux.sh
}

ulyaoth-nginx-mainline-passenger5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger5.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger5.sh ; ./build-ulyaoth-nginx-mainline-passenger5.sh
}

ulyaoth-nginx-mainline-passenger5-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/build-ulyaoth-nginx-mainline-passenger5-selinux.sh ; chmod +x build-ulyaoth-nginx-mainline-passenger5-selinux.sh ; ./build-ulyaoth-nginx-mainline-passenger5-selinux.sh
}

ulyaoth-hhvm()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hhvm/build-ulyaoth-hhvm.sh ; chmod +x build-ulyaoth-hhvm.sh ; ./build-ulyaoth-hhvm.sh
}

ulyaoth-banana()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-banana/build-ulyaoth-banana.sh ; chmod +x build-ulyaoth-banana.sh ; ./build-ulyaoth-banana.sh
}

ulyaoth-solr4()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr4.sh ; chmod +x build-ulyaoth-solr4.sh ; ./build-ulyaoth-solr4.sh
}

ulyaoth-solr5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr5.sh ; chmod +x build-ulyaoth-solr5.sh ; ./build-ulyaoth-solr5.sh
}

ulyaoth-solr5-docs()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr5-docs.sh ; chmod +x build-ulyaoth-solr5-docs.sh ; ./build-ulyaoth-solr5-docs.sh
}

ulyaoth-solr5-examples()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr5-examples.sh ; chmod +x build-ulyaoth-solr5-examples.sh ; ./build-ulyaoth-solr5-examples.sh
}

ulyaoth-solr6()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr6.sh ; chmod +x build-ulyaoth-solr6.sh ; ./build-ulyaoth-solr6.sh
}

ulyaoth-solr6-docs()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr6-docs.sh ; chmod +x build-ulyaoth-solr6-docs.sh ; ./build-ulyaoth-solr6-docs.sh
}

ulyaoth-solr6-examples()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-solr/build-ulyaoth-solr6-examples.sh ; chmod +x build-ulyaoth-solr6-examples.sh ; ./build-ulyaoth-solr6-examples.sh
}

ulyaoth-httpdiff()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-httpdiff/build-ulyaoth-httpdiff.sh ; chmod +x build-ulyaoth-httpdiff.sh ; ./build-ulyaoth-httpdiff.sh
}

ulyaoth-tengine()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/build-ulyaoth-tengine.sh ; chmod +x build-ulyaoth-tengine.sh ; ./build-ulyaoth-tengine.sh
}

ulyaoth-tengine-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/build-ulyaoth-tengine-selinux.sh ; chmod +x build-ulyaoth-tengine-selinux.sh ; ./build-ulyaoth-tengine-selinux.sh
}

ulyaoth-tengine-development()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/build-ulyaoth-tengine-development.sh ; chmod +x build-ulyaoth-tengine-development.sh ; ./build-ulyaoth-tengine-development.sh
}

ulyaoth-tengine-development-selinux()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/build-ulyaoth-tengine-development-selinux.sh ; chmod +x build-ulyaoth-tengine-development-selinux.sh ; ./build-ulyaoth-tengine-development-selinux.sh
}

ulyaoth-jsvc()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-jsvc/build-ulyaoth-jsvc.sh ; chmod +x build-ulyaoth-jsvc.sh ; ./build-ulyaoth-jsvc.sh
}

ulyaoth-terraform()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-terraform/build-ulyaoth-terraform.sh ; chmod +x build-ulyaoth-terraform.sh ; ./build-ulyaoth-terraform.sh
}

ulyaoth-nginx-stable-and-mainline-module-devel-kit()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh devel-kit
}

ulyaoth-nginx-stable-and-mainline-module-headers-more()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh headers-more
}

ulyaoth-nginx-stable-and-mainline-module-form-input()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh form-input
}

ulyaoth-nginx-stable-and-mainline-module-pam()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh pam
}

ulyaoth-nginx-stable-and-mainline-module-echo()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh echo
}

ulyaoth-nginx-stable-and-mainline-module-encrypted-session()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh encrypted-session
}

ulyaoth-nginx-stable-and-mainline-module-array-var()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh array-var
}

ulyaoth-nginx-stable-and-mainline-module-naxsi()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh naxsi
}

ulyaoth-nginx-stable-and-mainline-module-passenger5()
{
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/build-ulyaoth-nginx-stable-and-mainline-modules.sh ; chmod +x build-ulyaoth-nginx-stable-and-mainline-modules.sh ; ./build-ulyaoth-nginx-stable-and-mainline-modules.sh passenger5
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