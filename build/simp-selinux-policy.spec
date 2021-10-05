# policycoreutils_version and selinux_policy_version are specifically set
# to the *earliest* version of these packages present in these major releases.
#
# This is required since SELinux policies are forward compatible during a major
# release but not necessarily backwards compatible and we want to ensure
# maximum package compatibility.
#
# Use environment variable SIMP_ENV_NO_SELINUX_DEPS to ignore this
# and use the latest.  (This is good when building test ISOs that
# from a local environment, instead of a docker build, where a later
# version of selinux is installed.)
%define ignore_selinux_reqs %{getenv:SIMP_ENV_NO_SELINUX_DEPS}

# Only run the following if the environment variable is *not* defined
%if "%{ignore_selinux_reqs}" == ""
  %if 0%{?rhel} == 6 || 0%{?rhel} == 7
    %if 0%{?rhel} == 6
      %global policycoreutils_version 2.0.83
      %global selinux_policy_version 3.7.19
    %endif

    %if 0%{?rhel} == 7
      %global policycoreutils_version 2.2.5
      %global selinux_policy_version 3.12.1
    %endif

    %if 0%{?rhel} == 8
      %global policycoreutils_version 2.8-16.1
      %global selinux_policy_version 3.14.1
    %endif
  %endif
%endif

%global selinux_variants targeted

%define selinux_policy_short simp
%define selinux_policy %{selinux_policy_short}.pp


Summary: SIMP SELinux Policies
Name: simp-selinux-policy
Version: 1.1.1
Release: 1%{?dist}
License: Apache License 2.0
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if 0%{?rhel} > 7
Recommends: libselinux-utils
Recommends: policycoreutils
%else
Requires: libselinux-utils
Requires: policycoreutils
%endif
Requires(post): glibc-common
Requires(post): libsemanage
%if 0%{?selinux_policy_version:1}
Requires(post): selinux-policy >= %{selinux_policy_version}
Requires(post): selinux-policy-targeted >= %{selinux_policy_version}
%else
Requires(post): selinux-policy
Requires(post): selinux-policy-targeted
%endif
Requires(post,postun): policycoreutils
BuildRequires: selinux-policy-targeted
%if 0%{?selinux_policy_version:1}
BuildRequires: policycoreutils == %{policycoreutils_version}
BuildRequires: selinux-policy == %{selinux_policy_version}
BuildRequires: selinux-policy-devel == %{selinux_policy_version}
  %if 0%{?rhel} == 7
BuildRequires: policycoreutils-python == %{policycoreutils_version}
  %endif
  %if 0%{?rhel} > 6
BuildRequires: policycoreutils-devel == %{policycoreutils_version}
  %endif
%else
BuildRequires: policycoreutils
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
  %if 0%{?rhel} == 7
BuildRequires: policycoreutils-python
  %endif
  %if 0%{?rhel} > 6
BuildRequires: policycoreutils-devel
BuildRequires: selinux-policy-targeted
  %endif
%endif

Buildarch: noarch

%description

Provides SELinux policies suitable for configuring permissions on SIMP provided
server components.

%prep
%setup -q

%build
cd build/selinux
  make -f %{_datadir}/selinux/devel/Makefile
cd -

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/simp
cp -r sbin %{buildroot}/%{_datadir}/simp

cd build/selinux
  install -p -m 644 -D %{selinux_policy} %{buildroot}/%{_datadir}/selinux/packages/%{selinux_policy}
cd -

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0640,root,root,0750)
%{_datadir}/selinux/*/%{selinux_policy}
%attr(0750,-,-) %{_datadir}/simp/sbin/set_simp_selinux_policy

%post
%{_datadir}/simp/sbin/set_simp_selinux_policy install

%postun
if [ $1 -eq 0 ]; then
  %{_datadir}/simp/sbin/set_simp_selinux_policy remove
fi

%changelog
* Tue Oct 05 2021 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.1.1-1
- Ensure that dependencies are not removed on package uninstall

* Thu Oct 08 2020 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.1.0-1
- Added EL8 support
- Changed the base release to 1 to align with the Fedora packaging guidelines

* Tue Apr 30 2019 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0.0-0
- Creation of a new simp-selinux-policy package.  Policies were
  originally packaged in the simp-environment package.
