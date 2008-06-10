# TODO
# - conflicts with e2fsprogs uuid, rename libs with ossp prefix?
# - rename include ossp/uuid.h?
# - rename package to ossp-uuid?
# - fix bindings compilation
#
# Conditional build:
%bcond_without	php		# build PHP binding
%bcond_with	perl		# build Perl binding
%bcond_without	pgsql		# build postgresql binding
#
Summary:	Universally Unique Identifier library
Name:		uuid
Version:	1.6.1
Release:	0.2
License:	MIT
Group:		Libraries
URL:		http://www.ossp.org/pkg/lib/uuid/
Source0:	ftp://ftp.ossp.org/pkg/lib/uuid/%{name}-%{version}.tar.gz
# Source0-md5:	18c8875411da07fe4503fdfc2136bf46
BuildRequires:	libtool
%{?with_php:BuildRequires:	php-devel >= 3:5.0.0}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.344
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
Summary:	OSSP uuid Perl Binding
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl OSSP uuid modules, which includes a Data::UUID replacement.

%package -n php-%{name}
Summary:	PHP support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4

%description -n php-%{name}
UUID is a PHP extension for the creation of Universally Unique
Identifiers (UUID).

%package -n postgresql-%{name}
Summary:	OSSP uuid bindings for PostgreSQL
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
	--with-dce \
	--with-cxx \
	--with%{!?with_perl:out}-perl \
	--with%{!?with_php:out}-php \
	--with%{!?with_pgsql:out}-pgsql

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with php}
install -d $RPM_BUILD_ROOT%{_datadir}/php
mv $RPM_BUILD_ROOT{%{php_extensiondir},%{_datadir}/php}/%{name}.php
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
%attr(755,root,root) %{_libdir}/libuuid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuuid.so.16
%{_mandir}/man1/uuid.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uuid-config
%{_includedir}/uuid.h
%{_libdir}/libuuid.so
%{_pkgconfigdir}/uuid.pc
%{_mandir}/man3/uuid.3*
%{_mandir}/man1/uuid-config.1*
%{_libdir}/libuuid.la

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuuid++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuuid++.so.16

%files c++-devel
%defattr(644,root,root,755)
%{_includedir}/uuid++.hh
%{_libdir}/libuuid++.so
%{_libdir}/libuuid++.la
%{_mandir}/man3/uuid++.3*

%files dce
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuuid_dce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuuid_dce.so.16

%files dce-devel
%defattr(644,root,root,755)
%{_includedir}/uuid_dce.h
%{_libdir}/libuuid_dce.so
%{_libdir}/libuuid_dce.la

%if %{with perl}
%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{perl_vendorarch}/OSSP*
%{_mandir}/man3/Data::UUID.3*
%{_mandir}/man3/OSSP::uuid.3*
%endif

%if %{with php}
%files -n php-%{name}
%defattr(644,root,root,755)
%{_libdir}/php/uuid.so
%{_datadir}/php/uuid.php
%endif

%if %{with pgsql}
%files -n postgresql-%{name}
%defattr(644,root,root,755)
%{_libdir}/postgresql/uuid.so
%{_datadir}/postgresql/uuid.sql
%endif
