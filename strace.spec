%{?scl:%{?scl_package:%scl_package strace}}

Summary: Tracks and displays system calls associated with a running process
Name: %{?scl_prefix}strace
Version: 4.10
Release: 2%{?dist}
License: BSD
Group: Development/Debuggers
URL: http://sourceforge.net/projects/strace/
# The upstream source really comes in .xz format.  Unfortunately
# DTS builds using .xz seem to want to use /opt/rh/<...>/xz rather
# than the one in /usr/bin.  Using the .gz extension seems to avoid
# this problem.  This should be fixed at some point.
Source: http://downloads.sourceforge.net/strace/strace-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define alternatives_cmd %{!?scl:%{_sbindir}}%{?scl:%{_root_sbindir}}/alternatives
%define alternatives_cmdline %{alternatives_cmd}%{?scl: --altdir %{_sysconfdir}/alternatives --admindir %{_scl_root}/var/lib/alternatives}

BuildRequires: libacl-devel, libaio-devel, time
%{?scl:Requires:%scl_runtime}

Patch0: aarch64.patch
#
# RHBZ https://bugzilla.redhat.com/show_bug.cgi?id=1201777
#
# Patches created with git format-patch -o A dfabccf997dbad325442353926270d5b1289943f
#
# Selected minimal set to get package back into buildable state.
#
Patch0002: 0002-aarch64-fix-rt_sigreturn-decoding.patch
Patch0006: 0006-tests-select.test-handle-architectures-using-pselect.patch
Patch0007: 0007-aarch64-fix-ioctl-decoding.patch
Patch0014: 0014-aarch64-properly-decode-generic-syscalls.patch
Patch0015: 0015-stat64-v.test-add-newfstatat-syscall-support.patch
Patch0016: 0016-tests-uid-use-fchown-instead-of-chown.patch
Patch0017: 0017-Show-f_flags-field-in-printstatfs.patch

Patch1000: strace-strict-aliasing.patch
Patch1001: strace-rh948577.patch
Patch1002: strace-rh851457.patch
Patch1004: strace-rh1044044.patch
Patch1005: strace-no-net-tests.patch
Patch1006: strace-uid-gawk-interval.patch
Patch1007: strace-no-uio-tests.patch

# Hack as the RHEL 6 used for DTS is too old and doesn't define MADV_DODUMP
# and MADV_DONTDUMP.
Patch2000: strace-rh921550.patch


# In the past we had a separate strace64 package, these days the
# stndard 64 bit build provides that functionality.  For tracing
# 32 bit applications on ppc and s390 we still have strace32
Obsoletes: strace64

%define strace32_arches ppc s390

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%ifarch %{strace32_arches}
%package -n strace32
Summary: Tracks and displays system calls associated with a running process.
Group: Development/Debuggers

%description -n strace32
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

This package provides the `strace32' program to trace 32-bit processes on
64-bit IBM P and Z series platforms.
%endif

%prep
%setup -q -n strace-%{version}
%patch0 -p1
%patch0002 -p1
%patch0006 -p1
%patch0007 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch2000 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_bindir}/strace-graph

%define copy64 ln
%if 0%{?rhel}
%if 0%{?rhel} < 6
%endif
%define copy64 cp -p
%endif

%ifarch %{strace32_arches}
%{copy64} %{buildroot}%{_bindir}/strace %{buildroot}%{_bindir}/strace32
%endif

%check
make check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog ChangeLog-CVS COPYING NEWS README
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*

%ifarch %{strace32_arches}
%files -n strace32
%defattr(-,root,root)
%{_bindir}/strace32
%endif

%changelog
* Wed Aug  5 2015 DJ Delorie <dj@redhat.com> - 4.10-2
- Add --re-interval to caps tests also

* Fri Jul 17 2015 DJ Delorie <dj@redhat.com> - 4.10-1
- Rebase to fc23's 4.10

* Wed May 21 2014 Jeff Law <law@redhat.com> - 4.8-8
- Import from RHEL 7 and build

