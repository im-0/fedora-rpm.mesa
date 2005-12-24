#!/bin/bash
# NOTE: /bin/bash shebang on first line to get shell script syntax
# highlighting in mcedit.  (temporary hack)

# NOTE: Build target macros:  For now, we will just use build_fc and
# build_rhel to simplify things, until there is a reason to break it
# into per-release macros.  Only 1 of these macros should be enabled.
%define build_fc	1
%define build_rhel	0

#-- DRI Build Configuration ------------------------------------------
# NOTE: Enable DRI on PPC for Fedora Core Mac users, but disable on
# RHEL for improved stability, as DRI isn't really that important
# on server platforms.
%if %{build_fc}
%define with_dri_ppc 1
%endif
%if %{build_rhel}
%define with_dri_ppc 0
%endif
# Define arches to make with_dri enabled by default
%ifarch %{ix86} x86_64 ia64 alpha
%define with_dri 1
%endif
# Define PPC OS variant override.
%ifarch ppc
%define with_dri %{with_dri_ppc}
%endif
# Define arches to make with_dri disabled by default
%ifarch ppc64 s390 s390x
%define with_dri 0
%endif

# FIXME: libOSMesa does not build when DRI is enabled for some reason.  It
# seems next to impossible using the totally broken Mesa buildsystem to build
# both DRI drivers and OSMesa in a single build.  If someone feels like fixing
# all this to build on all 7 architectures, be my guest.
%if %{with_dri}
%define with_OSMesa	0
%else
%define with_OSMesa	1
%endif

# NOTE: This option enables motif support in libGLw for bug #175251
%define with_motif	1

#-- END DRI Build Configuration ------------------------------------------

Summary: Mesa graphics libraries
Name: mesa
Version: 6.4.1
Release: 3
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.mesa3d.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: MesaLib-%{version}.tar.bz2
Source1: redhat-mesa-target
Source2: redhat-mesa-driver-install
Source3: redhat-mesa-source-filelist-generator
#Patch0: mesa-6.3.2-makedepend.patch
Patch0: mesa-6.3.2-build-configuration-v4.patch
Patch1: mesa-6.3.2-fix-installmesa.patch
Patch2: mesa-6.4-multilib-fix.patch
Patch3: mesa-modular-dri-dir.patch
Patch4: mesa-6.4.1-libGLw-enable-motif-support.patch
#Patch4: mesa-6.4.1-enable-osmesa.patch
# General patches from upstream go here:
# FIXME: mesa-6.4.1-amd64-assyntax-fix.patch is backported from Mesa 6.4
# branch and can be dropped when we update to 6.4.2.
Patch100: mesa-6.4.1-amd64-assyntax-fix.patch

BuildRequires: pkgconfig
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: libXxf86vm-devel
%if %{with_motif}
BuildRequires: openmotif-devel
%endif

%description
Mesa

#-- libGL ------------------------------------------------------------
%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers.
Group: System Environment/Libraries

Provides: libGL

# libGL used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa
# libGL moved to XFree86-libs for RHL 7.3
Obsoletes: XFree86-libs
# libGL moved to XFree86-Mesa-libGL for RHL 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-Mesa-libGL
# libGL moved to xorg-x11-Mesa-libGL for FC[2-4], RHEL4
Obsoletes: xorg-x11-Mesa-libGL
# Conflict with the xorg-x11-libs too, just to be safe for file conflicts
Obsoletes: xorg-x11-libs

%description libGL
Mesa libGL runtime libraries and DRI drivers.
#-- libGL ------------------------------------------------------------
%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Requires: libX11-devel

Provides: libGL-devel

# libGL devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa-devel
# libGL devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-devel
# libGL devel files moved to xorg-x11-devel for FC2, FC3, FC4
Obsoletes: xorg-x11-devel

%description libGL-devel
Mesa libGL development package
#-- libGLU -----------------------------------------------------------
%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries

Provides: libGLU

# libGLU used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa
# libGLU moved to XFree86-libs for RHL 7.3
Obsoletes: XFree86-libs
# libGLU moved to XFree86-Mesa-libGLU for RHL 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-Mesa-libGLU
# libGLU moved to xorg-x11-Mesa-libGLU for FC[2-4], RHEL4
Obsoletes: xorg-x11-Mesa-libGLU
# Obsolete xorg-x11-libs too, just to be safe
Obsoletes: xorg-x11-libs

