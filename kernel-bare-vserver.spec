#
# Conditional build:
%bcond_without	source		# don't build kernel-bare-vserver-source package
%bcond_without	pcmcia		# don't build pcmcia
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	pae		# build PAE (HIGHMEM64G) support on uniprocessor

%{?debug:%define with_verbose 1}

%define		have_drm	1
%define		have_oss	1
%define		have_sound	1
%define		have_isa	1

%define		_basever		2.6.25
%define		_postver		.13
%define		_rel			1

%define		_enable_debug_packages			0

%define		alt_kernel	bare-vserver%{?with_pae:-pae}

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}
# _localversion is just that without version for "> localversion"
%define		_localversion %{_rel}
%define		kernel_release %{version}-%{alt_kernel}-%{_localversion}

Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(et.UTF-8):	Linuxi kernel (ehk operatsioonisüsteemi tuum)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{alt_kernel}
Version:	%{_basever}%{_postver}
Release:	%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	db95a49a656a3247d4995a797d333153
%if "%{_postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	39578e23ad899c2a418c7ca89b4248bb
%endif

Source2:	kernel-bare-vserver-autoconf.h
Source3:	kernel-bare-vserver-config.h
Source4:	kernel-bare-vserver-module-build.pl

Source10:	kernel-bare-vserver-x86.config
Source11:	kernel-bare-vserver-x86_64.config

# from http://vserver.13thfloor.at/Experimental/
Patch100:	linux-2.6-vs2.3.patch
# minimal grsecurity for vserver patched kernel
Patch101:	linux-2.6-grsec-vs-minimal.patch
# from squashfs: http://dl.sourceforge.net/sourceforge/squashfs/squashfs3.3.tar.gz
Patch102:	linux-2.6.25-squashfs.patch

URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.14.90.0.7
BuildRequires:	/sbin/depmod
BuildRequires:	gcc >= 5:3.2
# for hostname command
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.217
Autoreqprov:	no
Requires(post):	coreutils
Requires(post):	geninitrd >= 2.57
Requires(post):	module-init-tools >= 0.9.9
Requires:	/sbin/depmod
Requires:	coreutils
Requires:	geninitrd >= 2.57
Requires:	module-init-tools >= 0.9.9
Obsoletes:	kernel-misc-fuse
Obsoletes:	kernel-modules
Obsoletes:	kernel-net-hostap
Obsoletes:	kernel-net-ieee80211
Obsoletes:	kernel-net-ipp2p
Obsoletes:	kernel-smp
Conflicts:	e2fsprogs < 1.29
Conflicts:	isdn4k-utils < 3.1pre1
Conflicts:	jfsutils < 1.1.3
Conflicts:	module-init-tools < 0.9.10
Conflicts:	nfs-utils < 1.0.5
Conflicts:	oprofile < 0.9
Conflicts:	ppp < 1:2.4.0
Conflicts:	procps < 3.2.0
Conflicts:	quota-tools < 3.09
Conflicts:	reiserfsprogs < 3.6.3
Conflicts:	udev < 1:071
Conflicts:	util-linux < 2.10o
Conflicts:	xfsprogs < 2.6.0
%if %{with pae}
ExclusiveArch:  %{ix86}
ExcludeArch:	i386 i486 i586
%else
ExclusiveArch:	%{ix86} %{x8664}
%endif
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86} %{x8664}
%define		target_arch_dir		x86
%endif
%ifnarch %{ix86} %{x8664}
%define		target_arch_dir		%{_target_base_arch}
%endif

%ifarch %{ix86}
%define		kernel_config		x86
%else
%define		kernel_config		%{_target_base_arch}
%endif

%define		defconfig	arch/%{target_arch_dir}/defconfig

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	.*%{_kernelsrcdir}/.*
%define		_noautochrpath	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

%define		_kernelsrcdir	/usr/src/linux-%{version}-%{alt_kernel}

