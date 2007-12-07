#
# Conditional build:
%bcond_with	metis		# build with metis lib
#
Summary:	CHOLMOD: sparse supernodal Cholesky factorization and update/downdate
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
BuildRequires:	blas-devel
BuildRequires:	CCOLAMD-devel
BuildRequires:	AMD-devel
BuildRequires:	CAMD-devel
BuildRequires:	COLAMD-devel
BuildRequires:	lapack-devel
BuildRequires:	libtool >= 2:1.5
%{?with_metis:BuildRequires:	metis-devel}
BuildRequires:	UFconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CHOLMOD is a set of ANSI C routines for sparse Cholesky
factorization and update/downdate.

%package devel
Summary:	Header files for cholmod library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cholmod
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	UFconfig

%description devel
Header files for cholmod library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cholmod.

%package static
Summary:	Static cholmod library
Summary(pl.UTF-8):	Statyczna biblioteka cholmod
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cholmod library.

%description static -l pl.UTF-8
Statyczna biblioteka cholmod.

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
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} -C Lib install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir}

install Include/*.h $RPM_BUILD_ROOT%{_includedir}

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
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcholmod.a
