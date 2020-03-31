%define git 0
%define prerel 63ffd68
%define ver 0.10.0
%define gitday 20121312
%define _disable_ld_no_undefined 1


Summary:	Lightweight X11 desktop panel based on fbpanel
Name:		lxpanel
Release:	1
%if %git
Version:	%{ver}.git%{gitday}
Source0:	%{name}-%{prerel}.tar.gz
%else
Version:	%{ver}
Source0:	http://dfn.dl.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.xz
%endif
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://lxde.sourceforge.net/
#Source1:	volume_icon.tar.gz
Patch1:		configure_desktop_number.patch
Patch2:		lxpanel-0.5.12-automake113.patch
BuildRequires:	docbook-to-man
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libmenu-cache)
BuildRequires:	pkgconfig(libwnck-1.0)
Requires:	desktop-common-data
Requires:	obconf
Suggests:	pcmanfm
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
#/autogen.sh

%build
export CC=gcc
%configure2_5x \
	--enable-man \
	--with-plugins="cpu batt kbled xkb thermal deskno volumealsa"
%make

%install
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/lxpanelctl
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/batt.so
%{_libdir}/%{name}/plugins/cpu.so
%{_libdir}/%{name}/plugins/deskno.so
%{_libdir}/%{name}/plugins/kbled.so
%{_libdir}/%{name}/plugins/volumealsa.so
%{_libdir}/%{name}/plugins/xkb.so
%{_libdir}/%{name}/plugins/thermal.so
%{_datadir}/%{name}
%{_mandir}/man1/*

%files devel
%{_includedir}/lxpanel
%{_libdir}/pkgconfig/lxpanel.pc

