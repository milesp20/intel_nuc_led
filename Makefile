obj-m := nuc_led.o

KVERSION := $(shell uname -r)
KDIR := /lib/modules/$(KVERSION)/build
PWD := $(shell pwd)

default:
        $(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
        $(MAKE) -C $(KDIR) M=$(PWD) clean

install:
        $(MAKE) -C $(KDIR) M=$(PWD) modules_install
        @depmod -a $(KVERSION)
