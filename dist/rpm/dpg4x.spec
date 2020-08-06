Name: dpg4x
Version: 3.0
Release: 1%{?dist}
License: GPLv3
Summary: GUI to encode files into the DPG video format
Url: http://sourceforge.net/projects/dpg4x
Group: Applications/Multimedia

# Create this by setuptools:
# python setup.py sdist --formats=bztar
Source0: %{url}/files/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: python-devel >= 3.8
Requires: python >= 3.8
Requires: python3-wxpython4 >= 4.0
Requires: mplayer >= 1.4 
Requires: mencoder >= 1.4 
Requires: python3-pillow >= 7.0

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
 
%prep
%setup -q -n %{name}-%{version}

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

#mkdir -p %{buildroot}/usr/bin
#cp dist/pkg_common/dpg4x %{buildroot}/usr/bin
#mkdir -p %{buildroot}/usr/share/dpg4x/dpg4x
#cp dpg4x_main.py %{buildroot}/usr/share/dpg4x
#cp -r dpg4x %{buildroot}/usr/share/dpg4x

# man pages
mkdir -p %{buildroot}%{_mandir}/man1
cp -p dist/pkg_common/dpg4x.1 %{buildroot}%{_mandir}/man1

# translations
mkdir -p %{buildroot}/usr/share/locale/es/LC_MESSAGES
cp -p dpg4x/i18n/es/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/es/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/ca/LC_MESSAGES
cp -p dpg4x/i18n/ca/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/ca/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/en/LC_MESSAGES
cp -p dpg4x/i18n/en/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/en/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/sv/LC_MESSAGES
cp -p dpg4x/i18n/sv/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/sv/LC_MESSAGES

mkdir -p %{buildroot}/usr/share/locale/fr/LC_MESSAGES
cp -p dpg4x/i18n/fr/LC_MESSAGES/dpg4x.mo %{buildroot}/usr/share/locale/fr/LC_MESSAGES

%find_lang %{name}

# desktop, menus and icons (--vendor is required by SLES10)
desktop-file-install                                \
--vendor=%{name}                                    \
--dir=%{buildroot}/%{_datadir}/applications         \
dist/pkg_common/%{name}.desktop

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
cp -a dist/pkg_common/%{name}.xpm %{buildroot}/usr/share/pixmaps

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

#%files -f %{name}.lang
%files -f INSTALLED_FILES -f %{name}.lang
%defattr(-,root,root)
%doc LICENSE CREDITS INSTALL README ChangeLog
#%{_bindir}/*
#/usr/share/dpg4x/*
/usr/share/applications/*
/usr/share/icons/hicolor/*
/usr/share/pixmaps/*
%{_mandir}/man1/*

%changelog 
* Sun Aug 02 2020 Tomas Aronsson <d0malaga@users.sourceforge.net> - 3.0a1
— Rpm packaging using setuptools
* Sun Jun 21 2020 Tomas Aronsson <d0malaga@users.sourceforge.net> - 3.0a0
— Initial migration to Fedora 32
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
