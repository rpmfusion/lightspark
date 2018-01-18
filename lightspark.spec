%define debug 0

%define git 0

%if %{git}
%define git_snapshot 1
%endif

%define pre_release 0

%if %{?git}
%define commit 7dd881170a1ed48596c19bac48cdcdd403f70841
%define date 20170422
%endif

%if %{pre_release}
%define pre rc1
%endif

%define rel 2

%define major 0.8.0

Name:           lightspark
Version:        %{major}
Release:        %{?pre:0.}%{rel}%{?git_snapshot:.%{date}git}%{?pre:.%{pre}}%{?dist}.1
Summary:        An alternative Flash Player implementation
License:        LGPLv3+
URL:            http://lightspark.github.io/
%if %{git}
Source0:        https://github.com/lightspark/lightspark/archive/%{commit}.tar.gz#/%{name}-%{version}-%{date}git.tar.gz
%else
Source0:        https://github.com/lightspark/lightspark/archive/%{name}-%{version}.tar.gz
%endif

Patch0:         lightspark-0.7.2-fix_ffmpeg_include_dir.patch

# Build fails on ppc64 and ppc64le, temporarily disable them
# https://github.com/lightspark/lightspark/issues/283
ExcludeArch:    ppc64 ppc64le

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  glew-devel >= 1.5.4
BuildRequires:  glibmm24-devel
BuildRequires:  gtkglext-devel
BuildRequires:  libcurl-devel
BuildRequires:  libffi-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  librtmp-devel
BuildRequires:  llvm-devel >= 2.7
BuildRequires:  nasm
BuildRequires:  ncurses-devel
BuildRequires:  pcre-devel
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_mixer-devel
BuildRequires:  xz-devel


%description
Lightspark is a modern, free, open-source flash player implementation.
Lightspark features:

* JIT compilation of Actionscript to native x86 byte code using LLVM
* Hardware accelerated rendering using OpenGL Shaders (GLSL)
* Very good and robust support for current-generation Actionscript 3
* A new, clean, code base exploiting Multi-Threading and optimized for
modern hardware. Designed from scratch after the official Flash
documentation was released.


%package mozilla-plugin
Summary:       Mozilla compatible plugin for %{name}
Requires:      mozilla-filesystem
Requires:      %{name} = %{version}-%{release}

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}. It can fallback to
gnash for unsupported SWF files ( AS2/avm1 ); to enable this feature
install gnash ( without gnash-plugin ).


%package chromium-plugin
Summary:       Chromium compatible plugin for %{name}
Requires:      chromium
Requires:      %{name} = %{version}-%{release}

%description chromium-plugin
This is the Chromium compatible plugin for %{name}.


%prep
%if %{git}
%setup -q -n %{name}-%{commit}
%else
%setup -q -n %{name}-%{name}-%{version}
%endif
%patch0 -p1 -b .ffmpeg-include-dir


%build
%cmake -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins" \
       -DPPAPI_PLUGIN_DIRECTORY="%{_libdir}/chromium-browser/PepperFlash/" \
%if %{debug}
       -DCMAKE_BUILD_TYPE=Debug \
%else
       -DCMAKE_BUILD_TYPE=Release \
%endif
       .

%make_build VERBOSE=1


%install
%make_install
%find_lang %{name}

pushd $RPM_BUILD_ROOT%{_datadir}/man/man1
    ln -s %{name}.1.gz tightspark.1.gz
popd

#remove devel file from package
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%license COPYING COPYING.LESSER
%doc ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/lightspark.conf
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/man/man1/%{name}.1.*
%{_datadir}/man/man1/tightspark.1.*
%{_libdir}/%{name}/

%files mozilla-plugin
%license COPYING COPYING.LESSER
%{_libdir}/mozilla/plugins/lib%{name}plugin.so

%files chromium-plugin
%license COPYING COPYING.LESSER
%{_libdir}/chromium-browser/PepperFlash/libpepflashplayer.so
%{_libdir}/chromium-browser/PepperFlash/manifest.json


%changelog
* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.8.0-2.1
- Rebuilt for ffmpeg-3.5 git

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.8.0-2
- Rebuild for ffmpeg update

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 26 2017 Xavier Bachelot <xavier@bachelot.org> - 0.8.0-1
- Update to 0.8.0.
- Add chromium plugin sub-package.
- Clean up BR:s.
- Clean up build options.

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.7.2-13.20170422git.1
- Rebuild for ffmpeg update

* Sun Apr 23 2017 Xavier Bachelot <xavier@bachelot.org> - 0.7.2-13.20170422git
- New snapshot with LLVM 4.0 support.

* Tue Apr 04 2017 Xavier Bachelot <xavier@bachelot.org> - 0.7.2-12.20170107git
- Disable ppc64le and ppc64.

* Thu Mar 23 2017 Xavier Bachelot <xavier@bachelot.org> - 0.7.2-11.20170107git
- New snapshot.
- Specfile cleanup.

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.7.2-10.20160703git.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.7.2-10.20160703git.4
- Rebuilt for ffmpeg-3.1.1

* Sat Jul 09 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.7.2-10.20160703git.3
- Update to latest git

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.7.2-10.20140219git.2
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-10.20140219git.1
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.7.2-9.20140219git.1
- Rebuilt for ffmpeg-2.3

