%define git 0
%define prerel 63ffd68
%define gitday 20121312
%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %name %major

Summary:	Lightweight X11 desktop panel based on fbpanel
Name:		lxpanel
Release:	1
Version:	0.10.1
Source0:	http://downloads.sourceforge.net/lxde/lxpanel-%{version}.tar.xz
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://lxde.sourceforge.net/


BuildRequires:	docbook-to-man
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libfm-gtk3)
BuildRequires:  pkgconfig(libfm-extra)
BuildRequires:	pkgconfig(libmenu-cache)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:  pkgconfig(keybinder-3.0)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	libiw-devel

Requires:	desktop-common-data
Requires:	obconf
Requires:	libnotify
Recommends:	pcmanfm
Conflicts:	lxpanelx

%description
LXPanel is a lightweight X11 desktop panel contains:
1. User-friendly application menu automatically generated from *.desktop
   files on the system.
2. Launcher bar (Small icons clicked to launch apps)
3. Task bar supporting urgency hint (Can flash when gaim gets new
   incoming messages)
4. Notification area (System tray)
5. Digital clock
6. Run dialog (A dialog let you type a command and run, can be called in
   external programs)
7. Volume control plug-in (optional, written by jserv)
8. lxpanelctl, an external controller let you control lxpanel in other
   programs.

This version based on lxpanelx 0.6.0 alpha version

%package -n %libname
Summary:	Lxpanel library package
Group:		Graphical desktop/Other
Requires:	%{name} = %{version}

%description -n %libname
Library for access to the API.

%package devel
Summary:	Development files for lxpanel
Group:		Graphical desktop/Other

%description devel
This package contains development files needed for building lxde plugins.

%prep
%if %git
%setup -qn %{name}-%{prerel} -a1
%else
%setup -q
%endif
%autopatch -p1

%build

# Disable pager plugin as it breaks panel layout with GTK+ 3
# https://sourceforge.net/p/lxde/bugs/773/
sed -i '/pager.c/d' plugins/Makefile.am
sed -i '/STATIC_PAGER/d' src/private.h
sed -i 's/libwnck-3.0//' configure.ac

%configure \
	--enable-man \
	--enable-indicator-support \
	--enable-gtk3 \
	--with-plugins="cpu batt kbled xkb thermal deskno volumealsa"
%make_build

%install
%make_install

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/lxpanelctl
%dir %{_sysconfdir}/xdg/%{name}/
%{_sysconfdir}/xdg/%{name}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/batt.so
%{_libdir}/%{name}/plugins/cpu.so
%{_libdir}/%{name}/plugins/deskno.so
%{_libdir}/%{name}/plugins/kbled.so
%{_libdir}/%{name}/plugins/xkb.so
%{_libdir}/%{name}/plugins/thermal.so
%{_libdir}/%{name}/plugins/volume.so
%{_datadir}/%{name}
%{_mandir}/man1/*

%files -n %libname
%{_libdir}/%{name}/lib%{name}.so.%{major}{,.*}

%files devel
%{_includedir}/lxpanel
%{_libdir}/%{name}/lib%{name}.so
%{_libdir}/pkgconfig/lxpanel.pc
