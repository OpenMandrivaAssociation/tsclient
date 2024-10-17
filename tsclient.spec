%define Werror_cflags %nil

Summary: Client for VNC and Windows Terminal Server
Name: tsclient
Version: 2.0.2
Release: 7
License: GPL+
Group: Networking/Remote access
URL: https://sourceforge.net/projects/tsclient
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
Patch9:	tsclient-2.0.2_glib_h.patch

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
%patch9 -p1 -b .glib_h

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


%changelog
* Sat Feb 25 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.0.2-6
+ Revision: 780704
- added p9 for glib.h only build error
- rebuild
- spec clean up

* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 2.0.2-5
+ Revision: 677910
- fix build
- fix build with latest libnotify
- rebuild to add gconftool as req

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-4mdv2011.0
+ Revision: 615274
- the mass rebuild of 2010.1 packages

* Wed Jan 13 2010 Götz Waschk <waschk@mandriva.org> 2.0.2-3mdv2010.1
+ Revision: 490761
- fix build deps
- update patch 6 for new networkmanager

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 2.0.2-2mdv2010.0
+ Revision: 445561
- rebuild

* Fri Mar 06 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.2-1mdv2009.1
+ Revision: 349749
- Fix RPM Group
- New upstream release
- New upstream release

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 0.150-5mdv2009.0
+ Revision: 261654
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.150-4mdv2009.0
+ Revision: 254784
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.150-2mdv2008.1
+ Revision: 171148
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- drop old menu

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Dec 18 2007 Jérôme Soyer <saispo@mandriva.org> 0.150-1mdv2008.1
+ Revision: 132081
- New release

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill explicit icon extension

* Mon May 21 2007 Antoine Ginies <aginies@mandriva.com> 0.148-1mdv2008.0
+ Revision: 29386
- Import tsclient



* Sun Jul 16 2006 Jerome Soyer <saispo@mandriva.org> 0.148-1mdv2007
- 0.148 release

* Mon Dec  5 2005 Antoine Ginies <aginies@mandriva.com> 0.140-1mdk
- 0.140 release

* Fri Mar 18 2005 Antoine Ginies <aginies@n1.mandrakesoft.com> 0.132-3mdk
- rebuild

* Thu Feb 19 2004 Abel Cheung <deaddog@deaddog.org> 0.132-2mdk
- Use ImageMagick to generate icons
- Patch0: Fix some b0rked translation files

* Mon Jan  5 2004 Antoine Ginies <aginies@mandrakesoft.com> 0.132-1mdk
- release 0.132

* Mon Aug 18 2003 Antoine Ginies <aginies@bi.mandrakesoft.com> 0.120-1mdk
- release 0.120

* Fri May 02 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.108-1mdk
- 0.108
- add all icons
- fix files list
 
* Fri Jan 10 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.86-3mdk
- transparent icon (padbol) 
* Tue Jan 07 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.86-2mdk
- correct icon path
* Fri Jan 03 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.86-1mdk
- new release 0.86
* Mon Nov 04 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.32-1mdk
- version 0.32
* Wed Oct 30 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.16-2mdk
- correct url tag
* Tue Oct 29 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.16-1mdk
- patch for -F rdesktop option
- first release for Mandrakesoft 
