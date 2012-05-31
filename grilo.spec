#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Framework for access to sources of multimedia content
Name:		grilo
Version:	0.1.19
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo/0.1/%{name}-%{version}.tar.xz
# Source0-md5:	f387f1f7d20910d3cbaeb3f2819d7d6f
URL:		http://live.gnome.org/Grilo
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.22
BuildRequires:	gobject-introspection-devel >= 0.9
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libsoup-devel >= 2.33.4
BuildRequires:	libtool >= 2.2.6
BuildRequires:	libxml2-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.16.0
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
Requires:	glib2-devel >= 2.22
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
	%{__enable_disable static_libs static} \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/grilo-0.1

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
%attr(755,root,root) %{_bindir}/grilo-test-ui-0.1
%attr(755,root,root) %{_bindir}/grl-inspect-0.1
%attr(755,root,root) %ghost %{_libdir}/libgrilo-0.1.so.0
%attr(755,root,root) %{_libdir}/libgrilo-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgrlnet-0.1.so.0
%attr(755,root,root) %{_libdir}/libgrlnet-0.1.so.*.*.*
%dir %{_libdir}/grilo-0.1
%{_libdir}/girepository-1.0/Grl-0.1.typelib
%{_libdir}/girepository-1.0/GrlNet-0.1.typelib
%{_mandir}/man1/grl-inspect.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgrilo-0.1.so
%{_libdir}/libgrlnet-0.1.so
%{_includedir}/grilo-0.1
%{_pkgconfigdir}/grilo-0.1.pc
%{_pkgconfigdir}/grilo-net-0.1.pc
%{_datadir}/gir-1.0/Grl-0.1.gir
%{_datadir}/gir-1.0/GrlNet-0.1.gir
%{_datadir}/vala-0.16/vapi/grilo-0.1.deps
%{_datadir}/vala-0.16/vapi/grilo-0.1.vapi
%{_datadir}/vala-0.16/vapi/grilo-net-0.1.deps
%{_datadir}/vala-0.16/vapi/grilo-net-0.1.vapi

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgrilo-0.1.a
%{_libdir}/libgrlnet-0.1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/grilo
%endif
