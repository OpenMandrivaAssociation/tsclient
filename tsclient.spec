%define Werror_cflags %nil

Summary: Client for VNC and Windows Terminal Server
Name: tsclient
Version: 2.0.2
Release: %mkrel 3
URL: http://sourceforge.net/projects/tsclient
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

License: GPL+
Group: Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires: rdesktop
Requires: vnc

BuildRequires: gnome-desktop-devel
BuildRequires: libgnomeui2-devel
BuildRequires: libnotify-devel
BuildRequires: libnm-glib-devel
BuildRequires: gtk2-devel
BuildRequires: gnome-panel-devel
BuildRequires: desktop-file-utils
BuildRequires: libtool, intltool
BuildRequires: libglade2-devel

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
libtoolize --force --copy
autoreconf

%build

%configure2_5x
%make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

desktop-file-install --vendor tsclient --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications               \
  --remove-category Application                               \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

rm -rf $RPM_BUILD_ROOT/usr/lib/tsclient/plugins/*.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/tsc-handlers.schemas >& /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/tsc-handlers.schemas >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/tsc-handlers.schemas >& /dev/null || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi


%files -f %{name}.lang
%defattr(-,root,root)
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
