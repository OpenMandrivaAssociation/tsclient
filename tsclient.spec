%define Werror_cflags %nil
%define	version		2.0.1

Summary:  	Frontend for rdesktop for the GNOME2 platform
Name:     	tsclient
Version:  	%{version}
Release:  	%mkrel 1
License: 	GPL
Group:		Networking/Remote access
URL:		http://www.gnomepro.com/tsclient/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		%{name}-%{version}.tar.bz2
# reported upstream
Patch0: icon-names.patch
# reported upstream
Patch1: launch-args.patch
# reported upstream
Patch2: edit-dialog-crash.patch
# reported upstream
Patch3: vnc-password-optional.patch
# reported upstream
Patch4: vnc-remote-screen-size.patch
# NOT reported upstream; there's no simple way to make it support both
# realvnc and tightvnc
Patch5: realvnc-args.patch
Patch6: tsclient-libgnomeui.patch

Requires:	rdesktop >= 1.3
BuildRequires:	gnome-panel-devel gnomeui2-devel
BuildRequires:	imagemagick
BuildRequires:	gettext

%description
Terminal Server Client is a frontend for rdesktop for the GNOME2 platform.
Also support vnc.

%prep
%setup -q
%patch0 -p1 -b .icon-names
%patch1 -p1 -b .launch-args
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
rm -rf %{buildroot}
%makeinstall_std

# menu

mkdir -p %{buildroot}%{_datadir}/applnk/Internet/
cat << EOF > %{buildroot}%{_datadir}/applnk/Internet/tsclient.desktop
[Desktop Entry]
Name=Terminal Server Client
Comment=Frontend for rdesktop
TryExec=%{name}
Exec=tsclient
Icon=%{name}
Terminal=0
Type=Application
EOF

%find_lang %name

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING AUTHORS
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/gconf/schemas/tsc-handlers.schemas
%{_libdir}/tsclient
%{_datadir}/gnome/autostart/tsc-autostart.desktop
%{_datadir}/icons/hicolor/scalable/apps/tsclient.svg
%{_datadir}/tsclient
%{_includedir}/tsclient/*
%{_datadir}/applnk/Internet/tsclient.desktop

