#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	User interface builder for GTK+ and GNOME
Summary(pl.UTF-8):	Budowniczy interfejsów użytkownika dla GTK+ i GNOME
Name:		glade
Version:	3.38.2
Release:	2
License:	GPL v2+ and LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/glade/3.38/%{name}-%{version}.tar.xz
# Source0-md5:	f1ac9d9b6404308efb74adc548289455
URL:		https://glade.gnome.org/
BuildRequires:	gettext-devel >= 0.19.8
BuildRequires:	gjs-devel >= 1.64.0
BuildRequires:	glib2-devel >= 1:2.64.0
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	gtk+3-devel >= 3.24.0
BuildRequires:	gtk-doc >= 1.13
BuildRequires:	gtk-webkit4-devel >= 2.28
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2
BuildRequires:	python-pygobject3-devel >= 3.8.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gjs >= 1.64.0
Requires:	gtk-webkit4 >= 2.28
Requires:	hicolor-icon-theme
Conflicts:	glade3 < 3.8.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glade is a RAD tool to enable quick & easy development of user
interfaces for the GTK+ toolkit and the GNOME desktop environment.

The user interfaces designed in Glade are saved as XML, and by using
the GtkBuilder GTK+ object these can be loaded by applications
dynamically as needed.

By using GtkBuilder, Glade XML files can be used in numerous
programming languages including C, C++, C#, Vala, Java, Perl, Python
and others.

%description -l pl.UTF-8
Glade jest narzędziem typu RAD (Rapid Application Development) do
szybkiego i wygodnego tworzenia interfejsów użytkownika opartych o
bibliotekę GTK+ i środowisko GNOME.

Interfejsy użytkownika zaprojektowane w Glade są zapisywane w formacie
XML i poprzez użycie obiektu GtkBuilder, z biblioteki GTK+, mogą być
dynamicznie ładowane przez aplikacje.

Poprzez użycie GtkBuilder, pliki XML Glade mogą być używane w licznych
językach programowania, włączając C, C++, C#, Vala, Java, Perl, Python
i inne.

%package libs
Summary:	Glade library
Summary(pl.UTF-8):	Biblioteka Glade
Group:		X11/Libraries
Requires:	glib2 >= 1:2.64.0
Requires:	gtk+3 >= 3.24.0
Requires:	libxml2 >= 2.4.0

%description libs
Glade library.

%description libs -l pl.UTF-8
Biblioteka Glade.

%package devel
Summary:	Header files for Glade library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Glade
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.64.0
Requires:	gtk+3-devel >= 3.24.0
Requires:	libxml2-devel >= 2.4.0

%description devel
Header files for Glade library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Glade.

%package static
Summary:	Static Glade library
Summary(pl.UTF-8):	Statyczna biblioteka Glade
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Glade library.

%description static -l pl.UTF-8
Statyczna biblioteka Glade.

%package apidocs
Summary:	Glade API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Glade
Group:		Documentation
Requires:	gtk-doc-common
%{?noarchpackage}

%description apidocs
Glade API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Glade.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e '/^libgladeui = / s/shared_library/library/' gladeui/meson.build
%endif

%build
%meson build \
	-Dgladeui=true \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database_post

%postun
%update_icon_cache hicolor
%update_desktop_database_postun

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# NOTE: COPYING contains general notes; full GPL and LGPL texts are in COPYING.{GPL,LGPL}
%doc AUTHORS COPYING MAINTAINERS NEWS TODO
%attr(755,root,root) %{_bindir}/glade
%attr(755,root,root) %{_bindir}/glade-previewer
%dir %{_libdir}/glade
%dir %{_libdir}/glade/modules
%attr(755,root,root) %{_libdir}/glade/modules/libgladegjs.so
%attr(755,root,root) %{_libdir}/glade/modules/libgladeglade.so
%attr(755,root,root) %{_libdir}/glade/modules/libgladegtk.so
%attr(755,root,root) %{_libdir}/glade/modules/libgladepython.so
%attr(755,root,root) %{_libdir}/glade/modules/libgladewebkit2gtk.so
%{_datadir}/glade
%{_datadir}/gettext/its/glade-catalog.its
%{_datadir}/gettext/its/glade-catalog.loc
%{_desktopdir}/org.gnome.Glade.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Glade.svg
%{_iconsdir}/hicolor/symbolic/apps/glade-brand-symbolic.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Glade-symbolic.svg
%{_datadir}/metainfo/org.gnome.Glade.appdata.xml
%{_mandir}/man1/glade-previewer.1*
%{_mandir}/man1/glade.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgladeui-2.so.13
%{_libdir}/girepository-1.0/Gladeui-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-2.so
%{_datadir}/gir-1.0/Gladeui-2.0.gir
%{_includedir}/libgladeui-2.0
%{_pkgconfigdir}/gladeui-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgladeui-2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gladeui-2
%endif
