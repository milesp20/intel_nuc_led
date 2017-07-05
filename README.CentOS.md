# Building on CentOS

To build on CentOS:

Install gcc and the kernel development package:

```
sudo yum -y install kernel-devel-`uname -r` gcc
```

Build with make:

```
make
```

and load the module with insmod:

```
sudo insmod nuc_led.ko
```
