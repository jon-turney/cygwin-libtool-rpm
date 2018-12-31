# must be rebuilt with each new version of cygwin*-gcc
%define gcc_version 7.4.0

%{?cygwin_package_header}
%global debug_package %{nil}

Name:      cygwin-libtool
Version:   2.4.6
Release:   7%{?dist}
Summary:   Libtool for Cygwin toolchain

Group:     Development/Tools
License:   GPLv2+ and LGPLv2+ and GFDL
URL:       http://www.gnu.org/software/libtool/
Source0:   http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz
Patch0:    libtool-2.4.5-pass-ldflags.patch

BuildRequires: autoconf automake
BuildRequires: help2man

BuildRequires: cygwin32-filesystem
BuildRequires: cygwin32-binutils
BuildRequires: cygwin32-gcc = %{gcc_version}
BuildRequires: cygwin32-gcc-c++
BuildRequires: cygwin32-gcc-gfortran
BuildRequires: cygwin32

BuildRequires: cygwin64-filesystem
BuildRequires: cygwin64-binutils
BuildRequires: cygwin64-gcc = %{gcc_version}
BuildRequires: cygwin64-gcc-c++
BuildRequires: cygwin64-gcc-gfortran
BuildRequires: cygwin64

%description
Libtool for Cygwin toolchain

%package base
Summary:   Libtoolize for Cygwin toolchains
BuildArch: noarch
Requires:  autoconf automake sed

%description base
Libtoolize for Cygwin toolchains

%package -n cygwin32-libtool
Summary:   Libtool for Cygwin32 toolchain
Requires:  cygwin32-gcc = %{gcc_version}
Requires:  cygwin32-libltdl = %{version}-%{release}
Requires:  %{name}-base = %{version}-%{release}

%description -n cygwin32-libtool
Libtool scripts for Cygwin i686 toolchain

%package -n cygwin64-libtool
Summary:   Libtool for Cygwin64 toolchain
Requires:  cygwin64-gcc = %{gcc_version}
Requires:  cygwin64-libltdl = %{version}-%{release}
Requires:  %{name}-base = %{version}-%{release}

%description -n cygwin64-libtool
Libtool scripts for Cygwin x86_64 toolchain

%package -n cygwin32-libltdl
Summary:   Libtool Dynamic Module Loader library for Cygwin32 toolchain
Group:     Development/Libraries
License:   LGPLv2+
BuildArch: noarch

%description -n cygwin32-libltdl
Libtool dynamic module loader library for Cygwin i686 toolchain

%package -n cygwin64-libltdl
Summary:   Libtool Dynamic Module Loader library for Cygwin64 toolchain
Group:     Development/Libraries
License:   LGPLv2+
BuildArch: noarch

%description -n cygwin64-libltdl
Libtool dynamic module loader library for Cygwin x86_64 toolchain


%prep
%setup -q -n libtool-%{version}
%patch0 -p2
#./bootstrap


%build
%cygwin_configure --enable-shared --disable-static
# build not smp safe
%cygwin_make


%install
%cygwin_make install DESTDIR=$RPM_BUILD_ROOT

# Must keep .la files, required by LTDL_INIT

# Documentation already provided by Fedora native package
rm -fr $RPM_BUILD_ROOT%{cygwin32_docdir}/
rm -fr $RPM_BUILD_ROOT%{cygwin32_infodir}/
rm -fr $RPM_BUILD_ROOT%{cygwin32_mandir}/

rm -fr $RPM_BUILD_ROOT%{cygwin64_docdir}/
rm -fr $RPM_BUILD_ROOT%{cygwin64_infodir}/
rm -fr $RPM_BUILD_ROOT%{cygwin64_mandir}/

# Some packages (e.g. ncurses) build with the installed libtool
install -D -m0755 $RPM_BUILD_ROOT%{cygwin32_bindir}/libtool \
  $RPM_BUILD_ROOT%{_bindir}/%{cygwin32_target}-libtool
install -D -m0755 $RPM_BUILD_ROOT%{cygwin64_bindir}/libtool \
  $RPM_BUILD_ROOT%{_bindir}/%{cygwin64_target}-libtool

# libtoolize is run only once during %%prep, not per-arch
install -d -m0755 $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{cygwin32_datadir}/aclocal/ \
  $RPM_BUILD_ROOT%{cygwin32_datadir}/libtool/m4
mv $RPM_BUILD_ROOT%{cygwin32_datadir}/libtool/ \
  $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{cygwin32_bindir}/libtoolize \
  $RPM_BUILD_ROOT%{_bindir}/cygwin-libtoolize
sed -i -e "s|%{cygwin32_datadir}/libtool|%{_datadir}/%{name}|" \
  -e "s|%{cygwin32_datadir}/aclocal|%{_datadir}/%{name}/m4|" \
  -e "s|%{cygwin32_prefix}|/usr|" \
  $RPM_BUILD_ROOT%{_bindir}/cygwin-libtoolize
# remove duplicates
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/libtoolize
rm -fr $RPM_BUILD_ROOT%{cygwin64_datadir}/


%files base
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog*
%{_bindir}/cygwin-libtoolize
%{_datadir}/%{name}/

%files -n cygwin32-libtool
%{_bindir}/%{cygwin32_target}-libtool
%{cygwin32_bindir}/libtool

%files -n cygwin64-libtool
%{_bindir}/%{cygwin64_target}-libtool
%{cygwin64_bindir}/libtool

%files -n cygwin32-libltdl
%doc libltdl/COPYING.LIB libltdl/README
%{cygwin32_bindir}/cygltdl-7.dll
%{cygwin32_includedir}/libltdl/
%{cygwin32_includedir}/ltdl.h
%{cygwin32_libdir}/libltdl.dll.a
%{cygwin32_libdir}/libltdl.la

%files -n cygwin64-libltdl
%doc libltdl/COPYING.LIB libltdl/README
%{cygwin64_bindir}/cygltdl-7.dll
%{cygwin64_includedir}/libltdl/
%{cygwin64_includedir}/ltdl.h
%{cygwin64_libdir}/libltdl.dll.a
%{cygwin64_libdir}/libltdl.la


%changelog
* Mon Dec 31 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-7
- rebuilt for cygwin-gcc 7.4.0

* Tue Jun 05 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-6
- rebuilt for cygwin-gcc 7.3.0

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-5
- Rebuilt for cygwin-gcc 6.4.0

* Mon Sep 12 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-4
- Rebuilt to fix dependencies

* Thu Aug 04 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-3
- Rebuilt for cygwin-gcc 5.4.0

* Mon Feb 22 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-2
- Rebuilt for cygwin*-gcc 5.3.0

* Fri Jun 19 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.6-1
- new version, built for cygwin-gcc 4.9.2

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.2-4
- Create base subpackage with libtoolize for building on EL6

* Tue Jun 10 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.4.2-3
- Rebuilt for cygwin*-gcc 4.8.2.

* Sun Jan 19 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.4.2-2
- Rebuilt for cygwin*-gcc 4.8.2.

* Fri Jun 28 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.4.2-1
- Version bump.
- Update for new Cygwin packaging scheme.

* Thu Mar 22 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.4-2
- Remove noarch tag, as arch-specific gcc libdir is embedded in libtool script.
- Create separate libltdl noarch package.

* Thu Jul 07 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.4-1
- Initial RPM release.
