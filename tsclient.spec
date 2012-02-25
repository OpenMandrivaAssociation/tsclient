%define Werror_cflags %nil

Summary: Client for VNC and Windows Terminal Server
Name: tsclient
Version: 2.0.2
Release: 6
License: GPL+
Group: Networking/Remote access
URL: http://sourceforge.net/projects/tsclient
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# reported upstream
Patch0: icon-names.patch
# reported upstream
Patch2: edit-dialog-crash.patch
# reported upstream
Patch3: vnc-password-optional.patch
# reported upstream
Patch4: vnc-remote-screen-size.patch
# NOT reported upstream; there's no simple way to make it support both
# realvnc and tightvnc
Patch5: realvnc-args.patch
Patch6: tsclient-pkgconfig.patch
Patch7: tsclient-2.0.2-libnotify0.7.patch
Patch8: tsclient-2.0.2-link.patch

BuildRequires: desktop-file-utils
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: pkgconfig(gnome-desktop-2.0)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(libglade-2.0)
BuildRequires: pkgconfig(libgnomeui-2.0)
BuildRequires: pkgconfig(libnm-glib)
BuildRequires: pkgconfig(libnotify)
#BuildRequires: gnome-panel-devel

Requires: rdesktop
Requires: vnc

%description
tsclient is a frontend that makes it easy to use rdesktop and vncviewer.

%package devel
Summary: Header files needed to write tsclient plugins
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The tsclient-devel package contains header files that are needed to
develop tsclient plugins.

%prep
%setup -q
%patch0 -p1 -b .icon-names
%patch2 -p1 -b .edit-dialog-crash
%patch3 -p1 -b .vnc-password
%patch4 -p1 -b .vnc-remotesize
%patch5 -p1 -b .realvnc-args
%patch6 -p1 -b .libgnomeui
%patch7 -p0 -b .libnotify
%patch8 -p0 -b .link

%build
autoreconf -fi
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}/var/scrollkeeper

desktop-file-install \
	--vendor tsclient \
	--delete-original \
	--dir %{buildroot}%{_datadir}/applications \
	--remove-category Application \
	%{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}/usr/lib/tsclient/plugins/*.{a,la}

%find_lang %{name}

%preun
%preun_uninstall_gconf_schemas tsc-handlers

%files -f %{name}.lang
%doc COPYING AUTHORS
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/gconf/schemas/tsc-handlers.schemas
%{_libdir}/tsclient
%{_datadir}/gnome/autostart/tsc-autostart.desktop
%{_datadir}/icons/hicolor/scalable/apps/tsclient.svg
%{_datadir}/tsclient

%files devel
%{_includedir}/tsclient
