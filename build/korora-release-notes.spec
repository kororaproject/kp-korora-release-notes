# Documentation Specfile

Name:      korora-release-notes
Version:   18.0
Release:   1%{?dist}
Summary:   Release Notes
URL:       http://kororaproject.org
Group:     System Environment/Base
License:   CC-BY-SA
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires:	coreutils
Requires(post):	/bin/touch
Obsoletes:	fedora-release-notes
Provides:	fedora-release-notes

%description
These are the official Release Notes for Fedora 17,
written and edited by the Fedora community. For more
information on the Release Notes process or how you can
contribute, refer to the Release Notes HOWTO located at
http://fedoraproject.org/wiki/Docs/Beats/HowTo.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/%{name}
ln -sf %{_defaultdocdir}/HTML/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/fedora-release-notes
#
# Loop through the languages
#
cat /dev/null > html.lang
for LANGDIR in document/* ; do
  #
  # First, the html in /usr/share/doc/HTML, then descend
  # through any subdirectories, installing everything found.
  #
  # Language to process
  LANG=${LANGDIR#document/}
  # Target for the html
  NOTETARG=$RPM_BUILD_ROOT%{_defaultdocdir}/HTML/%{name}/${LANG}
  # Place where html files are
  SRCBASE=${LANGDIR}
  mkdir -p ${NOTETARG}
  mkdir -p ${NOTETARG}/Common_Content
  mkdir -p ${NOTETARG}/Common_Content/images
  install -m 644 ${SRCBASE}/Common_Content/images/*.png \
    ${NOTETARG}/Common_Content/images/
  install -m 644 ${SRCBASE}/Common_Content/images/*.svg \
    ${NOTETARG}/Common_Content/images/
  echo  "${NOTETARG}/" >> html.lang
  mkdir -p ${NOTETARG}/Common_Content/css
  install -m 644 ${SRCBASE}/Common_Content/css/*.css \
    ${NOTETARG}/Common_Content/css/
  echo  "${NOTETARG}/" >> html.lang
  echo  "${NOTETARG}/" >> html.lang
  install -m 644 ${SRCBASE}/*.html ${NOTETARG}/
  echo  "${NOTETARG}/" >> html.lang
done
#
# index.html
#
install -m 644 index.html $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/%{name}
#
# Now the desktop files
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/kde4
SRCBASE=desktop
install -m 644 ${SRCBASE}/fedora-release-notes.desktop \
    $RPM_BUILD_ROOT%{_datadir}/applications
install -m 644 ${SRCBASE}/fedora-release-notesX.desktop \
    $RPM_BUILD_ROOT%{_datadir}/applications
install -m 644 ${SRCBASE}/fedora-release-notes.KDE.desktop \
    $RPM_BUILD_ROOT%{_datadir}/applications/kde4/fedora-release-notes.desktop

#%find_lang %{name} --with-gnome --all-name
#for F in $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/index-*.html ; do
#  L=`echo ${F} | %{__sed} 's/.*\/index-\(.*\)\.html$/\1/'`
#  echo "%%lang(${L}) ${F#$RPM_BUILD_ROOT}" >> html.lang
#done
cat html.lang >> %{name}.lang

#
# Icons
#
ICONDIR="$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/"
for SZ in icons/* ; do
  SZA=${SZ#icons/}
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${SZA}/apps 
  if [ "${SZA}" == "scalable" ] ; then :
    install -m 644 ${SZ}/apps/fedora-documentation.svg \
      ${ICONDIR}/${SZA}/apps/fedora-release-notes.svg 
  else
    install -m 644 ${SZ}/apps/fedora-documentation.png \
      ${ICONDIR}/${SZA}/apps/fedora-release-notes.png 
  fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML
%{_datadir}/applications/fedora-release-notes.desktop
%{_datadir}/applications/fedora-release-notesX.desktop
%{_datadir}/applications/kde4/fedora-release-notes.desktop
%{_datadir}/icons/hicolor/16x16/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/22x22/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/24x24/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/32x32/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/36x36/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/48x48/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/64x64/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/72x72/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/96x96/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/128x128/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/192x192/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/256x256/apps/fedora-release-notes.png
%{_datadir}/icons/hicolor/scalable/apps/fedora-release-notes.svg

# CAUTION: This file was created by doc-publican-rpm.  Changes made
# to this file, other than the changelog and the description, will
# be overwritten.  Make permanent changes to the docs/tools.git repo

%changelog
* Sun May 20 2012 Chris Smart <chris@kororaa.org> - 17.0.0-1
 - Updated for Kororaa 17 release.

* Thu Nov 10 2011 Chris Smart <chris@kororaa.org> - 16.1.0-1
 - Updated for Kororaa 16 release.

* Sun Sep 04 2011 Chris Smart <chris@kororaa.org> - 15.1.0-2
 - Create link to fedora-release-notes, so we don't have to change .desktop file.
 - Add provides fedora-release-notes.

* Fri Jun  3 2011 John J. McDonough <jjmcd@fedoraproject.org> - 15.1.0-1
 - Typo in Virtualization (BZ#705928)
 - gnuplot not GNU plot (BZ#707318)
 - device naming (BZ#707730)
 - Correct version number of boost (BZ#707786)
 - Remove reference to disappeared GS-Theme-Selector (BZ#708085)

* Tue May 10 2011 John J. McDonough <jjmcd@fedoraproject.org> - 15.0.0-1
- Updated doc-publican-rpm (icons named to match package)
- BZ#680165, BZ#699770, BZ#701638, BZ#701780, BZ#702669

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 14.98.0-2
- Update icon cache and desktop database scriptlets

* Fri Apr  7 2011 John J. McDonough <jjmcd@fedoraproject.org> - 14.98.0-1
- Remove dom0, dnssec, riak dropped from features
- Add description of IcedTea
- Admonitions in GNOME

* Fri Apr  7 2011 Zachary. M Oglesby <oglesbyzm@gmail.com> - 14.96.1-2
- Fixed spec file

* Thu Apr  7 2011 John J. McDonough <jjmcd@fedoraproject.org> - 14.96.0-1
- Point Kernel to kernelnewbies (Kernel)
- Point features to F15 instead of general feature page (Overview)
- Correct boxgrinder URL (Virtualization)
- Correct Python URL (Developer Tools)
- Correct Rails URL (Developer Tools)
- Correct avr-gcc URL (Embedded Development)
- Correct avr-c++ URL (Embedded Development)
- Correct avr-binutils URL (Embedded Development)
- Correct dfu-programmer URL (Embedded Development)
- Correct xlog URL (Amateur radio)
- Correct splat URL (Amateur radio)
- Remove redundant systemd and add administrative user per Rahul

* Thu Apr  7 2011 John J. McDonough <jjmcd@fedoraproject.org> - 14.95.2-1
- Separate .desktop files for GNOME and XFCE/LXDE

* Tue Apr  5 2011 John J. McDonough <jjmcd@fedoraproject.org> - 14.95.1-1
- Additional icon sizes (including scalable) BZ#694371

* Tue Apr  5 2011 John J. McDonough <jjmcd@fedoraproject.org> - 14.95.0-1
- Notes for Fedora 15 Beta

* Tue Feb 15 2011 Tom Callaway <spot@fedoraproject.org> - 14.1.2-3
- fix noise during post by adding Requires(post) for touch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov  9 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.1.2-1
- Additional languages
- BZ#649122

* Tue Nov  2 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.1.1-1
- Remove javascript from htmls

* Mon Nov  1 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.1.0-1
- Zero day updates
- BZ#641421
- Remove systemd references

* Mon Oct 18 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.0.3-1
- Add French, Swedish, Catalan

* Sun Oct 17 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.0.2-1
- Updates to Russian, Ukranian, Dutch

* Sun Oct 17 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.0.1-2
- Correct problem with icons

* Sun Oct 17 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.0.1-1
- Correct problem in Russian translation

* Sat Oct 16 2010 John J. McDonough <jjmcd@fedoraproject.org> - 14.0.0-1
- Update for F14 release

* Mon Sep 13 2010 John J. McDonough <jjmcd@fedoraproject.org> - 13.95.0-4
- Correct description in specfile
- Corrects BZ#632819

* Mon Sep 13 2010 John J. McDonough <jjmcd@fedoraproject.org> - 13.95.0-3
- Release Notes for Beta

* Tue May 11 2010 John J. McDonough <jjmcd@fedoraproject.org> - 13-5
- Add Russian translation

* Mon May 10 2010 John J. McDonough <jjmcd@fedoraproject.org> - 13-4
- Zero day updates:
- Configuration change in varnish, BZ#588953 
- Incorrect link in kernel BZ#590492

* Mon May 3 2010 Paul W. Frields <stickster@gmail.com> - 13-3
- Include ToC in document

* Mon May 3 2010 Paul W. Frields <stickster@gmail.com> - 13-2
- Remove unnecessary desktop file validation

* Mon May 3 2010 Paul W. Frields <stickster@gmail.com> - 13-1
- Update for F13 GA release
- Add icons for hicolor theme per XDG

* Sun May 2 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.97.0-9
- Test build prior to GA rpm

* Sat May 1 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.97.0-8
- Change KDE desktop file BZ#482947

* Tue Apr 27 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.97.0-7
- Write to html.lang

* Mon Apr 5 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.95-4
- Remove dependency on htmlview for non-desktop installs

* Wed Mar 24 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.95-3
- Correct license, requires

* Wed Mar 24 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.95-2
- Build for Beta

* Wed Mar 24 2010 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.95-1
- Test Build

* Tue Nov 9 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.2-1
- Correct issue with about-fedora omf files

* Tue Nov 9 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.1-1
- Zero day updates

* Tue Nov 2 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.0-4
- Eliminate publican during the build due to 0.44 => 1.0 probs

* Tue Nov 2 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.0-3
- requires publican publican-fedora

* Tue Nov 2 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.0-2
- Touch up .omf files for about-fedora

* Mon Nov 2 2009 John J. McDonough <jjmcd@fedoraproject.org> - 12.0.0-1
- Fedora 12 notes
- Compared to Fedora 11, many documents and formats omitted
- Only xml provided and then only for f-r-n and about-fedora.

* Fri May 29 2009 John J. McDonough <jjmcd@fedoraproject.org> - 11.0.1-2
- More translations, bump release

* Thu May 28 2009 John J. McDonough <jjmcd@fedoraproject.org> - 11.0.1-1
- Updated english in release-notes, bump version

* Wed May 13 2009 Paul W. Frields <stickster@gmail.com> - 11.0.0-2
- Fix homepage content

* Thu May 7 2009 John J. McDonough <jjmcd@fedoraproject.org> - 11.0.0-1
- Update for Fedora 11 release candidate

* Tue Apr 14 2009 John J. McDonough <jjmcd@fedoraproject.org> - 10.93.0-1
- Use publican for F11 Preview release

* Sun Nov 16 2008 Paul W. Frields <stickster@gmail.com> - 10.0.0-1
- Updates for F10 GA release

* Fri Nov 7 2008 Paul W. Frields <stickster@gmail.com> - 10.0.0-0.2
- Snapshot package for updated fedora-release compatibility

* Thu Oct 30 2008 Paul W. Frields <stickster@gmail.com> - 9.92-4
- Fix URI in Release Notes OMF file (#469179)

* Tue Oct 28 2008 Paul W. Frields <stickster@gmail.com> - 9.92-3
- Correct file names for Fedora 10 Preview Release

* Fri Oct 17 2008 Paul W. Frields <stickster@gmail.com> - 9.92-2
- Update version for Fedora 10 Preview Release

* Thu Oct 2 2008 Paul W. Frields <stickster@gmail.com> - 9.92-1
- Bump version and release to match for F10 Preview Release
- Fix description
- Fix missing README content

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 8.92-2
- Provides: system-release-notes

* Sat Jul 19 2008 Paul W. Frields <stickster@gmail.com> - 9.0.2-1
- Content and translation updates
- Fix description (#453255)

* Mon May 12 2008 Paul W. Frields <stickster@gmail.com> - 9.0.1-1
- Update with various bugfixes and translation updates

* Wed Apr 16 2008 Paul W. Frields <stickster@gmail.com> - 9.0.0-1
- Update for Fedora 9 final release

* Thu Mar 20 2008 Paul W. Frields <stickster@gmail.com> - 8.92-1
- Bump version for Fedora 9 Preview Release

* Wed Nov 7 2007 Paul W. Frields <stickster@gmail.com> - 8.90-1
- Update for F-9 development branch

* Wed Nov 7 2007 Paul W. Frields <stickster@gmail.com> - 8.0.1-1
- Update with various bugfixes and translation updates

* Tue Oct 30 2007 Paul W. Frields <stickster@gmail.com> - 8.0.0-3
- Fix release number in description

* Wed Oct 24 2007 Paul W. Frields <stickster@gmail.com> - 8.0.0-2
- Fix leftover draft notice on local startpage copy (#350801)

* Mon Oct 22 2007 Paul W. Frields <stickster@gmail.com> - 8.0.0-1
- Update for final release

* Wed Sep 26 2007 Bill Nottingham <notting@redhat.com> - 7.92-2
- fix symlinking (#306781)
- set license tag -> Open Publication

* Sun Sep 16 2007 Paul W. Frields <stickster@gmail.com> - 7.92-1
- Include new start page
- Push new content for F8 test3

* Wed Sep 12 2007 Paul W. Frields <stickster@gmail.com> - 7.91-1
- Link stylesheet resources to save space

* Mon Aug 27 2007 Paul W. Frields <stickster@gmail.com> - 7.90-2
- Remove superfluous PNG files
- Bump release for rebranding change in homepage

* Tue Aug 21 2007 Paul W. Frields <stickster@gmail.com> - 7.90-1
- Resituate HTML documentation for release spins

* Thu May 10 2007 Paul W. Frields <stickster@gmail.com> - 7.0.0-1
- Fix fedora-release-notes to use yelp ghelp facility
- Fix post script to properly update scrollkeeper
- Build for F7

* Fri Apr 27 2007 Paul W. Frields <stickster@gmail.com> - 6.93-3
- Relocate about-fedora and use yelp's ghelp: facility (#208220)
- Fix distro name in OMF and document metadata

* Mon Apr 23 2007 Jesse Keating <jkeating@redhat.com> - 6.93-2
- Updated translations and bits from wiki

* Sun Apr 15 2007 Paul W. Frields <stickster@gmail.com> - 6.93-1
- Update for Fedora 7 test4

* Fri Mar 23 2007 Paul W. Frields <stickster@gmail.com> - 6.92-5
- Bump release to include fixes in homepage module

* Fri Mar 23 2007 Paul W. Frields <stickster@gmail.com> - 6.92-4
- Add temporary community help notice to Release Notes for F7 test3

* Thu Mar 22 2007 Paul W. Frields <stickster@gmail.com> - 6.92-3
- Bump release for rebuild

* Thu Mar 22 2007 Paul W. Frields <stickster@gmail.com> - 6.92-2
- Use content from all supplemental modules in Docs CVS

* Mon Mar 19 2007 Paul W. Frields <stickster@gmail.com> - 6.92-1
- Update for Fedora 7 test3

* Sat Jan 27 2007 Paul W. Frields <stickster@gmail.com> - 6.91-1
- Update for Fedora 7 test2

* Sun Oct 15 2006 Paul W. Frields <stickster@gmail.com> - 6-3
- Fix IG publication URL
- Amend CSS to respect font selections and restore icons

* Sun Oct 8 2006 Paul W. Frields <stickster@gmail.com> - 6-2
- Localize About Fedora menu item (somewhat)

* Thu Oct 05 2006 Jesse Keating <jkeating@redhat.com> - 6-1
- Build for FC6, lots of new translations

* Sat Sep 30 2006 Paul W. Frields <stickster@gmail.com> - 5.92-7
- Include new i18n browser home page

* Mon Sep 25 2006 Jesse Keating <jkeating@redhat.com> - 5.92-6
- Bump for lang fixes

* Tue Sep 12 2006 Paul W. Frields <stickster@gmail.com> - 5.92-5
- Update scrollkeeper data for about-fedora

* Mon Sep 11 2006 Paul W. Frields <stickster@gmail.com> - 5.92-4
- Update about-fedora

* Wed Sep 6 2006 Paul W. Frields <stickster@gmail.com> - 5.92-3
- Make sure we package README-BURNING-ISOS files

* Tue Sep 5 2006 Jesse Keating <jkeating@redhat.com> - 5.92-1
- Bump for 5.92

* Fri Sep 1 2006 Paul W. Frields <stickster@gmail.com> - 5.91-8
- Handle i18n OMF files

* Sat Aug 26 2006 Paul W. Frields <stickster@gmail.com> - 5.91-7
- Add README-BURNING-ISOS.txt for inclusion in mirrors
- Put About document in proper directory

* Wed Aug 2 2006 Jesse Keating <jkeating@redhat.com> - 5.91-6
- bump

* Wed Aug 2 2006 Paul W. Frields <stickster@gmail.com> - 5.91-5
- Add README-Accessibility (moved from fedora-release)

* Wed Jul 26 2006 Paul W. Frields <stickster@gmail.com> - 5.91-4
- Process paths correctly (#200266)
- Package standalone HTML

* Sun Jul 23 2006 Jesse Keating <jkeating@redhat.com> - 5.91-3
- Only use tabs
- Version the indexhtml provides/obsoletes
- Cleanup post and postun scriptlets
- Don't require fedora-release, fedora-release requires us.
- Add a URL tag

* Sun Jul 16 2006 Paul W. Frields <stickster@gmail.com> - 5.91-1
- Initial release for Fedora Core 6 test2.
