%define debug 0

%define git 0

%if %{git}
%define git_snapshot 1
%endif

%define pre_release 0

%if %{?git}
%define commit 13e17fbc018022340ddeec44c6f5d464674ec728
%define date 20110610
%endif

%if %{pre_release}
%define pre rc1
%endif 

%define rel 1

%define major 0.7.2

Name:           lightspark
Version:        %{major}
Release:        %{?pre:0.}%{rel}%{?git_snapshot:.%{date}git}%{?pre:.%{pre}}%{?dist}
Summary:        An alternative Flash Player implementation

Group:          Applications/Multimedia
License:        LGPLv3+
URL:            http://lightspark.sourceforge.net
%if %{git}
# This is a git snapshot, to get it, follow this steps :
# git clone git://github.com/lightspark/lightspark.git
# cd %%{name}
# git checkout %%{commit} *
# rm -rf .git && cd ..
# mv %%{name} %%{name}-%%{version}
# tar cjf %%{name}-%%{version}-%%{date}git.tar.bz2 %%{name}-%%{version}       
Source0:        %{name}-%{version}-%{date}git.tar.bz2
%else
Source0:        http://launchpad.net/%{name}/trunk/%{name}-%{version}/+download/%{name}-%{version}%{?pre:~%{pre}}.tar.gz
%endif

Patch0:         %{name}-0.5.5-remove-llvm-version-check.patch
Patch1:         lightspark-0.7.2-llvm33.patch
Patch2:         lightspark-0.7.2-llvm-libs-hack.patch

BuildRequires:  cmake
BuildRequires:  llvm-devel >= 2.7
BuildRequires:  glew-devel >= 1.5.4
BuildRequires:  ffmpeg-devel
BuildRequires:  nasm
BuildRequires:  SDL-devel
BuildRequires:  gtkglext-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pcre-devel
BuildRequires:  xulrunner-devel >= 1.9.2
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  boost-devel
BuildRequires:  gettext
BuildRequires:  libxml++-devel >= 2.33.1
BuildRequires:  librtmp-devel
BuildRequires:  libffi-devel
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

%prep
%setup -q -n %{name}-%{version}%{?pre:~%{pre}}
%patch0 -p1 -b .remove-llvm-version-check
%patch1 -p1 -b .llvm33
%patch2 -p1 -b .llvm-libs-hack

%build
%cmake -DCOMPILE_PLUGIN=1  \
       -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins" \
       -DENABLE_SOUND=1 \
%if %{debug}
       -DCMAKE_BUILD_TYPE=Debug \
%else
       -DCMAKE_BUILD_TYPE=Release \
%endif
       -DAUDIO_BACKEND=pulse \
       .

make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

pushd $RPM_BUILD_ROOT%{_datadir}/man/man1
    ln -s %{name}.1.gz tightspark.1.gz
popd

#remove devel file from package
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so

install -Dpm 644 media/%{name}-logo.svg $RPM_BUILD_ROOT%{_datadir}/%{name}

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/lightspark.conf
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/man/man1/%{name}.1.gz
%{_datadir}/man/man1/tightspark.1.gz
%{_libdir}/%{name}

%files mozilla-plugin
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER
%{_libdir}/mozilla/plugins/lib%{name}plugin.so

%changelog
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
