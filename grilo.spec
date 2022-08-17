#
# Conditional build:
%bcond_with	libsoup3	# libsoup3 instead of libsoup 2
%bcond_without	apidocs		# API documentation
%bcond_without	vala		# Vala API

Summary:	Framework for access to sources of multimedia content
Summary(pl.UTF-8):	Szkielet dostępu do źródeł treści multimedialnych
Name:		grilo
Version:	0.3.15
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/grilo/0.3/%{name}-%{version}.tar.xz
# Source0-md5:	df4e68e2bba461f0aed61874d8e4e05a
URL:		https://wiki.gnome.org/Projects/Grilo
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gobject-introspection-devel >= 0.9
BuildRequires:	gtk+3-devel >= 3.14
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	liboauth-devel
%if %{with libsoup3}
BuildRequires:	libsoup3-devel >= 3.0
%else
BuildRequires:	libsoup-devel >= 2.42.0
%endif
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel >= 3.4.1
%{?with_vala:BuildRequires:	vala >= 2:0.27.0}
BuildRequires:	xz
Requires:	glib2 >= 1:2.66
Requires:	gtk+3 >= 3.14
%if %{with libsoup3}
Requires:	libsoup3 >= 3.0
%else
Requires:	libsoup >= 2.42.0
%endif
Requires:	totem-pl-parser >= 3.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grilo is a framework that provides access to various sources of
multimedia content, using a pluggable system.

%description -l pl.UTF-8
Grilo to szkielet zapewniający dostęp do różnych źródeł treści
multimedialnych przy użyciu systemu wtyczek.

%package devel
Summary:	Header files for grilo libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek grilo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.66
Requires:	libxml2-devel >= 2.0
Obsoletes:	grilo-static < 0.3.7

%description devel
Header files for grilo libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek grilo.

%package apidocs
Summary:	grilo API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek grilo
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API and internal documentation for grilo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki grilo.

%package -n vala-grilo
Summary:	Vala API for grilo libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek grilo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0
BuildArch:	noarch

%description -n vala-grilo
Vala API for grilo libraries.

%description -n vala-grilo -l pl.UTF-8
API języka Vala do bibliotek grilo.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Denable-gtk-doc=true} \
	%{?without_vala:-Denable-vala=false} \
	%{!?with_libsoup3:-Dsoup3=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md TODO
%attr(755,root,root) %{_bindir}/grilo-test-ui-0.3
%attr(755,root,root) %{_bindir}/grl-inspect-0.3
%attr(755,root,root) %{_bindir}/grl-launch-0.3
%attr(755,root,root) %{_libdir}/libgrilo-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrilo-0.3.so.0
%attr(755,root,root) %{_libdir}/libgrlnet-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlnet-0.3.so.0
%attr(755,root,root) %{_libdir}/libgrlpls-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlpls-0.3.so.0
%{_libdir}/girepository-1.0/Grl-0.3.typelib
%{_libdir}/girepository-1.0/GrlNet-0.3.typelib
%{_libdir}/girepository-1.0/GrlPls-0.3.typelib
%{_mandir}/man1/grilo-test-ui-0.3.1*
%{_mandir}/man1/grl-inspect-0.3.1*
%{_mandir}/man1/grl-launch-0.3.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgrilo-0.3.so
%attr(755,root,root) %{_libdir}/libgrlnet-0.3.so
%attr(755,root,root) %{_libdir}/libgrlpls-0.3.so
%{_includedir}/grilo-0.3
%{_pkgconfigdir}/grilo-0.3.pc
%{_pkgconfigdir}/grilo-net-0.3.pc
%{_pkgconfigdir}/grilo-pls-0.3.pc
%{_datadir}/gir-1.0/Grl-0.3.gir
%{_datadir}/gir-1.0/GrlNet-0.3.gir
%{_datadir}/gir-1.0/GrlPls-0.3.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/grilo
%endif

%if %{with vala}
%files -n vala-grilo
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/grilo-0.3.deps
%{_datadir}/vala/vapi/grilo-0.3.vapi
%{_datadir}/vala/vapi/grilo-net-0.3.deps
%{_datadir}/vala/vapi/grilo-net-0.3.vapi
%endif
