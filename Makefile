obj-m := nuc_wmi.o

KVERSION := $(shell uname -r)
KDIR := /lib/modules/$(KVERSION)/build
PWD := $(shell pwd)

.PHONY: clean default dkms-add dkms-build dkms-deb dkms-install dkms-rpm dkms-uninstall install

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

dkms-add:
	dkms add --force $(PWD)

dkms-build: dkms-add
	dkms build -m intel-nuc-wmi -v 2.0

dkms-deb: dkms-add
	dkms mkdeb intel-nuc-wmi/2.0 --source-only

dkms-install: dkms-build
	dkms install -m intel-nuc-wmi -v 2.0
	@depmod -a $(KVERSION)

dkms-rpm: dkms-add
	dkms mkrpm intel-nuc-wmi/2.0 --source-only

dkms-status:
	dkms status intel-nuc-wmi/2.0

dkms-uninstall:
	dkms remove -m intel-nuc-wmi -v 2.0 --all
	rm -rf /usr/src/intel-nuc-wmi-2.0/

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	@depmod -a $(KVERSION)
