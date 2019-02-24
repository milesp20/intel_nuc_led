obj-m := nuc_led.o

MOD_VERSION := 2.0
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
	dkms build -m intel-nuc-led -v $(MOD_VERSION)

dkms-deb: dkms-add
	sed -i "s|PACKAGE_VERSION=.*|PACKAGE_VERSION=$(MOD_VERSION)|g" dkms.conf
	dkms mkdeb intel-nuc-led/$(MOD_VERSION) --source-only

dkms-install: dkms-build
	dkms install -m intel-nuc-led -v $(MOD_VERSION)
	@depmod -a $(KVERSION)

dkms-rpm: dkms-add
	sed -i "s|PACKAGE_VERSION=.*|PACKAGE_VERSION=$(MOD_VERSION)|g" dkms.conf
	dkms mkrpm intel-nuc-led/$(MOD_VERSION) --source-only

dkms-status:
	dkms status intel-nuc-led/$(MOD_VERSION)

dkms-uninstall:
	dkms remove -m intel-nuc-led -v $(MOD_VERSION) --all
	rm -rf /usr/src/intel-nuc-led-$(MOD_VERSION)/

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	@depmod -a $(KVERSION)
