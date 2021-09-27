%bcond_with tightspark

#global git_snapshot 1
%global commit       7dd881170a1ed48596c19bac48cdcdd403f70841
%global commit_short %(c=%{commit}; echo ${c:0:7})
%global date         20170422

Name:           lightspark
Version:        0.8.5
Release:        3%{?git_snapshot:.%{date}git%{commit_short}}%{?dist}
Summary:        An alternative Flash Player implementation
License:        LGPLv3+
URL:            http://lightspark.github.io/
%if 0%{?git_snapshot}
Source0:        https://github.com/lightspark/lightspark/archive/%{commit}.tar.gz#/%{name}-%{version}-%{date}git%{commit_short}.tar.gz
%else
Source0:        https://github.com/lightspark/lightspark/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# Fix build on EL7 (gcc4.8)
# https://github.com/lightspark/lightspark/commit/4d81b0977433f52d944d89a3c527162eb4a15c2f.patch
Patch0:         lightspark-0.8.5-gcc48.patch

BuildRequires:  cmake3
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  glew-devel >= 1.5.4
BuildRequires:  gtkglext-devel
BuildRequires:  libcurl-devel
BuildRequires:  libffi-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  librtmp-devel
BuildRequires:  nasm
BuildRequires:  ncurses-devel
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
%if 0%{?git_snapshot}
%setup -q -n %{name}-%{commit}
%else
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .gcc48
%endif


%build
%cmake3 \
    -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins" \
    -DPPAPI_PLUGIN_DIRECTORY="%{_libdir}/chromium-browser/PepperFlash/" \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%{?with_tightspark:    -DCOMPILE_TIGHTSPARK=1} \
     .

%cmake3_build


%install
%cmake3_install
%find_lang %{name}

%if %{with tightspark}
pushd %{buildroot}%{_datadir}/man/man1
    ln -s %{name}.1.gz tightspark.1.gz
popd
%endif

#remove devel file from package
rm %{buildroot}%{_libdir}/%{name}/lib%{name}.so

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files -f %{name}.lang
%license COPYING COPYING.LESSER
%doc ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/lightspark.conf
%{_bindir}/%{name}
%{?with_tightspark:%{_bindir}/tightspark}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/man/man1/%{name}.1.*
%{?with_tightspark:%{_datadir}/man/man1/tightspark.1.*}
%{_libdir}/%{name}/

%files mozilla-plugin
%license COPYING COPYING.LESSER
%{_libdir}/mozilla/plugins/lib%{name}plugin.so

%files chromium-plugin
%license COPYING COPYING.LESSER
%{_libdir}/chromium-browser/PepperFlash/libpepflashplayer.so
%{_libdir}/chromium-browser/PepperFlash/manifest.json


%changelog
* Fri Nov 26 2021 Xavier Bachelot <xavier@bachelot.org> - 0.8.5-3
- Fix build for EL7 (gcc 4.8)

* Thu Nov 11 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8.5-2
- Rebuilt for new ffmpeg snapshot

* Wed Sep 15 2021 Xavier Bachelot <xavier@bachelot.org> - 0.8.5-1
- Update to 0.8.5

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8.3-4
- Rebuilt for new ffmpeg snapshot

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Aug 06 2020 Xavier Bachelot <xavier@bachelot.org> - 0.8.3-2
- Use new cmake macros

* Wed Jul 08 2020 Xavier Bachelot <xavier@bachelot.org> - 0.8.3-1
- Update to 0.8.3

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 0.8.2-4
- Rebuilt for Boost 1.73

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8.2-3
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 27 2019 Xavier Bachelot <xavier@bachelot.org> - 0.8.2-1
- Update to 0.8.2.
- Build with debuginfo enabled.
- Remove pre_release and simplify snapshot handling.
- Minor spec cleanup.
- tightspark is not built by default anymore, add a bcond_with switch.

* Mon Aug 12 2019 Xavier Bachelot <xavier@bachelot.org> - 0.8.1-5
- Add patch to build with libswresample rather than deprecated libavresample.
- Drop old ffmpeg include dir patch.

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.8.1-4.2
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Xavier Bachelot <xavier@bachelot.org> - 0.8.1-4
- Add patch to disable llvm dependency.

* Tue Sep 04 2018 Xavier Bachelot <xavier@bachelot.org> - 0.8.1-3
- Fix build on ppc64.

* Tue Jul 31 2018 Xavier Bachelot <xavier@bachelot.org> - 0.8.1-2
- Remove ppc64le from ExcludeArch:.

* Sat Jul 21 2018 Xavier Bachelot <xavier@bachelot.org> - 0.8.1-1
- Update to 0.8.1.
- Add BR: gcc-c++.
- Simplify Version: and Release: handling.

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8.0-2.4
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8.0-2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.8.0-2.2
- Rebuild for boost-1.66
- Remove scriptlets

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
