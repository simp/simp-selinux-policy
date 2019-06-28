# simp-selinux-policy

This repository builds and packages SELinux policies suitable for
configuring permissions on SIMP provided server components.

## Installation

If not using an RPM installation, you can perform the following actions to
install the SELinux policy manually:

### Environment Prep

* ``yum install selinux-policy-devel``

### Policy Build

* ``sh sbin/set_simp_selinux_policy build``

### Policy Installation

* ``sh sbin/set_simp_selinux_policy install``

## Removal

To remove the SELinux policy:

* ``sh sbin/set_simp_selinux_policy remove``
