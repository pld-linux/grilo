#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# do not build Vala API
#
Summary:	Framework for access to sources of multimedia content
Name:		grilo
Version:	0.2.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	586b6f4f1cbffbba765ffb9384e26803
URL:		http://live.gnome.org/Grilo
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.9
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libsoup-devel >= 2.34.0
BuildRequires:	libtool >= 2.2.6
BuildRequires:	libxml2-devel
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.16.0}
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grilo is a framework that provides access to various sources of
multimedia content, using a pluggable system.

%package devel
Summary:	Header files for grilo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki grilo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30.0
Requires:	libxml2-devel

%description devel
Header files for grilo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki grilo.

%package static
Summary:	Static grilo library
Summary(pl.UTF-8):	Statyczna biblioteka grilo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static grilo library.

%description static -l pl.UTF-8
Statyczna biblioteka grilo.

%package apidocs
Summary:	grilo API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki grilo
Group:		Documentation

%description apidocs
API and internal documentation for grilo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki grilo.

%package -n vala-grilo
Summary:	grilo API for Vala language
Summary(pl.UTF-8):	API grilo dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-grilo
grilo API for Vala language.

%description -n vala-grilo -l pl.UTF-8
API grilo dla języka Vala.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-debug \
	%{__enable_disable static_libs static} \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/grilo-0.2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/grilo-simple-playlist
%attr(755,root,root) %{_bindir}/grilo-test-ui-0.2
%attr(755,root,root) %{_bindir}/grl-inspect-0.2
%attr(755,root,root) %{_libdir}/libgrilo-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrilo-0.2.so.1
%attr(755,root,root) %{_libdir}/libgrlnet-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlnet-0.2.so.0
%dir %{_libdir}/grilo-0.2
%{_libdir}/girepository-1.0/Grl-0.2.typelib
%{_libdir}/girepository-1.0/GrlNet-0.2.typelib
%{_mandir}/man1/grl-inspect.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgrilo-0.2.so
%attr(755,root,root) %{_libdir}/libgrlnet-0.2.so
%{_includedir}/grilo-0.2
%{_pkgconfigdir}/grilo-0.2.pc
%{_pkgconfigdir}/grilo-net-0.2.pc
%{_datadir}/gir-1.0/Grl-0.2.gir
%{_datadir}/gir-1.0/GrlNet-0.2.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgrilo-0.2.a
%{_libdir}/libgrlnet-0.2.a
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
