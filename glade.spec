#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	User interface builder for GTK+ and GNOME
Summary(pl.UTF-8):	Budowniczy interfejsów użytkownika dla GTK+ i GNOME
Name:		glade
Version:	3.14.1
Release:	1
License:	GPL v2 and LGPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glade/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	e6a5f2cae2b3147669fbe5101dc70dbf
URL:		http://glade.gnome.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils >= 0.18.0
BuildRequires:	gobject-introspection-devel >= 0.10.1
BuildRequires:	gtk+3-devel >= 3.6.0
BuildRequires:	intltool >= 0.41.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.4.0
BuildRequires:	pkgconfig
BuildRequires:	python-pygobject3-devel >= 3.0.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	yelp-tools
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires:	%{name}-libs = %{version}-%{release}
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
Requires:	gtk+3 >= 3.6.0

%description libs
Glade library.

%description libs -l pl.UTF-8
Biblioteka Glade.

%package devel
Summary:	Header files for Glade library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Glade
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3-devel >= 3.6.0
Requires:	libxml2-devel >= 1:2.4.0

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

%description apidocs
Glade API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Glade.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/glade/modules/*.{a,la}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database_post

%postun
%update_icon_cache hicolor
%update_desktop_database_postun

%post libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/glade
%attr(755,root,root) %{_bindir}/glade-previewer
%dir %{_libdir}/glade
%dir %{_libdir}/glade/modules
%attr(755,root,root) %{_libdir}/glade/modules/libgladegtk.so
%attr(755,root,root) %{_libdir}/glade/modules/libgladepython.so
%{_datadir}/glade
%{_desktopdir}/glade.desktop
%{_iconsdir}/hicolor/*/*/*.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgladeui-2.so.4
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