* Sun Aug 03 2014 Sérgio Basto <sergio@serjux.com> - 0.7.2-9.20140219git
- Rebuilt for boost-1.55

* Tue Mar 25 2014 Xavier Bachelot <xavier@bachelot.org> 0.7.2-8.20130827git
- Rebuild for ffmpeg 2.2.

* Tue Mar 11 2014 Xavier Bachelot <xavier@bachelot.org> 0.7.2-7.20140219git
- New snapshot with LLVM 3.4 support.
- Add patch to properly set FFmpeg include directory.

* Tue Jan 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-6.20130827git
- Rebuilt for librtmp

* Tue Nov 05 2013 Xavier Bachelot <xavier@bachelot.org> 0.7.2-5.20130827git
- Rebuild for ffmpeg 2.1.

* Tue Aug 27 2013 Xavier Bachelot <xavier@bachelot.org> - 0.7.2-4.20130827git
- Update to git snapshot.
- Drop obsolete patches.

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-3.1
- Rebuilt for FFmpeg 2.0.x

* Tue Jun 11 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-2.1
- Rebuilt for LLVM soname fix

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-2
- Rebuilt for x264/FFmpeg

* Sat May 11 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.7.2-1
- New upstream release 0.7.2
- Fix building with llvm-3.3
- Rebuild for new boost libs

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.1-2.1
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.1-2
- Rebuilt for ffmpeg

* Fri Dec 28 2012 Xavier Bachelot <xavier@bachelot.org> - 0.7.1-1
- Update to 0.7.1.

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-1.1
- Rebuilt for FFmpeg 1.0

* Sun Oct 28 2012 Xavier Bachelot <xavier@bachelot.org> - 0.7.0-1
- Update to 0.7.0.

* Wed Oct 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0.1-3
- Rebuilt for boost GLEW

* Tue Jul 03 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.6.0.1-2
- Rebuild

* Tue Jul 03 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.6.0.1-1
- Update to 0.6.0.1

* Mon May 21 2012 Xavier Bachelot <xavier@bachelot.org> - 0.5.7-1
- Update to 0.5.7.

* Mon Mar 12 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.5-2
- Release bump

* Mon Mar 12 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.5-1
- Update to 0.5.5

* Fri Feb 10 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.4.1-1
- Update to 0.5.4.1

* Mon Dec 05 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.3-1
- Update to 0.5.3

* Tue Nov 15 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.2.1-1
- Update to upstream 0.5.2.1 release

* Sun Sep 11 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.0-2
- BR libffi-devel

* Sun Sep 11 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.0-1
- Update to 0.5.0 final

* Sat Jul 09 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.5.0-0.1.rc1
- Update to 0.5.0 rc1
- Removed fontconfig-devel and ftgl-devel from BR
- Removed hicolor-icon-theme from Requires ( automatically pulled by gtk )

* Fri May 27 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.8.1-1
- Update 0.4.8.1

* Thu May 05 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.7.1-1
- Update to 0.4.7.1

* Tue Mar 22 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.6.1-1
- Update to 0.4.6.1

* Wed Mar 16 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.6-1
- Update to 0.4.6 final

* Sun Mar 13 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.6.0-0.1.20110313git
- New snapshot, fixes buttons display on youtube

* Fri Mar 04 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5.3-1.20110304git
- Update to 0.4.5.3

* Wed Feb 09 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5.2-1.20110209git
- Today's snapshot, fixes a youtube crasher

* Sun Jan 09 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5.1-3.20110109git
- Today's snapshot, fixes a crash on some websites

* Sat Jan 08 2011 Hicham HAOAURI <hicham.haouari@gmail.com> - 0.4.5.1-2.20110108git
- Today's snapshot, with gradients support

* Thu Dec 16 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5.1-1
- New bugfix release

* Wed Dec 08 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5-1
- Update to 0.4.5 final

* Thu Nov 25 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.5-0.1.rc1
- Release candidate for the upcoming version
- Drop noexecstack patch ( merged upstream )

* Sat Nov 20 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4.3-4
- Avoid creating executable stack, fixes :
  https://bugs.launchpad.net/lightspark/+bug/668677

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.4.3-2
- Rebuilt for gcc bug

* Fri Sep 24 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4.3-1
- New bugfix release

* Sun Sep 12 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4.2-1
- New bugfix release

* Thu Sep 02 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4.1-1
- New bugfix release

* Sun Aug 29 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4-1
- New upstream release

* Sat Aug 28 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.3-2.20100825git
- Resnapshot to latest git

* Tue Aug 10 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.3-1
- New upstream release

* Thu Aug 05 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2.3-1
- Fix more crashes

* Tue Jul 27 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2.2-1
- Add gnash fallback

* Sat Jul 24 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2.1-1
- New bugfix release

* Tue Jul 20 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-1
- 0.4.2 release

* Mon Jul 19 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.4.20100719git.rc2
- Fix sound synchronization

* Sun Jul 04 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.3.20100707git.rc2
- Attempt to fix buffer alignment issue

* Sun Jul 04 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.2.rc2
- New release candidate

* Wed Jun 23 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.1.rc1
- Initial package for fedora
