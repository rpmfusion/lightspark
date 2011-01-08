%define debug 0

%define git 1

%if %{git}
%define git_snapshot 1
%endif

%define pre_release 0

%if %{?git}
%define commit c9fbbca66ce214e8df2d59aae90af6427af5057f
%define date 20110108
%endif

%if %{pre_release}
%define pre rc1
%endif 

%define rel 2

%define major 0.4.5

Name:           lightspark
Version:        %{major}.1
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
Source0:        http://launchpad.net/%{name}/trunk/%{name}-%{major}/+download/%{name}-%{version}%{?pre:~%{pre}}.tar.gz
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  llvm-devel >= 2.7
BuildRequires:  glew-devel >= 1.5.4
BuildRequires:  ftgl-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  nasm
BuildRequires:  SDL-devel
BuildRequires:  gtkglext-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  fontconfig-devel
BuildRequires:  pcre-devel
BuildRequires:  xulrunner-devel >= 1.9.2
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  boost-devel
BuildRequires:  gettext
BuildRequires:  libxml++-devel >= 2.33.1

Requires:       hicolor-icon-theme

%description
Lightspark is a modern, free, open-source flash player implementation.
Lightspark features:

* JIT compilation of Actionscript to native x86 bytecode using LLVM
* Hardware accelerated rendering using OpenGL Shaders (GLSL)
* Very good and robust support for current-generation Actionscript 3
* A new, clean, codebase exploiting multithreading and optimized for 
modern hardware. Designed from scratch after the official Flash 
documentation was released.

%package mozilla-plugin
Summary:       Mozilla compatible plugin for %{name}
Requires:      mozilla-filesystem
Requires:      %{name} = %{version}-%{release}

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}. It can fallback to
gnash for unsupported swf files ( AS2/avm1 ); to enable this feature
install gnash ( without gnash-plugin ).

%prep
%setup -q -n %{name}-%{version}%{?pre:~%{pre}}

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
%{_libdir}/mozilla/plugins/lib%{name}plugin.so

%changelog
* Fri Jan 08 2011 Hicham HAOAURI <hicham.haouari@gmail.com> - 0.4.5.1-2.20110108git
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

* Thu Sep 12 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.4.2-1
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

* Tue Jul 24 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2.1-1
- New bugfix release

* Tue Jul 20 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-1
- 0.4.2 release

* Sun Jul 19 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.4.20100719git.rc2
- Fix sound synchronization

* Sun Jul 04 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.3.20100707git.rc2
- Attempt to fix buffer alignment issue

* Sun Jul 04 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.2.rc2
- New release candidate

* Thu Jun 23 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.4.2-0.1.rc1
- Initial package for fedora