%if "%{_target_base_arch}" != "%{_arch}"
	%define CrossOpts ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	CrossOpts ARCH=%{_target_base_arch} CC="%{__cc}"
	%define	DepMod /sbin/depmod
	%endif

%else
	%define CrossOpts ARCH=%{_target_base_arch} CC="%{__cc}"
	%define	DepMod /sbin/depmod
%endif

%define Features %(echo "%{__features}" | sed '/^$/d')

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%{Features}

%description -l de.UTF-8
Das Kernel-Paket enthält den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist für grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Prozeß-Management, Geräte Ein- und Ausgaben, usw.

%{Features}

%description -l fr.UTF-8
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un système d'exploitation Linux. Le noyau traite les
fonctions basiques d'un système d'exploitation: allocation mémoire,
allocation de process, entrée/sortie de peripheriques, etc.

%{Features}

%description -l pl.UTF-8
Pakiet zawiera jądro Linuksa niezbędne do prawidłowego działania
Twojego komputera. Zawiera w sobie sterowniki do sprzętu znajdującego
się w komputerze, takiego jak sterowniki dysków itp.

%{Features}

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de.UTF-8):	vmlinux - dekompressiertes Kernel Bild
Summary(pl.UTF-8):	vmlinux - rozpakowany obraz jądra
Group:		Base/Kernel
Obsoletes:	kernel-smp-vmlinux

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de.UTF-8
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl.UTF-8
vmlinux - rozpakowany obraz jądra.