%description libGLU
Mesa libGLU runtime library
#-- libGLU-devel -----------------------------------------------------
%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
Requires: mesa-libGLU = %{version}-%{release}
Requires: libGL-devel

Provides: libGLU-devel

# libGLU devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa-devel
# libGLU devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-devel
# libGLU devel files moved to xorg-x11-devel for FC2, FC3, FC4
Obsoletes: xorg-x11-devel

%description libGLU-devel
Mesa libGLU development package
#-- libGLw -----------------------------------------------------------
%package libGLw
Summary: Mesa libGLw runtime library
Group: System Environment/Libraries

Provides: libGLw

# libGLw used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa
# libGLw moved to XFree86-libs for RHL 7.3, 8, 9, FC1, RHEL 3
Obsoletes: XFree86-libs
# libGLw moved to xorg-x11-libs FC[2-4], RHEL4
Obsoletes: xorg-x11-libs

%description libGLw
Mesa libGLw runtime library
#-- libGLw-devel -----------------------------------------------------
%package libGLw-devel
Summary: Mesa libGLw development package
Group: Development/Libraries
Requires: libGLw = %{version}-%{release}

Provides: libGLw-devel

# libGLw devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa-devel
# libGLw devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-devel
# libGLw devel files moved to xorg-x11-devel for FC2, FC3, FC4
Obsoletes: xorg-x11-devel

%description libGLw-devel
Mesa libGLw development package
#-- source -----------------------------------------------------------
%package source
Summary: Mesa source code required to build X server
Group: Development/Libraries

%description source
The mesa-source package provides the minimal source code needed to
build DRI enabled X servers, etc.

#-- prep -------------------------------------------------------------
%prep
%setup -q -n Mesa-%{version}
# Copy Red Hat Mesa build/install simplificomplication scripts into build dir.
install -m 755 %{SOURCE1} ./
install -m 755 %{SOURCE2} ./
install -m 755 %{SOURCE3} ./

#%patch0 -p0 -b .makedepend
%patch1 -p0 -b .fix-installmesa
%patch2 -p0 -b .multilib-fix
%patch3 -p1 -b .modular
%if %{with_motif}
%patch4 -p0 -b .libGLw-enable-motif-support
%endif

%patch100 -p1 -b .amd64-assyntax-fix

# WARNING: The following files are copyright "Mark J. Kilgard" under the GLUT
# license and are not open source/free software, so we remove them.
rm include/GL/uglglutshapes.h

#-- Build ------------------------------------------------------------
%build
# Macroize this to simplify things
%define makeopts MKDEP="gcc -M" MKDEP_OPTIONS="-MF depend"
export CFLAGS="$RPM_OPT_FLAGS"
export LIB_DIR=$RPM_BUILD_ROOT%{_libdir}
export INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
export DRI_DRIVER_DIR="%{_libdir}/dri"

# NOTE: We use a custom script to determine which Mesa build target should
# be used, and reduce spec file clutter.
MESATARGET="$(./redhat-mesa-target %{with_dri} %{_arch})"
#DRIVER_DIRS="dri osmesa"

echo -e "********************\nMESATARGET=$MESATARGET\n********************\n"
make ${MESATARGET} %{makeopts}


#-- Install ----------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT
# NOTE: the rpm makeinstall macro does not work for mesa
#%%makeinstall DESTDIR=$RPM_BUILD_ROOT
# NOTE: "make install" calls mesa's installmesa script, passing DESTDIR
# to it as a commandline arg, but LIB_DIR and INCLUDE_DIR get hard coded in
# that script, meaning multilib breaks.
#make install DESTDIR=$RPM_BUILD_ROOT/usr

# NOTE: Since Mesa's install procedure doesn't work on multilib properly,
# we fix it here, as I have patched the installmesa script to remove the
# hard coding, and we set the variables ourself right here, and it should
# hopefully pick them up.
#	-- Mike A. Harris <mharris@redhat.com>
export LIB_DIR=$RPM_BUILD_ROOT%{_libdir}
export INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
bin/installmesa $RPM_BUILD_ROOT/usr
install -m 644 src/glw/GLw{,M}DrawA{,P}.h $RPM_BUILD_ROOT%{_includedir}/GL/

