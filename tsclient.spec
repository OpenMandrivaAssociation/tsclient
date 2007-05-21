%define	version		0.148

Summary:  	Terminal Server Client is a frontend for rdesktop for the GNOME2 platform
Name:     	tsclient
Version:  	%{version}
Release:  	%mkrel 1
License: 	GPL
Group:		Networking/Remote access 
URL:		http://www.gnomepro.com/tsclient/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.132-translation.patch.bz2

Requires:	rdesktop >= 1.3
BuildRequires:	gnome-panel-devel
BuildRequires:	ImageMagick
BuildRequires:	gettext

%description
Terminal Server Client is a frontend for rdesktop for the GNOME2 platform.
Also support vnc.

%prep
%setup -q
#%patch0 -p1

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# icon
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -D -m 644       tsclient.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 tsclient.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 tsclient.png %{buildroot}%{_miconsdir}/%{name}.png

# menu
mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name}  <<EOF
?package(%name): \
 command="%{_bindir}/%{name}" \
 needs="X11" \
 section="Networking/Remote access" \
 title="Terminal Server Client" \
 longtitle="Frontend for rdesktop" \
 icon="%{name}.png" \
 xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applnk/Internet/
cat << EOF > %{buildroot}%{_datadir}/applnk/Internet/tsclient.desktop
[Desktop Entry]
Name=Terminal Server Client
Comment=Frontend for rdesktop
TryExec=%{name}
Exec=tsclient
Icon=%{name}.png
Terminal=0
Type=Application
EOF

%find_lang %name

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS NEWS
%{_bindir}/tsclient
%{_libdir}/bonobo/servers/*.server
%{_libexecdir}/tsclient-applet
%{_datadir}/application-registry/tsclient.applications
%{_datadir}/applications/tsclient.desktop
%{_datadir}/pixmaps/*
%{_datadir}/mime-info/*
%{_datadir}/applnk/Internet/tsclient.desktop
%{_mandir}/man1/*

%{_menudir}/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
