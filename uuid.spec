# TODO
# - conflicts with e2fsprogs uuid, rename libs with ossp prefix?
Summary:	Universally Unique Identifier library
Name:		uuid
Version:	1.5.1
Release:	0.1
License:	MIT
Group:		Libraries
URL:		http://www.ossp.org/pkg/lib/uuid/
Source0:	ftp://ftp.ossp.org/pkg/lib/uuid/%{name}-%{version}.tar.gz
# Source0-md5:	d7df0c4cb02dad7ce3e1ec8fc669f724
BuildRequires:	libtool
BuildRequires:	php-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OSSP uuid is a ISO-C:1999 application programming interface (API) and
corresponding command line interface (CLI) for the generation of DCE
1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally Unique
Identifier (UUID). It supports DCE 1.1 variant UUIDs of version 1
(time and node based), version 3 (name based, MD5), version 4 (random
number based) and version 5 (name based, SHA-1). Additional API
bindings are provided for the languages ISO-C++:1998, Perl:5 and
PHP:4/5. Optional backward compatibility exists for the ISO-C DCE-1.1
and Perl Data::UUID APIs.

%package devel
Summary:	Development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for OSSP uuid.

%package c++
Summary:	C++ support for Universally Unique Identifier library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ libraries for OSSP uuid.

%package c++-devel
Summary:	C++ development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description c++-devel
C++ development headers and libraries for OSSP uuid.

%package dce
Summary:	DCE support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description dce
DCE OSSP uuid library.

%package dce-devel
Summary:	DCE development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name}-dce = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description dce-devel
DCE development headers and libraries for OSSP uuid.

%package -n perl-%{name}
Summary:	Perl support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl OSSP uuid modules, which includes a Data::UUID replacement.

%package -n php-%{name}
Summary:	PHP support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n php-%{name}
PHP OSSP uuid module.

%package -n postgresql-%{name}
Summary:	PostgreSQL support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n postgresql-%{name}
PostgreSQL OSSP uuid module.

%prep
%setup -q

%build
# Build the library.
%configure \
	--disable-static \
	--without-perl \
	--without-php \
	--with-dce \
	--with-cxx \
	--with-pgsql

%{__make}

# Build the Perl module.
cd perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{rpmcflags}" \
	COMPAT=1
%{__make}
cd -

# Build the PHP module.
cd php
phpize
%configure \
	--enable-uuid
%{__make}
cd -

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,a}
#chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so.*.*.*

# Install the Perl modules.
%{__make} -C perl pure_install \
	PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the PHP module.
%{__make} -C php install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a

%if 0
%check
%{__make} check

cd perl
LD_LIBRARY_PATH=../.libs make test
cd -

cd php
LD_LIBRARY_PATH=../.libs make test
cd -
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%post dce -p /sbin/ldconfig
%postun dce -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HISTORY NEWS PORTING README SEEALSO THANKS TODO USERS
%attr(755,root,root) %{_bindir}/uuid
%attr(755,root,root) %{_libdir}/libuuid.so.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uuid-config
%{_includedir}/uuid.h
%{_libdir}/libuuid.so
%{_pkgconfigdir}/uuid.pc
%{_mandir}/man3/uuid.3*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuuid++.so.*

%files c++-devel
%defattr(644,root,root,755)
%{_includedir}/uuid++.hh
%{_libdir}/libuuid++.so
%{_mandir}/man3/uuid++.3*

%files dce
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuuid_dce.so.*

%files dce-devel
%defattr(644,root,root,755)
%{_includedir}/uuid_dce.h
%{_libdir}/libuuid_dce.so

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{perl_vendorarch}/OSSP*
%{_mandir}/man3/Data::UUID.3*
%{_mandir}/man3/OSSP::uuid.3*

%files -n php-%{name}
%defattr(644,root,root,755)
%{_libdir}/php/uuid.so

%files -n postgresql-%{name}
%defattr(644,root,root,755)
%{_libdir}/postgresql/uuid.so
%{_datadir}/postgresql/uuid.sql