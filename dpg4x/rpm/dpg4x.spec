Name: dpg4x
Version: 2.3
Release: 3%{?dist}
License: GPLv3
Summary: GUI to encode files into the DPG video format
Url: http://sourceforge.net/projects/dpg4x
Group: Applications/Multimedia

# Original SourceForge tar file
Source0: %{url}/files/%{name}_%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
BuildRequires: desktop-file-utils
# python-devel is more compatible with older distros like SLES10
BuildRequires: python-devel >= 2.4
Requires: python >= 2.4
Requires: wxPython >= 2.8
Requires: mplayer >= 1.0 
Requires: mencoder >= 1.0 
# Python Imaging Library (PIL) is better when creating DPG thumbnails
# not a mandatory dependency
Requires: python-imaging >= 1.0

%description
DPG for X allows the easy creation of DPG video files. A DPG video is
the video format that you need if you want to play movies on your
Nintendo DS.

Features:
 - Simple GUI suitable for beginners.
 - Includes lots of options for the advanced user.
 - Command line options to encode videos from batch jobs.
 - Supports individual per-media settings when needed.
 - Multiple DPG version support, from DPG0 to DPG4.
 - Can process any video file playable by mplayer.
 - Encodes your DVD and VCD directly.
 - Includes subtitles support.
 - Ability to preview the encoding settings.
 - Drag and drop support from your favorite file manager.
 - Batch processing.
 - Multiplatform.
 - Multilanguage.
 
# The sourceForge tar files has '_' instead of '-', require -n tag
%prep
%setup -q -n %{name}_%{version}
# distutils needs config file at top directory
cp pkg_common/setup.cfg .

%build
python pkg_common/setup.py build

%install
rm -rf %{buildroot}
# --prefix prevents SLES10 from placing files in /usr/local
python pkg_common/setup.py install -O1 --root=%{buildroot} --prefix=%{_prefix}

# man pages
mkdir -p %{buildroot}%{_mandir}/man1
cp -p pkg_common/dpg4x.1 %{buildroot}%{_mandir}/man1

# translations
mkdir -p %{buildroot}/usr/share/locale/es/LC_MESSAGES
cp -p i18n/es/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/es/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/ca/LC_MESSAGES
cp -p i18n/ca/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/ca/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/en/LC_MESSAGES
cp -p i18n/en/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/en/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/sv/LC_MESSAGES
cp -p i18n/sv/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/sv/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/fr/LC_MESSAGES
cp -p i18n/fr/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/fr/LC_MESSAGES

%find_lang %{name}

# desktop, menus and icons (--vendor is required by SLES10)
desktop-file-install                                \
--vendor=%{name}                                    \
--dir=%{buildroot}/%{_datadir}/applications         \
pkg_common/%{name}.desktop

mkdir -p %{buildroot}/usr/share/icons/hicolor/16x16/apps
ln -s  /usr/share/%{name}/icons/%{name}_16.png %{buildroot}/usr/share/icons/hicolor/16x16/apps/%{name}.png
mkdir -p %{buildroot}/usr/share/icons/hicolor/22x22/apps
ln -s  /usr/share/%{name}/icons/%{name}_22.png %{buildroot}/usr/share/icons/hicolor/22x22/apps/%{name}.png
mkdir -p %{buildroot}/usr/share/icons/hicolor/32x32/apps
ln -s  /usr/share/%{name}/icons/%{name}_32.png %{buildroot}/usr/share/icons/hicolor/32x32/apps/%{name}.png
mkdir -p %{buildroot}/usr/share/icons/hicolor/48x48/apps
ln -s  /usr/share/%{name}/icons/%{name}_48.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/%{name}.png
mkdir -p %{buildroot}/usr/share/icons/hicolor/64x64/apps
ln -s  /usr/share/%{name}/icons/%{name}_64.png %{buildroot}/usr/share/icons/hicolor/64x64/apps/%{name}.png

mkdir -p %{buildroot}/usr/share/pixmaps
ln -s  /usr/share/%{name}/icons/%{name}_32.png %{buildroot}/usr/share/pixmaps/%{name}.png
cp -a pkg_common/%{name}.xpm %{buildroot}/usr/share/pixmaps

# Set exec flag on files that can be run directly (those with shebangs)
chmod 755  %{buildroot}/usr/share/dpg4x/Dpg4x.py

# Make sure the icon cache is up to date
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING CREDITS INSTALL README ChangeLog
%{_bindir}/*
/usr/share/dpg4x/*
/usr/share/applications/*
/usr/share/icons/hicolor/*
/usr/share/pixmaps/*
%{_mandir}/man1/*

%changelog 
* Tue Aug 20 2013 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.3-3
— Updates for newer mplayer versions
* Thu Jul 25 2013 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.3-2
— Updates to Windows installer, increasing rpm release number to align
* Sun Sep 09 2012 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.3-1
— Updates for packaging dpg4x v2.3.
- Removed Dpg2Avi and DpgImginjector scripts, now included in dpg4x
- Added French translation
* Sat Aug 27 2011 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.2-1
— Updates for packaging dpg4x v2.2.
- Added dpgimginjector and PIL dependency 
- Minor updates to be rpmlint compliant (tested on Fedora 15)
* Fri Jan 14 2011 Marc Davignon <mpdavig@users.sourceforge.net> - 2.1-1
— Updates for packaging dpg4x v2.1.
- Added man page, python >= 2.4, and SLES10 support
* Sun Jan  9 2011 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.0-3
— Using pkg_resources/fedora, minor distutils improvements
* Sun Jan  2 2011 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.0-2
— Minor updates based on Debian package for dpg4x v2.0 (description, man pages, icon links)
* Sun Dec 12 2010 Tomas Aronsson <d0malaga@users.sourceforge.net> - 2.0-1
— Updates for packaging dpg4x v2.0 from SourceForge. Updated translation for Swedish
* Sun Sep  5 2010 Tomas Aronsson <d0malaga@users.sourceforge.net> - 1.2-1
— First version, packaging dpg4x v1.2 from SourceForge. Additional translation for Swedish
