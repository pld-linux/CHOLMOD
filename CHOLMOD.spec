#
# Conditional build:
%bcond_with	metis		# build with metis lib
#
Summary:	CHOLMOD: sparse supernodal Cholesky factorization and update/downdate
Summary(pl.UTF-8):	CHOLMOD - rzadki wielowęzłowy rozkład Cholesky'ego z poprawianiem
Name:		CHOLMOD
Version:	1.6.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.cise.ufl.edu/research/sparse/cholmod/%{name}-%{version}.tar.gz
# Source0-md5:	d07af9879992e597fb197daaefd2eb19
Patch0:		%{name}-ufconfig.patch
Patch1:		%{name}-shared.patch
URL:		http://www.cise.ufl.edu/research/sparse/cholmod/
BuildRequires:	AMD-devel
BuildRequires:	CAMD-devel
BuildRequires:	CCOLAMD-devel
BuildRequires:	COLAMD-devel
BuildRequires:	UFconfig
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	libtool >= 2:1.5
%{?with_metis:BuildRequires:	metis-devel}
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
Requires:	UFconfig

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

%build
%{__make} \
	CC="%{__cc}" \
%if %{with metis}
	CFLAGS="%{rpmcflags} -fPIC" \
%else
	CFLAGS="%{rpmcflags} -fPIC -DNPARTITION" \
	METIS= \
%endif
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
%doc README.txt Doc/UserGuide.pdf
%attr(755,root,root) %{_libdir}/libcholmod.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcholmod.so
%{_libdir}/libcholmod.la
%{_includedir}/cholmod

%files static
%defattr(644,root,root,755)
%{_libdir}/libcholmod.a
