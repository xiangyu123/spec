%define _user appuser
%define _group appuser

%define _prefix /apps/soft/qianbao-php-5.6.37
%define _sysconfdir   %{_prefix}/etc
%define _exec_prefix  %{_prefix}
%define _libdir       %{_prefix}/lib64
%define _datadir      %{_prefix}/share
%define _sbindir      %{_prefix}/sbin
%define _bindir       %{_prefix}/bin
%define _mandir       %{_prefix}/share/man
%define _libexecdir   %{_prefix}/libexec
%define _includedir   %{_prefix}/include

Name: qianbao-php
Version: 5.6.37
Release: 1%{?dist}
Summary: qianbao-php-5.6.37
License: GPLv2
URL: http://www.php.net
Packager: xuzhigui@qianbao.com
Vendor: Qianbao-OPS
Source0: %{name}-%{version}.tar.gz
Source1: libiconv-1.14.tar.gz
BuildRoot: %_topdir/BUILDROOT
BuildRequires:  gcc,gcc-c++,make,cmake,autoconf,automake
Requires: curl,curl-devel,libjpeg,libjpeg-devel,libpng,libpng-devel,freetype,freetype-devel,pcre,pcre-devel,ncurses-devel
Requires: mhash,ncurses-devel,bison,openssl-devel,libcurl-devel,gdbm-devel,openldap-devel,libtidy-devel,zlib-devel,libxml2-devel,libpng-devel
Requires: mcrypt
Requires: php-bcmath
Requires: bzip2-devel
Requires: libxml2-devel
Requires: libtool
Requires: libtool-ltdl,openssl-devel,openssl

%description
Qianbao-php version 5.6.37, if you have any other request, please contact xuzhigui@qianbao.com,wangshaoqian@qianbao.com or ops

%prep
%setup -q

%build
%configure --prefix=%{_prefix} --with-config-file-path=%{_sysconfdir} \
           --with-fpm-user=%{_user} --with-fpm-group=%{_group} \
           --with-bz2 --with-curl --enable-ftp --enable-sockets --disable-ipv6 \
           --with-gd --with-jpeg-dir --with-png-dir --enable-sysvsem --enable-sysvshm \
           --with-freetype-dir --enable-gd-native-ttf \
           --with-iconv-dir=/usr/local --enable-mbstring --enable-calendar \
           --with-gettext --with-ldap --with-libxml-dir --with-zlib \
           --with-pdo-mysql=mysqlnd --with-mysqli=mysqlnd --with-mysql=mysqlnd \
           --enable-dom --enable-xml --enable-fpm --with-libdir=lib64 --enable-bcmath \
           --enable-sysvsem --enable-inline-optimization --with-curl --enable-mbregex \
           --enable-fileinfo --enable-xml --with-mcrypt --with-xmlrpc --with-mhash \
           --enable-zip --enable-soap --with-openssl

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=$RPM_BUILD_ROOT
rm -rf %{buildroot}/{.channels,.depdb,.depdblock,.filemap,.lock,.registry}
%{__install} -p -D -m 0755 sapi/fpm/init.d.php-fpm %{buildroot}/etc/init.d/php-fpm
%{__install} -p -D -m 0644 php.ini-production %{buildroot}/%{_prefix}/etc/php.ini
%{__install} -p -D -m 0644 sapi/fpm/php-fpm.conf  %{buildroot}/%{_prefix}/etc/php-fpm.conf
%{__install} -p -D -m 0755 sapi/fpm/php-fpm_init.sh %{buildroot}/%{_prefix}/bin/php-fpm_init.sh

QA_SKIP_BUILD_ROOT=1
QA_RPATHS=$[ 0x0001|0x0010 ]
export QA_SKIP_BUILD_ROOT
export QA_RPATHS

%pre

%post
sh %{_prefix}/bin/php-fpm_init.sh %{_prefix}
cat >/etc/ld.so.conf.d/php.conf <<EOF
%{_libdir}
EOF
/sbin/ldconfig > /dev/null 2>&1
if [ $1 == 1 -a -z "`grep ^%{_user} /etc/passwd`" ]; then    # $1有3个值，代表动作，安装类型，处理类型
    groupadd %{_group} -g 500                                # 1：表示安装
    useradd -u 500 -g 500 -m %{_user}                        # 2：表示升级
fi 

%postun
if [ "$1" = 0 ] ; then
        /bin/rm -rf %{_prefix}
        /bin/rm -rf /etc/ld.so.conf.d/php.conf
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%attr(0755,root,root) /etc/init.d/php-fpm

%doc

%changelog
* Tue Aug 14 2018 xuzhigui,wangshaoqian 5.6.37-1
- Initial version

