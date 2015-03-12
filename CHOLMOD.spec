#
# Conditional build:
%bcond_with	metis		# build with partition support (using metis lib)
#
Summary:	CHOLMOD: sparse supernodal Cholesky factorization and update/downdate
Summary(pl.UTF-8):	CHOLMOD - rzadki wielowęzłowy rozkład Cholesky'ego z poprawianiem
Name:		CHOLMOD
Version:	3.0.1
Release:	2
License:	GPL v2+ (some parts LGPL v2.1+)
Group:		Libraries
Source0:	http://www.cise.ufl.edu/research/sparse/cholmod/%{name}-%{version}.tar.gz
# Source0-md5:	677c2fac5bf480c125801ced2f51f9fe
Patch0:		%{name}-ufconfig.patch
Patch1:		%{name}-shared.patch
# http://www.cise.ufl.edu/research/sparse/cholmod/metis.patch (for METIS 5)
Patch2:		%{name}-metis.patch
URL:		http://www.cise.ufl.edu/research/sparse/cholmod/
BuildRequires:	AMD-devel >= 2.4.0
BuildRequires:	CAMD-devel >= 2.4.0
BuildRequires:	CCOLAMD-devel >= 2.9.0
BuildRequires:	COLAMD-devel >= 2.9.0
BuildRequires:	SuiteSparse_config-devel >= 4.3.0
BuildRequires:	blas-devel
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel
BuildRequires:	libtool >= 2:1.5
%if %{with metis}
BuildRequires:	metis-devel >= 5
%endif
Requires:	AMD >= 2.4.0
Requires:	CAMD >= 2.4.0
Requires:	CCOLAMD >= 2.9.0
Requires:	COLAMD >= 2.9.0
Requires:	SuiteSparse_config-libs >= 4.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CHOLMOD is a set of ANSI C routines for sparse Cholesky
factorization and update/downdate.

%description -l pl.UTF-8
CHOLMOD to zbiór procedur ANSI C do rzadkiego rozkładu Cholesky'ego z
poprawianiem.

%package devel
Summary:	Header files for CHOLMOD library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CHOLMOD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	AMD-devel >= 2.4.0
Requires:	CAMD-devel >= 2.4.0
Requires:	CCOLAMD-devel >= 2.9.0
Requires:	COLAMD-devel >= 2.9.0
Requires:	SuiteSparse_config-devel >= 4.3.0

%description devel
Header files for CHOLMOD library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CHOLMOD.

%package static
Summary:	Static CHOLMOD library
Summary(pl.UTF-8):	Statyczna biblioteka CHOLMOD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CHOLMOD library.

%description static -l pl.UTF-8
Statyczna biblioteka CHOLMOD.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	%{!?with_metis:CHOLMOD_CONFIG=-DNPARTITION} \
	%{?with_metis:WITH_METIS=1} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/cholmod

%{__make} -C Lib install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir}

install Include/*.h $RPM_BUILD_ROOT%{_includedir}/cholmod

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt Doc/ChangeLog
%attr(755,root,root) %{_libdir}/libcholmod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcholmod.so.0

%files devel
%defattr(644,root,root,755)
%doc Doc/UserGuide.pdf
%attr(755,root,root) %{_libdir}/libcholmod.so
%{_libdir}/libcholmod.la
%{_includedir}/cholmod

%files static
%defattr(644,root,root,755)
%{_libdir}/libcholmod.a
