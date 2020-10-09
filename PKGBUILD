developer="https://indiecomputing.com/"
url="https://github.com/uboslinux/intel_nuc_led"
maintainer=${developer}
pkgname=$(basename $(pwd))
pkgver=0.11
pkgrel=1
pkgdesc='Intel NUC LED Control for Linux'
arch=('x86_64')
license=('GPL3')
_kernelver=5.8.10.arch1-1
_kernelpath=5.8.10-arch1-1
# Note: not the same: hyphen vs dot
depends=("linux=${_kernelver}")
makedepends=(
    "linux-headers=${_kernelver}"
    "python-setuptools"
)
source=(
    "Makefile"
    "nuc_led.c"
)
sha512sums=(
    'SKIP'
    'SKIP'
)

build() {
    # Build kernel module
    cd ${srcdir}
    make KVERSION="$(uname -r)" default
}

package() {
    # Package kernel module
    install -m 0644 -D ${srcdir}/nuc_led.ko -t ${pkgdir}/usr/lib/modules/${_kernelpath}/extramodules/

    install -m 0644 -D ${startdir}/contrib/etc/modprobe.d/nuc_led.conf -t ${pkgdir}/usr/lib/modprobe.d/
    install -m 0644 -D ${startdir}/contrib/etc/modules-load.d/nuc_led.conf -t ${pkgdir}/usr/lib/modules-load.d/

    find "${pkgdir}" -name '*.ko' -exec gzip -n {} +

    # Build and package userspace
    cd ${startdir}/contrib/nuc_wmi
    python setup.py install --root ${pkgdir}
}