%package drm
Summary:	DRM kernel modules
Summary(de.UTF-8):	DRM Kernel Treiber
Summary(pl.UTF-8):	Sterowniki DRM
Group:		Base/Kernel
Requires(postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	kernel-smp-drm
Autoreqprov:	no

%description drm
DRM kernel modules.

%description drm -l de.UTF-8
DRM Kernel Treiber.

%description drm -l pl.UTF-8
Sterowniki DRM.

%package pcmcia
Summary:	PCMCIA modules
Summary(de.UTF-8):	PCMCIA Module
Summary(pl.UTF-8):	Moduły PCMCIA
Group:		Base/Kernel
Requires(postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	kernel-smp-pcmcia
Conflicts:	pcmcia-cs < 3.1.21
Conflicts:	pcmciautils < 004
Autoreqprov:	no

%description pcmcia
PCMCIA modules.

%description pcmcia -l de.UTF-8
PCMCIA Module.

%description pcmcia -l pl.UTF-8
Moduły PCMCIA.

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de.UTF-8):	ALSA Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku ALSA
Group:		Base/Kernel
Requires(postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	kernel-smp-sound-alsa
Autoreqprov:	no

%description sound-alsa
ALSA (Advanced Linux Sound Architecture) sound drivers.

%description sound-alsa -l de.UTF-8
ALSA (Advanced Linux Sound Architecture) Sound-Treiber.

%description sound-alsa -l pl.UTF-8
Sterowniki dźwięku ALSA (Advanced Linux Sound Architecture).

%package sound-oss
Summary:	OSS kernel modules
Summary(de.UTF-8):	OSS Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku OSS
Group:		Base/Kernel
Requires(postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	kernel-smp-sound-oss
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de.UTF-8
OSS (Open Sound System) Treiber.

%description sound-oss -l pl.UTF-8
Sterowniki dźwięku OSS (Open Sound System).

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Autoreqprov:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten, die beim rekompilieren des
Kernels oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Conflicts:	rpmbuild(macros) < 1.321
Autoreqprov:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package source
Summary:	Kernel source tree
Summary(de.UTF-8):	Der Kernel Quelltext
Summary(pl.UTF-8):	Kod źródłowy jądra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. You can build a custom
kernel that is better tuned to your particular hardware.

%description source -l de.UTF-8
Das Kernel-Source-Paket enthält den source code (C/Assembler-Code) des
Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zurückgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien können auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr.UTF-8
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont nécessaires pour compiler la plupart des
programmes C, car il dépend de constantes définies dans le code
source. Les sources peuvent être aussi utilisée pour compiler un noyau
personnalisé pour avoir de meilleures performances sur des matériels
particuliers.

%description source -l pl.UTF-8
Pakiet zawiera kod źródłowy jądra systemu.

%package doc
Summary:	Kernel documentation
Summary(de.UTF-8):	Kernel Dokumentation
Summary(pl.UTF-8):	Dokumentacja do jądra Linuksa
Group:		Documentation
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
/usr/src/linux/Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
/usr/src/linux/Documentation.

%prep
%setup -q -n linux-%{_basever}

%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | patch -p1 -s
%endif

%patch100 -p1
%patch101 -p1
%patch102 -p1

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}-%{alt_kernel}#g' Makefile

# on sparc this line causes CONFIG_INPUT=m (instead of =y), thus breaking build
sed -i -e '/select INPUT/d' net/bluetooth/hidp/Kconfig

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%build
TuneUpConfigForIX86 () {
	set -x
%ifarch %{ix86}
	pae=
	[ "$2" = "yes" ] && pae=yes
	%if %{with pae}
	pae=yes
	%endif
	%ifnarch i386
	sed -i 's:CONFIG_M386=y:# CONFIG_M386 is not set:' $1
	%endif
	%ifarch i486
	sed -i 's:# CONFIG_M486 is not set:CONFIG_M486=y:' $1
	%endif
	%ifarch i586
	sed -i 's:# CONFIG_M586 is not set:CONFIG_M586=y:' $1
	%endif
	%ifarch i686
	sed -i 's:# CONFIG_M686 is not set:CONFIG_M686=y:' $1
	%endif
	%ifarch pentium3
	sed -i 's:# CONFIG_MPENTIUMIII is not set:CONFIG_MPENTIUMIII=y:' $1
	%endif
	%ifarch pentium4
	sed -i 's:# CONFIG_MPENTIUM4 is not set:CONFIG_MPENTIUM4=y:' $1
	%endif
	%ifarch athlon
	sed -i 's:# CONFIG_MK7 is not set:CONFIG_MK7=y:' $1
	%endif
	%ifarch i686 athlon pentium3 pentium4
	if [ "$pae" = "yes" ]; then
		sed -i "s:CONFIG_HIGHMEM4G=y:# CONFIG_HIGHMEM4G is not set:" $1
		sed -i "s:# CONFIG_HIGHMEM64G is not set:CONFIG_HIGHMEM64G=y\nCONFIG_X86_PAE=y:" $1
	fi
	sed -i 's:CONFIG_MATH_EMULATION=y:# CONFIG_MATH_EMULATION is not set:' $1
	%endif
	return 0
%endif
}

BuildConfig() {
	%{?debug:set -x}
	# is this a special kernel we want to build?
	Config="%{kernel_config}"
	KernelVer=%{kernel_release}
	echo "Building config file using $Config.conf..."
	cat $RPM_SOURCE_DIR/kernel-bare-vserver-$Config.config > %{defconfig}
	TuneUpConfigForIX86 %{defconfig}

%{?debug:sed -i "s:# CONFIG_DEBUG_SLAB is not set:CONFIG_DEBUG_SLAB=y:" %{defconfig}}
%{?debug:sed -i "s:# CONFIG_DEBUG_PREEMPT is not set:CONFIG_DEBUG_PREEMPT=y:" %{defconfig}}
%{?debug:sed -i "s:# CONFIG_RT_DEADLOCK_DETECT is not set:CONFIG_RT_DEADLOCK_DETECT=y:" %{defconfig}}

}

BuildKernel() {
	%{?debug:set -x}
	echo "Building kernel $1 ..."
	%{__make} %CrossOpts mrproper \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	ln -sf %{defconfig} .config

	%{__make} %CrossOpts clean \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	%{__make} %CrossOpts include/linux/version.h \
		%{?with_verbose:V=1}

	%{__make} %CrossOpts scripts/mkcompile_h \
		%{?with_verbose:V=1}

	%{__make} %CrossOpts \
		%{?with_verbose:V=1}
}

PreInstallKernel() {
	Config="%{kernel_config}"
	KernelVer=%{kernel_release}

	mkdir -p $KERNEL_INSTALL_DIR/boot
	install System.map $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer
%ifarch %{ix86} %{x8664}
	install arch/x86/boot/bzImage $KERNEL_INSTALL_DIR/boot/vmlinuz-$KernelVer
	install vmlinux $KERNEL_INSTALL_DIR/boot/vmlinux-$KernelVer
%endif

	%{__make} %CrossOpts modules_install \
		%{?with_verbose:V=1} \
		DEPMOD=%DepMod \
		INSTALL_MOD_PATH=$KERNEL_INSTALL_DIR \
		KERNELRELEASE=$KernelVer

	# You'd probabelly want to make it somewhat different
	install -d $KERNEL_INSTALL_DIR%{_kernelsrcdir}
	install Module.symvers $KERNEL_INSTALL_DIR%{_kernelsrcdir}/Module.symvers-dist

	echo "CHECKING DEPENDENCIES FOR KERNEL MODULES"
	if [ %DepMod = /sbin/depmod ]; then
		/sbin/depmod --basedir $KERNEL_INSTALL_DIR -ae -F $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer -r $KernelVer || :
	fi
	touch $KERNEL_INSTALL_DIR/lib/modules/$KernelVer/modules.dep
	echo "KERNEL RELEASE $KernelVer DONE"
}

KERNEL_BUILD_DIR=`pwd`
echo "-%{_localversion}" > localversion

KERNEL_INSTALL_DIR="$KERNEL_BUILD_DIR/build-done/kernel"
rm -rf $KERNEL_INSTALL_DIR
BuildConfig
ln -sf %{defconfig} .config
install -d $KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux
rm -f include/linux/autoconf.h
%{__make} %CrossOpts include/linux/autoconf.h
install include/linux/autoconf.h \
	$KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux/autoconf-dist.h
install .config \
	$KERNEL_INSTALL_DIR%{_kernelsrcdir}/config-dist
BuildKernel
PreInstallKernel

%{__make} %CrossOpts include/linux/utsrelease.h
cp include/linux/utsrelease.h{,.save}
cp include/linux/version.h{,.save}
cp scripts/mkcompile_h{,.save}

%install
rm -rf $RPM_BUILD_ROOT
umask 022

export DEPMOD=%DepMod

install -d $RPM_BUILD_ROOT%{_kernelsrcdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi

KERNEL_BUILD_DIR=`pwd`

cp -a$l $KERNEL_BUILD_DIR/build-done/kernel/* $RPM_BUILD_ROOT

if [ -e  $RPM_BUILD_ROOT/lib/modules/%{kernel_release} ] ; then
	rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/build
	ln -sf %{_kernelsrcdir} $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/build
	install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{cluster,misc}
fi

find . -maxdepth 1 ! -name "build-done" ! -name "." -exec cp -a$l "{}" "$RPM_BUILD_ROOT%{_kernelsrcdir}/" ";"

cd $RPM_BUILD_ROOT%{_kernelsrcdir}

%{__make} %CrossOpts mrproper archclean \
	RCS_FIND_IGNORE='-name build-done -prune -o'

if [ -e $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/include/linux/autoconf-dist.h ]; then
	install $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/include/linux/autoconf-dist.h \
		$RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux
	install	$KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/config-dist \
		$RPM_BUILD_ROOT%{_kernelsrcdir}
fi

cp -Rdp$l $KERNEL_BUILD_DIR/include/linux/* \
	$RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux

%{__make} %CrossOpts mrproper
mv -f include/linux/utsrelease.h.save $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/utsrelease.h
cp include/linux/version.h{.save,}
cp scripts/mkcompile_h{.save,}
rm -rf include/linux/version.h.save
rm -rf scripts/mkcompile_h.save
install %{SOURCE2} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/autoconf.h
install %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h

# collect module-build files and directories
perl %{SOURCE4} %{_kernelsrcdir} $KERNEL_BUILD_DIR

# ghosted initrd
touch $RPM_BUILD_ROOT%{initrd_dir}/initrd-%{kernel_release}.gz

# rpm obeys filelinkto checks for ghosted symlinks, convert to files
rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}

# remove unnecessary dir with dead symlink
rm -rf $RPM_BUILD_ROOT/arch/i386

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz-%{alt_kernel}
mv -f /boot/System.map-%{alt_kernel} /boot/System.map-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf System.map-%{kernel_release} /boot/System.map-%{alt_kernel}

%depmod %{kernel_release}

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{kernel_release}.gz --install %{kernel_release} --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinux-%{kernel_release} /boot/vmlinux-%{alt_kernel}

%post drm
%depmod %{kernel_release}

%postun drm
%depmod %{kernel_release}

%post pcmcia
%depmod %{kernel_release}

%postun pcmcia
%depmod %{kernel_release}

%post sound-alsa
%depmod %{kernel_release}

%postun sound-alsa
%depmod %{kernel_release}

%post sound-oss
%depmod %{kernel_release}

%postun sound-oss
%depmod %{kernel_release}

%post headers
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux-%{alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux-%{alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux-%{alt_kernel})" = "linux-%{version}-%{alt_kernel}" ]; then
			rm -f %{_prefix}/src/linux-%{alt_kernel}
		fi
	fi
fi

%triggerin module-build -- %{name} = %{epoch}:%{version}-%{release}
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/build
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/source

%triggerun module-build -- %{name} = %{epoch}:%{version}-%{release}
if [ "$1" = 0 ]; then
	rm -f /lib/modules/%{kernel_release}/{build,source}
fi

%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{kernel_release}
/boot/System.map-%{kernel_release}
%ghost %{initrd_dir}/initrd-%{kernel_release}.gz
%dir /lib/modules/%{kernel_release}
%dir /lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/kernel/arch
/lib/modules/%{kernel_release}/kernel/crypto
/lib/modules/%{kernel_release}/kernel/drivers
%if %{have_drm}
%exclude /lib/modules/%{kernel_release}/kernel/drivers/char/drm
%endif
/lib/modules/%{kernel_release}/kernel/fs

# this directory will be removed after disabling rcutorture mod. in 2.6.20.
/lib/modules/%{kernel_release}/kernel/kernel

/lib/modules/%{kernel_release}/kernel/lib
/lib/modules/%{kernel_release}/kernel/net
%if %{have_sound}
%dir /lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/sound/ac97_bus.ko*
/lib/modules/%{kernel_release}/kernel/sound/sound*.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/cx88/cx88-alsa.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/em28xx/em28xx-alsa.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/saa7134/saa7134-alsa.ko*
%endif
%dir /lib/modules/%{kernel_release}/misc
%if %{with pcmcia}
%dir /lib/modules/%{kernel_release}/kernel/drivers/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/pcmcia/pcmcia*ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia/[!p]*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia/pd6729.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/ata/pata_pcmcia.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/usb/gadget/g_midi.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/b43
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/libertas/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
%endif
%ghost /lib/modules/%{kernel_release}/modules.*
# symlinks pointing to kernelsrcdir
%ghost /lib/modules/%{kernel_release}/build
%ghost /lib/modules/%{kernel_release}/source
%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}

%if %{have_drm}
%files drm
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/char/drm
%endif

%if %{with pcmcia}
%files pcmcia
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/pcmcia/*ko*
/lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia/pcmcia*ko*
/lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{kernel_release}/kernel/drivers/ata/pata_pcmcia.ko*
/lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/b43
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/libertas/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
%endif

%if %{have_sound}
%files sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound
%exclude %dir /lib/modules/%{kernel_release}/kernel/sound
%exclude /lib/modules/%{kernel_release}/kernel/sound/ac97_bus.ko*
%exclude /lib/modules/%{kernel_release}/kernel/sound/sound*.ko*
%if %{have_oss}
%exclude /lib/modules/%{kernel_release}/kernel/sound/oss
%endif
/lib/modules/%{kernel_release}/kernel/drivers/usb/gadget/g_midi.ko*
/lib/modules/%{kernel_release}/kernel/drivers/media/video/cx88/cx88-alsa.ko*
/lib/modules/%{kernel_release}/kernel/drivers/media/video/em28xx/em28xx-alsa.ko*
/lib/modules/%{kernel_release}/kernel/drivers/media/video/saa7134/saa7134-alsa.ko*

%if %{have_oss}
%files sound-oss
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound/oss
%endif
%endif

%files headers
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/include
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist

%files module-build -f aux_files
%defattr(644,root,root,755)
# symlinks pointint to kernelsrcdir
%dir /lib/modules/%{kernel_release}
/lib/modules/%{kernel_release}/build
%{_kernelsrcdir}/Kbuild
%{_kernelsrcdir}/localversion
%{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%{_kernelsrcdir}/arch/*/kernel/sigframe*.h
%{_kernelsrcdir}/drivers/lguest/lg.h
%dir %{_kernelsrcdir}/scripts
%dir %{_kernelsrcdir}/scripts/kconfig
%{_kernelsrcdir}/scripts/Kbuild.include
%{_kernelsrcdir}/scripts/Makefile*
%{_kernelsrcdir}/scripts/basic
%{_kernelsrcdir}/scripts/mkmakefile
%{_kernelsrcdir}/scripts/mod
%{_kernelsrcdir}/scripts/setlocalversion
%{_kernelsrcdir}/scripts/*.c
%{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/scripts/kconfig/*
%{_kernelsrcdir}/scripts/mkcompile_h

%files doc
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/Documentation

%if %{with source}
%files source -f aux_files_exc
%defattr(644,root,root,755)
%{_kernelsrcdir}/arch/*/[!Mk]*
%{_kernelsrcdir}/arch/*/kernel/[!M]*
%{_kernelsrcdir}/arch/x86/kvm
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%exclude %{_kernelsrcdir}/arch/*/kernel/sigframe*.h
%exclude %{_kernelsrcdir}/drivers/lguest/lg.h
%{_kernelsrcdir}/block
%{_kernelsrcdir}/crypto
%{_kernelsrcdir}/drivers
%{_kernelsrcdir}/fs
%{_kernelsrcdir}/grsecurity
%{_kernelsrcdir}/init
%{_kernelsrcdir}/ipc
%{_kernelsrcdir}/kernel
%{_kernelsrcdir}/lib
%{_kernelsrcdir}/mm
%{_kernelsrcdir}/net
%{_kernelsrcdir}/virt
%{_kernelsrcdir}/scripts/*
%exclude %{_kernelsrcdir}/scripts/Kbuild.include
%exclude %{_kernelsrcdir}/scripts/Makefile*
%exclude %{_kernelsrcdir}/scripts/basic
%exclude %{_kernelsrcdir}/scripts/kconfig
%exclude %{_kernelsrcdir}/scripts/mkmakefile
%exclude %{_kernelsrcdir}/scripts/mod
%exclude %{_kernelsrcdir}/scripts/setlocalversion
%exclude %{_kernelsrcdir}/scripts/*.c
%exclude %{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/sound
%{_kernelsrcdir}/security
%{_kernelsrcdir}/usr
%{_kernelsrcdir}/COPYING
%{_kernelsrcdir}/CREDITS
%{_kernelsrcdir}/MAINTAINERS
%{_kernelsrcdir}/README
%{_kernelsrcdir}/REPORTING-BUGS
%{_kernelsrcdir}/.mailmap
%endif
