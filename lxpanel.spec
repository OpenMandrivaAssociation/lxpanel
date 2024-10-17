# Workaround for Clang 16
%global optflags %{optflags} -Wno-incompatible-function-pointer-types
# Workaround for Clang 15+
%global optflags %{optflags} -Wno-error -Wno-implicit-function-declaration

# git snapshot
%global snapshot 1
%if 0%{?snapshot}
	%global commit		633a2d46ffd37f3acde539de9a2861d1ade49ef8
	%global commitdate	20230918
	%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

#define git 0
#define prerel 63ffd68
#define gitday 20121312
#define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %name
%define oldlibname %mklibname %name 0

Summary:	Lightweight X11 desktop panel based on fbpanel
Name:		lxpanel
Version:	0.10.1
Release:	3
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		https://www.lxde.org
# Use active maintained fork
#Source0:	https://github.com/lxde-continued/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
#Source0:	http://downloads.sourceforge.net/lxde/lxpanel-%{version}.tar.xz
Source0:	https://github.com/lxde/lxpanel/archive/%{?snapshot:%{commit}}%{!?snapshot:%{version}}/%{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}.tar.gz
# https://sourceforge.net/p/lxde/bugs/773/
Patch0:		0001-Specify-GTK_REQUEST_CONSTANT_SIZE.-Fixes-773.patch
#  resized panel background to enable larger panel heights #65
Patch1:		https://github.com/lxde/lxpanel/pull/65/commits/4f3d32e66135f733450ed0717cf4e96018046216.patch
# (fedora)
Patch3:	lxpanel-0.10.1-0003-volumealsa-poll-alsa-mixer-several-times-at-startup.patch
Patch4:	lxpanel-0.8.1-Fix-pager-scroll.patch
Patch5:	lxpanel-0.10.1-batt-chaging-pending.patch
# some plugins can't be compiled:
#  netstat, indicator
Patch10:	lxpanel-0.10.1-remove_failing_plugins.patch
# from lxde-continued
#  highlight selected workspace in pager
Patch101:	https://github.com/lxde/lxpanel/commit/359ac141643ca9072bdc66542902a529316f3b10.patch
#  apply partial workaround for GTK3 tooltip positioning bug (MAGEIA#30574)
Patch102:	https://github.com/lxde/lxpanel/commit/76d0d61194a3dec9f3cc9947933d2594366c439b.patch
#  merge pull request #3 from nsalguero/master
Patch103:	https://github.com/lxde/lxpanel/commit/0c44a8acd3cd497e61a4fdadace4b69c49185b57.patch

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
BuildRequires:	pkgconfig(libfm-gtk3)
BuildRequires:	pkgconfig(libfm-extra)
BuildRequires:	pkgconfig(libmenu-cache)
#BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(keybinder-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xkbfile)
#BuildRequires:	libiw-devel

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

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/lxpanelctl
%dir %{_sysconfdir}/xdg/%{name}/
%{_sysconfdir}/xdg/%{name}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/batt.so
%{_libdir}/%{name}/plugins/cpu.so
%{_libdir}/%{name}/plugins/cpufreq.so
%{_libdir}/%{name}/plugins/deskno.so
%{_libdir}/%{name}/plugins/kbled.so
%{_libdir}/%{name}/plugins/monitors.so
%{_libdir}/%{name}/plugins/netstatus.so
%{_libdir}/%{name}/plugins/thermal.so
%{_libdir}/%{name}/plugins/volume.so
%{_libdir}/%{name}/plugins/weather.so
%{_libdir}/%{name}/plugins/xkb.so
%{_datadir}/%{name}
%{_mandir}/man1/*

#---------------------------------------------------------------------------

%package -n %libname
Summary:	Lxpanel library package
Group:		Graphical desktop/Other
Requires:	%{name} = %{version}
Obsoletes:	%oldlibname < %{EVRD}

%description -n %libname
Library for access to the API.

%files -n %libname
%{_libdir}/%{name}/lib%{name}.so.%{major}{,.*}

#---------------------------------------------------------------------------

%package devel
Summary:	Development files for lxpanel
Group:		Graphical desktop/Other

%description devel
This package contains development files needed for building lxde plugins.

%files devel
%{_includedir}/lxpanel
%{_libdir}/%{name}/lib%{name}.so
%{_libdir}/pkgconfig/lxpanel.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}

%build
autoreconf -fiv
%configure \
	--disable-indicator-support \
	--enable-gtk3 \
	%{nil}
%make_build

%install
%make_install

# locales
%find_lang %{name}

