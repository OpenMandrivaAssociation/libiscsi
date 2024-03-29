%define major 9
%define libname %mklibname iscsi %{major}
%define devname %mklibname -d iscsi

Name:		libiscsi
Summary:	iSCSI client library
Version:	1.19.0
Release:	2
License:	LGPLv2+
Group:		System/Libraries
URL:		https://github.com/sahlberg/%{name}
Source0:	https://github.com/sahlberg/libiscsi/archive/%{version}.tar.gz
Patch0:		libiscsi-1.19.0-clang9.patch
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gpg-error)

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
%autosetup -p1
# disable examples
sed -i 's!examples!!g' Makefile.am
./autogen.sh

%build
%ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
%endif

%setup_compile_flags

%configure --disable-static CFLAGS="$CFLAGS -Wno-error"

%make LDFLAGS="%{ldflags}" CFLAGS="%{optflags}" CC=%{__cc}

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
%{_bindir}/iscsi-ls
%{_bindir}/iscsi-inq
%{_bindir}/iscsi-readcapacity16
%{_bindir}/iscsi-swp
%{_bindir}/iscsi-perf
%{_mandir}/man1/*