%if %{with_dri}
#pushd src/mesa/drivers/dri
#    make install DESTDIR=$RPM_BUILD_ROOT/usr %{makeopts}
#popd
# NOTE: Since Mesa's install target does not seem to properly install the
# DRI modules, we install them by hand here.  -- mharris
export DRIMODULE_SRCDIR="%{_lib}"
export DRIMODULE_DESTDIR="$RPM_BUILD_ROOT%{_libdir}/dri"
./redhat-mesa-driver-install %{_arch}
%endif

# Run custom source filelist generator script, passing it a prefix
%define mesa_source_filelist mesa-source-rpm-filelist.lst
%define mesasourcedir %{_datadir}/mesa/source

./redhat-mesa-source-filelist-generator $RPM_BUILD_ROOT %{mesasourcedir}

#-- Clean ------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

#-- Check ------------------------------------------------------------
%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libGLU -p /sbin/ldconfig
%postun libGLU -p /sbin/ldconfig
%post libGLw -p /sbin/ldconfig
%postun libGLw -p /sbin/ldconfig

%files libGL
%defattr(-,root,root,-)
%dir %{_libdir}
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.2
# x86 DRI modules
%if %{with_dri}
# NOTE: It is libGL.so.1.2 in DRI builds, and libGL.so.1.5.060400 in non-DRI
# builds, although it isn't clear what the rationale for this is to me yet,
# nonetheless, I'm conditionalizing it to get it to build.
#%{_libdir}/libGL.so.1.2
%dir %{_libdir}/dri
# NOTE: This is a glob for now, as we explicitly determine and limit the DRI
# drivers that are installed on a given OS/arch combo in our custom DRI
# driver install script.  If the upstream install script improves enough to
# make our script unnecessary, we might want to change to an explicit file
# manifest here in the future.
%{_libdir}/dri/*_dri.so
# NOTE: Documentive list of all DRI drivers built by default in Mesa 6.4.1
#%{_libdir}/dri/ffb_dri.so
#%{_libdir}/dri/i810_dri.so
#%{_libdir}/dri/i830_dri.so
#%{_libdir}/dri/i915_dri.so
#%{_libdir}/dri/mach64_dri.so
#%{_libdir}/dri/mga_dri.so
#%{_libdir}/dri/r128_dri.so
#%{_libdir}/dri/r200_dri.so
#%{_libdir}/dri/r300_dri.so
#%{_libdir}/dri/radeon_dri.so
#%{_libdir}/dri/s3v_dri.so
#%{_libdir}/dri/savage_dri.so
#%{_libdir}/dri/sis_dri.so
#%{_libdir}/dri/tdfx_dri.so
#%{_libdir}/dri/trident_dri.so
#%{_libdir}/dri/unichrome_dri.so
%endif
%if %{with_OSMesa}
# NOTE: This is the software rasterizer only.  Why it is 1.5.* is not clear
# to me currently, but it is a change from Xorg 6.8.2's Mesa.
#%{_libdir}/libGL.so.1.5.060400
%{_libdir}/libOSMesa.so.6
%{_libdir}/libOSMesa.so.6.4.060401
%endif

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/amesa.h
%{_includedir}/GL/directfbgl.h
%{_includedir}/GL/dmesa.h
%{_includedir}/GL/fxmesa.h
%{_includedir}/GL/ggimesa.h
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/mesa_wgl.h
%{_includedir}/GL/mglmesa.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/svgamesa.h
#%{_includedir}/GL/uglglutshapes.h
%{_includedir}/GL/uglmesa.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h
%{_libdir}/libGL.so
%if ! %{with_dri}
%{_libdir}/libOSMesa.so
%endif

%files libGLU
%defattr(-,root,root,-)
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.060401

%files libGLU-devel
%defattr(-,root,root,-)
%{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h

%files libGLw
%defattr(-,root,root,-)
%{_libdir}/libGLw.so.1
%{_libdir}/libGLw.so.1.0.0

%files libGLw-devel
%defattr(-,root,root,-)
%{_libdir}/libGLw.so
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h

%files source -f mesa-source-rpm-filelist.lst
%defattr(-,root,root,-)

%changelog
* Sat Dec 24 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-3
- Manually copy libGLw headers that Mesa forgets to install, to fix (#173879).
- Added mesa-6.4.1-libGLw-enable-motif-support.patch to fix (#175251).
- Removed "Conflicts" lines from libGL package, as they are "Obsoletes" now.
- Do not rename swrast libGL .so version, as it is the OpenGL version.

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-2
- Rebuild to ensure libGLU gets rebuilt with new gcc with C++ compiler fixes.
- Changed the 3 devel packages to use Obsoletes instead of Conflicts for the
  packages the files used to be present in, as this is more friendy for
  OS upgrades.
- Added "Requires: libX11-devel" to mesa-libGL-devel package (#173712)
- Added "Requires: libGL-devel" to mesa-libGLU-devel package (#175253)

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-1
- Updated MesaLib tarball to version 6.4.1 from Mesa project for X11R7 RC4.
- Added pkgconfig dependency.
- Updated "BuildRequires: libdrm-devel >= 2.0-1"
- Added Obsoletes lines to all the subpackages to have cleaner upgrades.
- Added mesa-6.4.1-amd64-assyntax-fix.patch to work around a build problem on
  AMD64, which is fixed in the 6.4 branch of Mesa CVS.
- Conditionalize libOSMesa inclusion, and default to not including it for now.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 6.4-5.1
- rebuilt

* Sun Nov 20 2005 Jeremy Katz <katzj@redhat.com> 6.4-5
- fix directory used for loading dri modules (#173679)
- install dri drivers as executable so they get stripped (#173292)

* Thu Nov 3 2005 Mike A. Harris <mharris@redhat.com> 6.4-4
- Wrote redhat-mesa-source-filelist-generator to dynamically generate the
  files to be included in the mesa-source subpackage, to minimize future
  maintenance.
- Fixed detection and renaming of software mesa .so version.

* Wed Nov 2 2005 Mike A. Harris <mharris@redhat.com> 6.4-3
- Hack: autodetect if libGL was given .so.1.5* and rename it to 1.2 for
  consistency on all architectures, and to avoid upgrade problems if we
  ever disable DRI on an arch and then re-enable it later.

* Wed Nov 2 2005 Mike A. Harris <mharris@redhat.com> 6.4-2
- Added mesa-6.4-multilib-fix.patch to instrument and attempt to fix Mesa
  bin/installmesa script to work properly with multilib lib64 architectures.
- Set and export LIB_DIR and INCLUDE_DIR in spec file 'install' section,
  and invoke our modified bin/installmesa directly instead of using
  "make install".
- Remove "include/GL/uglglutshapes.h", as it uses the GLUT license, and seems
  like an extraneous file anyway.
- Conditionalize the file manifest to include libGL.so.1.2 on DRI enabled
  builds, but use libGL.so.1.5.060400 instead on DRI disabled builds, as
  this is how upstream builds the library, although it is not clear to me
  why this difference exists yet (which was not in Xorg 6.8.2 Mesa).

* Thu Oct 27 2005 Mike A. Harris <mharris@redhat.com> 6.4-1
- Updated to new upstream MesaLib-6.4
- Updated libGLU.so.1.3.060400 entry in file manifest
- Updated "BuildRequires: libdrm-devel >= 1.0.5" to pick up fixes for the
  unichrome driver.

* Tue Sep 13 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-6
- Fix redhat-mesa-driver-install and spec file to work right on multilib
  systems.
  
* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-5
- Fix mesa-libGL-devel to depend on mesa-libGL instead of mesa-libGLU.
- Added virtual "Provides: libGL..." entries for each subpackage as relevant.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-4
- Added the mesa-source subpackage, which contains part of the Mesa source
  code needed by other packages such as the X server to build stuff.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-3
- Added Conflicts/Obsoletes lines to all of the subpackages to make upgrades
  from previous OS releases, and piecemeal upgrades work as nicely as
  possible.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-2
- Wrote redhat-mesa-target script to simplify mesa build target selection.
- Wrote redhat-mesa-driver-install to install the DRI drivers and simplify
  per-arch conditionalization, etc.

* Sun Sep 4 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-1
- Initial build.
