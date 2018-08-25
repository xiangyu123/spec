%define _prefix       /usr/local/libiconv
%define _sysconfdir   %{_prefix}/etc
%define _exec_prefix  %{_prefix}
%define _libdir       %{_prefix}/lib64
%define _datadir      %{_prefix}/share
%define _sbindir      %{_prefix}/sbin
%define _bindir       %{_prefix}/bin
%define _mandir       %{_prefix}/share/man
%define _libexecdir   %{_prefix}/libexec
%define _includedir   %{_prefix}/include

Name: qianbao-libiconv
Version: 1.14
Release: 1%{?dist}
Summary: qianbao-libiconv-1.14
License: GPLv2
URL: https://www.gnu.org/software/libiconv/
Packager: xuzhigui@qianbao.com
Vendor: Qianbao-OPS
Source0: %{name}-%{version}.tar.gz
BuildRoot: %_topdir/BUILDROOT
BuildRequires:  gcc,gcc-c++,make,cmake,ncurses-devel,bison,openssl-devel
Requires: libtool
Requires: libtool-ltdl

%description
Qianbao-libiconv version 1.14, if you have any other request, please contact xuzhigui@qianbao.com or ops

%prep
%setup -q 

%build
%configure --prefix=%{_prefix}
CFLAGS="-O3 -fPIC"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

QA_SKIP_BUILD_ROOT=1
QA_RPATHS=$[ 0x0001|0x0010 ]
export QA_SKIP_BUILD_ROOT
export QA_RPATHS

%pre

%post
cat >/etc/ld.so.conf.d/libiconv.conf <<EOF
{_prefix}/lib
{_prefix}/lib64
EOF
/sbin/ldconfig > /dev/null 2>&1

%postun
if [ "$1" = 0 ] ; then
  rm -f /etc/ld.so.conf.d/libiconv.conf
  rm -rf %{_prefix}
  /sbin/ldconfig > /dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%doc

%changelog
* Tue Aug 14 2018 xuzhigui 1.14-1
- Initial version

