# $Id$

%define php_extdir %(php-config --extension-dir)

Summary: PHP accelerator, optimizer, encoder and dynamic content cacher
Name: php-mmcache
Version: 2.4.6
Release: 1
License: GPL
Group: Development/Languages
URL: http://turck-mmcache.sourceforge.net/
Source: http://dl.sf.net/turck-mmcache/turck-mmcache-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
Provides: php-zend_extension
BuildRequires: php, php-devel
# Required by phpize
BuildRequires: autoconf, automake, libtool, gcc-c++

%description
Turck MMCache is a free open source PHP accelerator, optimizer, encoder and
dynamic content cache for PHP. It increases performance of PHP scripts by
caching them in compiled state, so that the overhead of compiling is almost
completely eliminated. Also it uses some optimizations to speed up execution
of PHP scripts. Turck MMCache typically reduces server load and increases the
speed of your PHP code by 1-10 times. 


%prep 
%setup -n turck-mmcache-%{version}


%build
phpize
%configure
%{__make}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# The cache directory where pre-compiled files will reside
%{__mkdir_p} %{buildroot}%{_localstatedir}/cache/php-mmcache

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/mmcache.ini << 'EOF'
; Enable Turck MMCache extension module
zend_extension = %{php_extdir}/mmcache.so

; Options to the MMCache module
mmcache.cache_dir = %{_localstatedir}/cache/php-mmcache
mmcache.shm_size = 8
mmcache.enable = 1
mmcache.optimizer = 1
mmcache.check_mtime = 1
mmcache.debug = 0
mmcache.filter = ""
mmcache.shm_max = 0
mmcache.shm_ttl = 0
mmcache.shm_prune_period = 0
mmcache.keys = shm
mmcache.sessions = shm
mmcache.content = shm

EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc CREDITS EXPERIMENTAL LICENSE README README.loader TODO
%config(noreplace) %{_sysconfdir}/php.d/mmcache.ini
%{php_extdir}/mmcache.so
%attr(0750, apache, apache) %{_localstatedir}/cache/php-mmcache


%changelog
* Mon May 10 2004 Matthias Saou <http://freshrpms.net/> 2.4.6-1
- Initial RPM release.

