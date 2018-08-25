%global php_extdir %(/apps/soft/qianbao-php-5.6.37/bin/php-config --extension-dir 2>/dev/null || echo "undefined")

Name: qianbao-php-redis
Version: 4.1.1
Release: 1%{?dist}
Summary: qianbao-php-redis-4.1.1
License: GPLv2
URL: https://www.gnu.org/software/libiconv/
Packager: xuzhigui@qianbao.com
Vendor: Qianbao-OPS
Source0: %{name}-%{version}.tar.gz
BuildRoot: %_topdir/BUILDROOT
Requires: qianbao-php

%description
Qianbao-php-redis version 4.1.1, if you have any other request, please contact xuzhigui@qianbao.com or ops

%prep
%setup -q 

%build
/apps/soft/qianbao-php-5.6.37/bin/phpize
%configure --with-php-config=/apps/soft/qianbao-php-5.6.37/bin/php-config
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{php_extdir}
make install INSTALL_ROOT=%{buildroot}
find %{buildroot} -name redis.so -exec /bin/mv {} %{buildroot}%{php_extdir} \;

QA_SKIP_BUILD_ROOT=1
QA_RPATHS=$[ 0x0001|0x0010 ]
export QA_SKIP_BUILD_ROOT
export QA_RPATHS

%pre

%post
if [ $1 == 1 ];then
[ -z "`grep '^extension_dir' /apps/soft/qianbao-php-5.6.37/etc/php.ini`" ] && echo "extension_dir = \"%{php_extdir}\"" >> /apps/soft/qianbao-php-5.6.37/etc/php.ini
  sed -i '/^extension_dir.*/a\extension = "redis.so"' /apps/soft/qianbao-php-5.6.37/etc/php.ini
fi

%preun
if [ $1 == 0 ];then
  /etc/init.d/php-fpm stop > /dev/null 2>&1
  sed -i '/redis.so/d' /apps/soft/qianbao-php-5.6.37/etc/php.ini
fi

%postun
if [ "$1" = 0 ] ; then
  /etc/init.d/php-fpm start > /dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/redis.so

%doc

%changelog
* Tue Aug 14 2018 xuzhigui 1.14-1
- Initial version

