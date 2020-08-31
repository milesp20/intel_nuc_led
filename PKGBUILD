developer="https://indiecomputing.com/"
url="https://github.com/uboslinux/intel_nuc_led"
maintainer=${developer}
pkgname=$(basename $(pwd))
pkgver=0.8
pkgrel=1
pkgdesc='Intel NUC LED Control for Linux '
arch=('x86_64')
license=('GPL3')
_kernelver=5.8.5.arch1-1
_kernelpath=5.8.5-arch1-1
# Note: not the same: hyphen vs dot
depends=("linux=${_kernelver}")
makedepends=("linux-headers=${_kernelver}")
source=(
    "Makefile"
    "nuc_led.c"
)
sha512sums=(
    'SKIP'
    'SKIP'
)

build() {
    cd ${srcdir}
    make KVERSION="$(uname -r)" default
}

package() {
    install -m 0644 -D ${srcdir}/nuc_led.ko -t ${pkgdir}/usr/lib/modules/${_kernelpath}/extramodules/

    install -m 0644 -D ${startdir}/contrib/etc/modprobe.d/nuc_led.conf -t ${pkgdir}/usr/lib/modprobe.d/
    install -m 0644 -D ${startdir}/contrib/etc/modules-load.d/nuc_led  -t ${pkgdir}/usr/lib/modules-load.d/

    find "${pkgdir}" -name '*.ko' -exec gzip -n {} +
}
