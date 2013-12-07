%define	major	1
%define	libname	%mklibname iscsi %{major}
%define	devname	%mklibname -d iscsi

Name:		libiscsi
Summary:	iSCSI client library
Version:	1.9.0
Release:	5
License:	LGPLv2+
Group:		System/Libraries
URL:		https://github.com/sahlberg/%{name}

Source0:	https://sites.google.com/site/libiscsitarballs/libiscsitarballs/%{name}-%{version}.tar.gz
Patch0:		libiscsi-1.9.0-use-libgcrypt-for-MD5.patch
Patch1:		libiscsi-1.9.0-fix-strict-aliasing-violation.patch
Patch2:		libiscsi-1.9.0-disable-Werror.patch

BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(libgcrypt)

%description
libiscsi is a library for attaching to iSCSI resources across
a network.

%package -n	%{libname}
Summary:	iSCSI client library
Group:		System/Libraries

%description -n	%{libname}
libiscsi is a library for attaching to iSCSI resources across
a network.

%package -n	%{devname}
Summary:	iSCSI client development libraries
Group:		Development/C
Provides:	iscsi-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
The libiscsi-devel package includes the header files for libiscsi.

%package	utils
Summary:	iSCSI Client Utilities
Group:		Networking/File transfer
License:	GPLv2+

%description	utils
The libiscsi-utils package provides a set of assorted utilities to connect
to iSCSI servers without having to set up the Linux iSCSI initiator.

%prep
%setup -q
%patch0 -p1 -b .gcrypt~
%patch1 -p1 -b .aliasing~
%patch2 -p1 -b .werror~
autoreconf -fi

%build
%ifarch %{ix86} %arm
LDFLAGS="%{ldflags} -fuse-ld=bfd" \
%endif
%configure	 --disable-static
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libiscsi.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/iscsi
%{_includedir}/iscsi/*.h
%{_libdir}/libiscsi.so
%{_libdir}/pkgconfig/libiscsi.pc

%files utils
%doc README TODO
%{_bindir}/ld_iscsi.so
%{_bindir}/iscsi-ls
%{_bindir}/iscsi-inq
%{_bindir}/iscsi-readcapacity16

%changelog
* Fri Jun 14 2013 Per Øyvind Karlsen <peroyvind@moondrake.net> 1.9.0-1
- initial moondrake package based on fedora package

* Fri May 3 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-4
- Add patch 2 for FIPS mode
- Add patch 3 to avoid segmentation fault on iscsi-tools

* Thu Mar 7 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-3
- Correct license for libiscsi-utils, prefer %%global to %%define
- Add Requires
- Remove %%clean section

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-2
- Use %%config for ld.so.conf.d file.

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-1
- Initial version (bug 914752)
