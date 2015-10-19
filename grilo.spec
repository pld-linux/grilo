#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# do not build Vala API
#
Summary:	Framework for access to sources of multimedia content
Summary(pl.UTF-8):	Szkielet dostępu do źródeł treści multimedialnych
Name:		grilo
Version:	0.2.14
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	fce7eba405ada20fefcb877d534d9d4f
Patch0:		%{name}-sh.patch
URL:		http://live.gnome.org/Grilo
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.43.1
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.9
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	intltool >= 0.40.0
BuildRequires:	liboauth-devel
BuildRequires:	libsoup-devel >= 2.34.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel >= 3.4.1
%{?with_vala:BuildRequires:	vala >= 2:0.27.0}
BuildRequires:	xz
Requires:	glib2 >= 1:2.43.1
Requires:	libsoup >= 2.34.0
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
Requires:	glib2-devel >= 1:2.43.1
Requires:	libxml2-devel >= 2

%description devel
Header files for grilo libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek grilo.

%package static
Summary:	Static grilo libraries
Summary(pl.UTF-8):	Statyczne biblioteki grilo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static grilo libraries.

%description static -l pl.UTF-8
Statyczne biblioteki grilo.

%package apidocs
Summary:	grilo API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek grilo
Group:		Documentation

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

%description -n vala-grilo
Vala API for grilo libraries.

%description -n vala-grilo -l pl.UTF-8
API języka Vala do bibliotek grilo.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-debug \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/grilo-0.2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/grilo-test-ui-0.2
%attr(755,root,root) %{_bindir}/grl-inspect-0.2
%attr(755,root,root) %{_bindir}/grl-launch-0.2
%attr(755,root,root) %{_libdir}/libgrilo-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrilo-0.2.so.1
%attr(755,root,root) %{_libdir}/libgrlnet-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlnet-0.2.so.0
%attr(755,root,root) %{_libdir}/libgrlpls-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlpls-0.2.so.0
%dir %{_libdir}/grilo-0.2
%{_libdir}/girepository-1.0/Grl-0.2.typelib
%{_libdir}/girepository-1.0/GrlNet-0.2.typelib
%{_libdir}/girepository-1.0/GrlPls-0.2.typelib
%{_mandir}/man1/grilo-test-ui-0.2.1*
%{_mandir}/man1/grl-inspect-0.2.1*
%{_mandir}/man1/grl-launch-0.2.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgrilo-0.2.so
%attr(755,root,root) %{_libdir}/libgrlnet-0.2.so
%attr(755,root,root) %{_libdir}/libgrlpls-0.2.so
%{_includedir}/grilo-0.2
%{_pkgconfigdir}/grilo-0.2.pc
%{_pkgconfigdir}/grilo-net-0.2.pc
%{_pkgconfigdir}/grilo-pls-0.2.pc
%{_datadir}/gir-1.0/Grl-0.2.gir
%{_datadir}/gir-1.0/GrlNet-0.2.gir
%{_datadir}/gir-1.0/GrlPls-0.2.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgrilo-0.2.a
%{_libdir}/libgrlnet-0.2.a
%{_libdir}/libgrlpls-0.2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/grilo
%endif

%if %{with vala}
%files -n vala-grilo
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/grilo-0.2.deps
%{_datadir}/vala/vapi/grilo-0.2.vapi
%{_datadir}/vala/vapi/grilo-net-0.2.deps
%{_datadir}/vala/vapi/grilo-net-0.2.vapi
%endif
