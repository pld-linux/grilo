#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	vala		# do not build Vala API

Summary:	Framework for access to sources of multimedia content
Summary(pl.UTF-8):	Szkielet dostępu do źródeł treści multimedialnych
Name:		grilo
Version:	0.3.7
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo/0.3/%{name}-%{version}.tar.xz
# Source0-md5:	7c2c9a506e64e5f1a5fafd89ce53d9b0
URL:		http://live.gnome.org/Grilo
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 0.9
BuildRequires:	gtk+3-devel >= 3.14
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	liboauth-devel
BuildRequires:	libsoup-devel >= 2.42.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2
BuildRequires:	meson >= 0.37.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel >= 3.4.1
%{?with_vala:BuildRequires:	vala >= 2:0.27.0}
BuildRequires:	xz
Requires:	glib2 >= 1:2.44.0
Requires:	libsoup >= 2.42.0
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
Requires:	glib2-devel >= 1:2.44.0
Requires:	libxml2-devel >= 2

%description devel
Header files for grilo libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek grilo.

%package apidocs
Summary:	grilo API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek grilo
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-grilo
Vala API for grilo libraries.

%description -n vala-grilo -l pl.UTF-8
API języka Vala do bibliotek grilo.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Denable-gtk-doc=true} \
	%{?without_vala:-Denable-vala=false}
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
