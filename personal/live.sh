#!/bin/bash

# Autoarch Personal v3.0.7
# LIVE SCRIPT

# Update live env pacman config
cp dotfiles/pacman.conf /etc
pacman -Syu

# Base system install
pacstrap /mnt base base-devel linux-zen linux-zen-headers linux-firmware btrfs-progs dosfstools mtools exfatprogs f2fs-tools e2fsprogs jfsutils nilfs-utils reiserfsprogs xfsprogs networkmanager network-manager-applet wpa_supplicant wireless_tools dialog nano vim sudo doas zip unrar lzip lzop arj unarj man-db man-pages texinfo pipewire pipewire-alsa pipewire-pulse cups inetutils numlockx pkgfile fish git go grub efibootmgr os-prober fuse2 go ntfs-3g neofetch figlet lolcat wget curl bash-completion bluez bluez-utils xdg-utils xdg-user-dirs reflector nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings

# Generate FileSystem Table
genfstab -U /mnt >> /mnt/etc/fstab

# Arrange directories
mkdir /mnt/etc/pacman.d/hooks /mnt/etc/libvirt

# Place config files
cp dotfiles/grub /mnt/etc/default/grub
cp dotfiles/libvirt.conf /mnt/etc/libvirt
cp dotfiles/pacman.conf /mnt/etc/pacman.conf
cp dotfiles/mkinitcpio.conf /mnt/etc/mkinitcpio.conf
cp dotfiles/environment /mnt/etc
cp dotfiles/nvidia.hook /mnt/etc/pacman.d/hooks

# Basic configuration sequence
arch-chroot /mnt ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
arch-chroot /mnt echo "en_US.UTF-8 UTF-8" >> /mnt/etc/locale.gen
arch-chroot /mnt echo "pt_BR.UTF-8 UTF-8" >> /mnt/etc/locale.gen
arch-chroot /mnt echo "LANG=pt_BR.UTF-8" >> /mnt/etc/locale.conf
arch-chroot /mnt echo "KEYMAP=us" >> /mnt/etc/vconsole.conf
arch-chroot /mnt echo "tornado" >> /mnt/etc/hostname
arch-chroot /mnt echo "127.0.0.1 localhost" >> /mnt/etc/hosts
arch-chroot /mnt echo "::1 localhost" >> /mnt/etc/hosts
arch-chroot /mnt echo "127.0.1.1 tornado.localdomain tornado" >> /mnt/etc/hosts
arch-chroot /mnt echo "permit :root" >> /mnt/etc/doas.conf
arch-chroot /mnt echo "permit :wheel" >> /mnt/etc/doas.conf
arch-chroot /mnt echo " " >> /mnt/etc/sudoers
arch-chroot /mnt echo "%wheel ALL=(ALL:ALL) ALL" >> /mnt/etc/sudoers

# Generate locales
arch-chroot /mnt locale-gen

# Add user
arch-chroot /mnt useradd -mG wheel markp

# Change passwords
arch-chroot /mnt passwd markp
arch-chroot /mnt passwd root

# Change shell environment
arch-chroot /mnt chsh -s /usr/bin/fish markp
arch-chroot /mnt chsh -s /bin/fish root

# Update pacman config
arch-chroot /mnt pacman -Syy
arch-chroot /mnt pkgfile --update

# Install the bootloader
arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchLinux --recheck
arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg

# Autostarting servives
arch-chroot /mnt systemctl enable NetworkManager
arch-chroot /mnt systemctl enable bluetooth
arch-chroot /mnt systemctl enable cups

# Regen initramfs
arch-chroot /mnt mkinitcpio -p linux-zen

# Unmount partitions for reboot
umount -R /mnt
swapoff /dev/nvme0n1p6

# Verbose
echo " "
echo "# First script finished, reboot now and run the final script."
echo " "