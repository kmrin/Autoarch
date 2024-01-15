"""
Autoarch Public v3.0.2

Changelog:
    > 3.0.0 - Initial release.
    
    > 3.0.1 - Fixed a problem where nvme drives where not accounted for.
    
    > 3.0.2 - Several functions and variables were renamed to make the script more readable.
            - Script now tracks if it made any changes to the user's disk and is able to
              revert those changes if necessary, say if a major error happens.
            - Script now uses the shutil library for file copying, making things safer.
            - 'try' functions are now more widely used to prevent errors from exploding.
            - 'subprocess.Popen' calls have been replaced by 'subprocess.run'.
            - Sintaxes like ifs, ands, ors and formats have been simplified.
            - Script now checks for system type through 'os.path.exists' instead of a clumsy
              os.system(ls ...).read() command.
            - Added a swap partition for Legacy BIOS systems.
            - Improved verbose.
    
    > 3.1.0 - Added the possibility of choosing multiple disks.
"""

# Import libraries
import subprocess
import cpuinfo
import shutil
import time
import os

# Welcome logo
print("""
┌────────────────────────────────────────────────┐
│    _         _             _             _     │
│   / \  _   _| |_ ___      / \   _ __ ___| |__  │
│  / _ \| | | | __/ _ \    / _ \ | '__/ __| '_ \ │
│ / ___ \ |_| | || (_) |  / ___ \| | | (__| | | |│
│/_/   \_\__,_|\__\___/  /_/   \_\_|  \___|_| |_|│
│                                         PUBLIC │
└────────────────────────────────────────────────┘
Version 3.1.0                         Made by rin
    """)

# Set global status for disk manipulation
diskManipulated = False

# Information gathering
def getInfo():
    getInfo.language = input("Choose a language: [Ex.: pt_BR, en...]: ")
    getInfo.hostname = input("Choose a hostname: ")
    getInfo.username = input("Now a username: ")

# Update live env pacman configuration
def pacUpd():
    # Shell commands
    updCache = "pacman -Syy"
    
    # Shutil parameters
    src = "config/pacman.conf"
    dst = "/etc/pacman.conf"
    
    # Execute
    try:
        print(' ')
        shutil.copy(src, dst)
        subprocess.run(updCache, shell=True)
        print("\nPacman live configuration updated.\n")
    except PermissionError:
        print("\nPermission denied to update pacman config.\n")
        cancel()
    except:
        print("\nAn error occurred trying to update pacman.\n")
        cancel()

# Disk setup
def disks():
    # Making sure python doesn't shit it's pants
    disks.dev = "bruh"
    disks.multiRootDev = "bruh"
    
    global diskManipulated
    
    # Ask if it's a multidisk installation
    disks.multi = input("Is this installation going to use multiple disks? [Y / N]: ")
    
    # Multidisk install
    if disks.multi.lower() == "y":
        # Setup
        disks.disk_dict = {}
        disk_mount = {}
        disk_label = {}
        
        # List availiable disks to user
        subprocess.run("lsblk", shell=True)
        
        disks.multiRoot = input("\nWhich disk should be used for root? [Ex.: sda, vda, nvme0n1...]: ")
        disks.disk_amount = int(input('How many extra disks? [Ex.: 1, 3, 6]: '))
        disks.disk_amount += 1
        disk_number = 1

        while disk_number < disks.disk_amount:
            print('')
            disks.disk_dict[disk_number] = input(f"Choose extra disk {disk_number} [Ex.: sda, vda, nvme0n1...]: ")
            disk_mount[disk_number] = input("It's mountpoint? [Ex.: /mnt/home, /mnt/var, /mnt/games...]: ")
            disk_label[disk_number] = input("Now it's label: [Ex.: Data, Cache, Games]: ")
            disk_number += 1

        # Confirmation
        print('')
        print(f"Your root disk is: {disks.multiRoot}")
        print(f"The extra disks selected are: {disks.disk_dict}")
        print(f"These are their mountpoints: {disk_mount}")
        print(f"And you called them: {disk_label}")
        
        correct = input("\nIs the above information correct? [Y / N]: ")
        
        # Aproved
        if correct.lower() == 'y':
            # Verbose
            print("""
                
Understood. The installation will begin in 10 seconds.
During this period, you can abort the installation by pressing 'Ctrl + C'.

WARNING!!! ALL DATA ON THE SELECTED DISK(S) WILL BE LOST!!!
                
                """)

            # Timer loop (waits 10 seconds before proceeding with the installation)
            time_left = 10
            while time_left <= 10:
                print("Time left:", time_left)
                time.sleep(1)
                time_left -= 1
                if time_left == 0:
                    break
            
            # Define main root device
            disks.multiRootDev = f'/dev/{disks.multiRoot}'
            
            # Root device partitions
            if "nvme" in disks.multiRoot:
                disks.part1 = disks.multiRootDev + 'p1'
                disks.part2 = disks.multiRootDev + 'p2'
                disks.part3 = disks.multiRootDev + 'p3'
            else:
                disks.part1 = disks.multiRootDev + '1'
                disks.part2 = disks.multiRootDev + '2'
                disks.part3 = disks.multiRootDev + '3'
            
            # UEFI and Legacy BIOS root device manipulation
            # UEFI
            if os.path.exists("/sys/firmware/efi/efivars"):
                print("\nCreating GPT partition table...")
                subprocess.run(["parted", disks.multiRootDev, "mktable", "gpt", "-s"])
                time.sleep(1)
                
                print("Creating boot partition...")
                subprocess.run(["parted", disks.multiRootDev, "mkpart", "primary", "fat32", "0%", "512MiB", "-s"])
                time.sleep(1)
                
                print("Creating swap partition...")
                subprocess.run(["parted", disks.multiRootDev, "mkpart", "primary", "linux-swap", "512MiB", "8704MiB", "-s"])
                time.sleep(1)
                
                print("Creating root partition...")
                subprocess.run(["parted", disks.multiRootDev, "mkpart", "primary", "btrfs", "8704MiB", "100%", "-s"])
                time.sleep(1)
                
                print("Flagging boot partition as ESP...")
                subprocess.run(["parted", disks.multiRootDev, "set", "1", "esp", "on", "-s"])
                time.sleep(1)
                
                print("\nFormatting boot partition...\n")
                subprocess.run(["mkfs.fat", "-F32", disks.part1])
                time.sleep(1)
                
                print("\nFormatting swap partition...\n")
                subprocess.run(["mkswap", disks.part2])
                time.sleep(1)
                
                print("\nFormatting root partition...\n")
                subprocess.run(["mkfs.btrfs", "-f", "-L", "SYSTEM", disks.part3])
                time.sleep(1)
                
                print("\nMounting FileSystem...")
                subprocess.run(["mount", disks.part3, "/mnt"])
                subprocess.run(["mount", disks.part1, "/mnt/boot", "--mkdir"])
                subprocess.run(["swapon", disks.part2])
                time.sleep(1)
            
            # BIOS
            else:
                print("\nCreating MBR/DOS partition table...")
                subprocess.run(["parted", disks.multiRootDev, "mktable", "msdos", "-s"])
                time.sleep(1)
                
                print("Creating swap partition...")
                subprocess.run(["parted", disks.multiRootDev, "mkpart", "primary", "linux-swap", "0%", "8192MiB", "-s"])
                time.sleep(1)
                
                print("Creating root partition...")
                subprocess.run(["parted", disks.multiRootDev, "mkpart", "primary", "btrfs", "8192MiB", "100%", "-s"])
                time.sleep(1)
                
                print("Formatting swap partition...\n")
                subprocess.run(["mkswap", disks.part1])
                time.sleep(1)
                
                print("\nFormatting root partition...\n")
                subprocess.run(["mkfs.btrfs", "-f", "-L", "SYSTEM", disks.part2])
                time.sleep(1)
                
                print("Flagging root partition as bootable...")
                subprocess.run(["parted", disks.multiRootDev, "set", "1", "boot", "on", "-s"])
                time.sleep(1)
                
                print("\nMounting FileSystem...")
                subprocess.run(["mount", disks.part2, "/mnt"])
                subprocess.run(["swapon", disks.part1])
                time.sleep(1)
            
            # Extra disks
            print("\nPreparing extra disks...\n")
            
            index = 1
            
            for _ in disks.disk_dict:
                current_dev = f"/dev/{disks.disk_dict[index]}"
                
                # NVME sanity check
                if 'nvme' in disks.disk_dict[index]:
                    current_devPart = f'/dev/{disks.disk_dict[index]}p1'
                else:
                    current_devPart = f'/dev/{disks.disk_dict[index]}1'
                    
                # UEFI
                if os.path.exists("/sys/firmware/efi/efivars"):
                    subprocess.run(["parted", current_dev, "mktable", "gpt", "-s"])
                else:
                    subprocess.run(["parted", current_dev, "mktable", "msdos", "-s"])
                
                subprocess.run(["parted", current_dev, "mkpart", "primary", "btrfs", "0%", "100%", "-s"])
                subprocess.run(["mkfs.btrfs", "-f", "-L", disk_label[index], current_devPart])
                subprocess.run(["mount", current_devPart, disk_mount[index], "--mkdir"])
                
                index += 1
            
            time.sleep(1)
            
            # Verbose
            print("\nExtra disks setup complete...")
            
            # Verbose
            print("""
                
FileSystem Ready for install...
                
                """)
            
            # Tell revert that the disk has been manipulated
            diskManipulated = True
            
            # Wait 2 seconds before proceeding to make sure all processes have finished
            time.sleep(2)
        
        # Reproved
        elif correct.lower() == 'n':
            # Re-run
            print("Understood. Try again.\n")
            disks()
        
        # Invalid
        else:
            # Re-run
            print("Understood. Try again.\n")
            disks()
    
    # Single disk install
    elif disks.multi.lower() == 'n':
        # List availiable disks to user
        subprocess.run("lsblk", shell=True)
        
        # Define disk to be used for the install
        disks.selected = input("\nWhich disk should be used? [Ex.: sda, vda, nvme0n1...]: ")
        
        # Confirm user selection
        print("\nThe selected disk is", disks.selected + ".")
        confirm = input("Is the above information correct? [Y / N]: ")
        
        # Approved
        if confirm.lower() == "y":
            # Verbose
            print("""
                
Understood. The installation will begin in 10 seconds.
During this period, you can abort the installation by pressing 'Ctrl + C'.

WARNING!!! ALL DATA ON THE SELECTED DISK(S) WILL BE LOST!!!
                
                """)

            # Timer loop (waits 10 seconds before proceeding with the installation)
            time_left = 10
            while time_left <= 10:
                print("Time left:", time_left)
                time.sleep(1)
                time_left -= 1
                if time_left == 0:
                    break
            
            # Define main device to be manipulated
            disks.dev = f'/dev/{disks.selected}'
            
            # Partitions
            if "nvme" in disks.selected:
                disks.part1 = disks.dev + 'p1'
                disks.part2 = disks.dev + 'p2'
                disks.part3 = disks.dev + 'p3'
            else:
                disks.part1 = disks.dev + '1'
                disks.part2 = disks.dev + '2'
                disks.part3 = disks.dev + '3'
            
            # UEFI and Legacy BIOS disk manipulation
            # UEFI
            if os.path.exists("/sys/firmware/efi/efivars"):
                print("\nCreating GPT partition table...")
                subprocess.run(["parted", disks.dev, "mktable", "gpt", "-s"])
                time.sleep(1)
                
                print("Creating boot partition...")
                subprocess.run(["parted", disks.dev, "mkpart", "primary", "fat32", "0%", "512MiB", "-s"])
                time.sleep(1)
                
                print("Creating swap partition...")
                subprocess.run(["parted", disks.dev, "mkpart", "primary", "linux-swap", "512MiB", "8704MiB", "-s"])
                time.sleep(1)
                
                print("Creating root partition...")
                subprocess.run(["parted", disks.dev, "mkpart", "primary", "btrfs", "8704MiB", "100%", "-s"])
                time.sleep(1)
                
                print("Flagging boot partition as ESP...")
                subprocess.run(["parted", disks.dev, "set", "1", "esp", "on", "-s"])
                time.sleep(1)
                
                print("\nFormatting boot partition...\n")
                subprocess.run(["mkfs.fat", "-F32", disks.part1])
                time.sleep(1)
                
                print("\nFormatting swap partition...\n")
                subprocess.run(["mkswap", disks.part2])
                time.sleep(1)
                
                print("\nFormatting root partition...\n")
                subprocess.run(["mkfs.btrfs", "-f", "-L", "SYSTEM", disks.part3])
                time.sleep(1)
                
                print("\nMounting FileSystem...")
                subprocess.run(["mount", disks.part3, "/mnt"])
                subprocess.run(["mount", disks.part1, "/mnt/boot", "--mkdir"])
                subprocess.run(["swapon", disks.part2])
                time.sleep(1)
                
            # BIOS
            else:
                print("\nCreating MBR/DOS partition table...")
                subprocess.run(["parted", disks.dev, "mktable", "msdos", "-s"])
                time.sleep(1)
                
                print("Creating swap partition...")
                subprocess.run(["parted", disks.dev, "mkpart", "primary", "linux-swap", "0%", "8192MiB", "-s"])
                time.sleep(1)
                
                print("Creating root partition...")
                subprocess.run(["parted", disks.dev, "mkpart", "primary", "btrfs", "8192MiB", "100%", "-s"])
                time.sleep(1)
                
                print("Formatting swap partition...\n")
                subprocess.run(["mkswap", disks.part1])
                time.sleep(1)
                
                print("\nFormatting root partition...\n")
                subprocess.run(["mkfs.btrfs", "-f", "-L", "SYSTEM", disks.part2])
                time.sleep(1)
                
                print("Flagging root partition as bootable...")
                subprocess.run(["parted", disks.dev, "set", "1", "boot", "on", "-s"])
                time.sleep(1)
                
                print("\nMounting FileSystem...")
                subprocess.run(["mount", disks.part2, "/mnt"])
                subprocess.run(["swapon", disks.part1])
                time.sleep(1)
                
            # Verbose
            print("""
                
FileSystem Ready for install...
                
                """)
            
            # Tell revert that the disk has been manipulated
            diskManipulated = True
            
            # Wait 2 seconds before proceeding to make sure all processes have finished
            time.sleep(2)
        
        # Reproved
        elif confirm.lower() == "n":
            # Re-run
            print("Understood. Try again.\n")
            disks()
        
        # Invalid
        else:
            # Re-run
            print("Invalid input. Try again\n")
            disks()
        
    # Invalid
    else:
        print("Invalid input. Try again")
        disks()

# This function will only be used if a major failure happens
def cancel():
    verbose = """

Sorry if any problem happened.
If there's any issue with the script, file a bug report to my GitLab, cheers!
          
              """

    if diskManipulated:
        print("\nReverting changes done to disk...")
        
        if os.path.exists("/sys/firmware/efi/efivars"):
            if disks.multi.lower() == 'y':
                subprocess.run(["umount", "-R", "/mnt"])
                subprocess.run(["swapoff", disks.part2])
                subprocess.run(["parted", disks.multiRootDev, "mktable", "gpt", "-s"])
                
                index = 1
                
                for _ in disks.disk_dict:
                    current_dev = f'/dev/{disks.disk_dict[index]}'
                    subprocess.run(["parted", current_dev, "mktable", "gpt", "-s"])
                    
            elif disks.multi.lower() == 'n':
                subprocess.run(["umount", "-R", "/mnt"])
                subprocess.run(["swapoff", disks.part2])
                subprocess.run(["parted", disks.dev, "mktable", "gpt", "-s"])
            
            print(verbose)
        else:
            if disks.multi.lower() == 'y':
                subprocess.run(["umount", "-R", "/mnt"])
                subprocess.run(["swapoff", disks.part1])
                subprocess.run(["parted", disks.multiRootDev, "mktable", "gpt", "-s"])
                
                index = 1
                
                for _ in disks.disk_dict:
                    current_dev = f'/dev/{disks.disk_dict[index]}'
                    subprocess.run(["parted", current_dev, "mktable", "msdos", "-s"])
                
            elif disks.multi.lower() == 'n':
                subprocess.run(["umount", "-R", "/mnt"])
                subprocess.run(["swapoff", disks.part1])
                subprocess.run(["parted", disks.dev, "mktable", "msdos", "-s"])
            
            print(verbose)
    else:
        print("\nDisks not changed")

    exit()

# Base system install
def baseSys():
    # Commands
    strap = "pacstrap /mnt base base-devel linux-zen linux-zen-headers linux-firmware btrfs-progs dosfstools " \
            "mtools exfatprogs f2fs-tools e2fsprogs jfsutils nilfs-utils reiserfsprogs udftools xfsprogs " \
            "networkmanager network-manager-applet wpa_supplicant wireless_tools dialog nano man-db man-pages " \
            "texinfo pipewire pipewire-pulse pipewire-alsa cups inetutils numlockx pkgfile fish git curl go " \
            "grub efibootmgr os-prober fuse2 go bluez bluez-utils "
    fstab = "genfstab -U /mnt >> /mnt/etc/fstab"
    language_local = "arch-chroot /mnt echo " + getInfo.language + ".UTF-8 UTF-8 " + ">> /mnt/etc/locale.gen"
    language_lang = "arch-chroot /mnt echo LANG=" + getInfo.language + ".UTF-8 " + ">> /mnt/etc/locale.conf"
    hostname = "arch-chroot /mnt echo " + getInfo.hostname + " >> " + "/mnt/etc/hostname"
    username = "arch-chroot /mnt useradd -mG wheel " + getInfo.username
    netman = "arch-chroot /mnt systemctl enable NetworkManager"
    cups = "arch-chroot /mnt systemctl enable cups"
    bluetooth = "arch-chroot /mnt systemctl enable bluetooth"
    rootpass = "arch-chroot /mnt passwd"
    userpass = "arch-chroot /mnt passwd " + getInfo.username
    locale = "arch-chroot /mnt locale-gen"
    libvirtDir = "mkdir /mnt/etc/libvirt"
    
    # Exec
    print("The installation of the system packages will begin shortly...\n")
    time.sleep(2)
    
    print("Installing base system...\n")
    os.system(strap)
    time.sleep(0.5)
    
    print("\nGenerating FileSystem Table...\n")
    os.system(fstab)
    time.sleep(0.5)
    
    print("Editing locale gen file...\n")
    os.system(language_local)
    time.sleep(0.5)
    
    print("Editing locale lang file...\n")
    os.system(language_lang)
    time.sleep(0.5)
    
    print("Setting hostname...\n")
    os.system(hostname)
    time.sleep(0.5)
    
    print("Creating user...\n")
    os.system(username)
    time.sleep(0.5)
    
    print("Making NetworkManager autostart...\n")
    os.system(netman)
    time.sleep(0.5)
    
    print("Making CUPS autostart...\n")
    os.system(cups)
    time.sleep(0.5)
    
    print("Making sure bluetooth works...(if you have it)\n")
    os.system(bluetooth)
    time.sleep(0.5)

    os.system(locale)
    time.sleep(0.5)
    
    print("\nCreating libvirt dir...")
    os.system(libvirtDir)
    time.sleep(0.5)
    
    print("\n# Please set the root password:\n")
    os.system(rootpass)
    time.sleep(0.5)
    
    print("\n# Now the user password please:\n")
    os.system(userpass)
    time.sleep(0.5)
    
    print("\nThanks!\n")
    time.sleep(1.5)
    
    # Check for VM support
    info = cpuinfo.get_cpu_info()
    if 'vmx' in info['flags'] or 'svm' in info['flags']:
        vm = True
    else:
        vm = False
    
    # Check CPU vendor
    output = subprocess.check_output(['lscpu']).decode('UTF-8')
    for line in output.split('\n'):
        if 'Vendor ID:' in line:
            vendor_id = line.split(':')[1].strip()
            break
    if vendor_id == 'AuthenticAMD':
        cpu = 'amd'
    elif vendor_id == 'GenuineIntel':
        cpu = 'intel'
    else:
        print("Unable to determine CPU vendor, falling back to default GRUB config.\n")
        cpu = 0
        time.sleep(2)
    
    # Config files
    configs = [("config/doas.conf", "/mnt/etc/doas.conf"),
                ("config/sudoers", "/mnt/etc/sudoers"),
                ("config/mkinitcpio.conf", "/mnt/etc/mkinitcpio.conf"),
                ("config/pacman.conf", "/mnt/etc/pacman.conf"),
                ("config/libvirt.conf", "/mnt/etc/libvirt/libvirt.conf")]
    
    grub = ["config/grub-default", "/mnt/etc/default/grub",
            "config/grub-amd", "/mnt/etc/default/grub",
            "config/grub-intel", "/mnt/etc/default/grub"]
    
    # Execute
    for src, dst in configs:
        try:
            shutil.copy(src, dst)
        except PermissionError:
            print("\nPermission denied while trying to install config files.")
            cancel()
        except:
            print("\nAn unexpected error occurred.\n")
            cancel()
            
    if vm == str('yes') and cpu == str('amd'):
        src = grub[2]
        dst = grub[3]
        
        try:
            shutil.copy(src, dst)
        except PermissionError:
            print("\nPermission denied while trying to install config files.")
            cancel()
        except:
            print("\nAn unexpected error occurred.\n")
            cancel()
    elif vm == str('yes') and cpu == str('intel'):
        src = grub[4]
        dst = grub[5]
        
        try:
            shutil.copy(src, dst)
        except PermissionError:
            print("\nPermission denied while trying to install config files.")
            cancel()
        except:
            print("\nAn unexpected error occurred.\n")
            cancel()
    else:
        src = grub[0]
        dst = grub[1]
        
        try:
            shutil.copy(src, dst)
        except PermissionError:
            print("\nPermission denied while trying to install config files.")
            cancel()
        except:
            print("\nAn unexpected error occurred.\n")
            cancel()

# GRUB Bootloader installation
def grub():
    # Commands
    uefi_install = "arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchLinux"
    uefi_mkconfig = "arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg"
    bios_install = "arch-chroot /mnt grub-install --target=i386-pc " + disks.dev
    bios_installMulti = "arch-chroot /mnt grub-install --target=i386-pc " + disks.multiRootDev
    bios_mkconfig = "arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg"
    
    # Verbose
    print("Installing GRUB bootloader...\n")
    
    # Check system type and install grub accordingly
    # UEFI
    if os.path.exists("/sys/firmware/efi/efivars"):
        os.system(uefi_install)
        os.system(uefi_mkconfig)
    
    # BIOS
    else:
        if disks.multi.lower() == 'y':
            os.system(bios_installMulti)
            
        elif disks.multi.lower() == 'n':
            os.system(bios_install)
        
        os.system(bios_mkconfig)
    
    # Verbose
    print("""
          
GRUB Bootloader installed. Proceeding...
          
          """)
    
    # Halt
    time.sleep(2)

# Ask user if they would like to have a ready to use desktop environment
def desktop():
    # Commands
    kde_packages = "arch-chroot /mnt pacman -S --noconfirm xorg plasma konsole dolphin sddm kcalc ark " \
                   "kate kcolorchooser kaccounts-providers kaccounts-integration kio-gdrive " \
                   "dolphin-plugins gvfs gvfs-afc gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs " \
                   "gvfs-smb openssl sshfs kconfigwidgets kcoreaddons kdecoration kguiaddons kiconthemes " \
                   "kwindowsystem qt5-declarative qt5-x11extras qt5-tools qt5pas partitionmanager " \
                   "filelight kdialog ksysguard gnome-keyring libgnome-keyring kwalletmanager seahorse "
    kde_services = "arch-chroot /mnt systemctl enable sddm"
    
    gnome_packages = "arch-chroot /mnt pacman -S --noconfirm xorg gdm gnome gnome-extra gnome-tweaks " \
                     "nautilus-image-converter nautilus-sendto nautilus-share seahorse-nautilus file-roller "
    gnome_services = "arch-chroot /mnt systemctl enable gdm"
    
    xfce_packages = "arch-chroot /mnt pacman -S --noconfirm xorg lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings " \
                    "gvfs gvfs-afc gvfs-goa gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs gvfs-smb menumaker " \
                    "mousepad ristretto thunar thunar-archive-plugin thunar-media-tags-plugin xarchiver " \
                    "thunar-volman xfce4 xfce4-goodies xfce4-clipman-plugin xfce4-whiskermenu-plugin " \
                    "xfce4-pulseaudio-plugin accountsservice gtk3 python-cairo python-gobject python-pexpect " \
                    "intltool python-distutils-extra cheese"
    xfce_services = "arch-chroot /mnt systemctl enable lightdm"
    
    pac_refresh = "arch-chroot /mnt pacman -Syy"
    
    # Verbose
    print("Would you like to install a desktop environment?")
    
    # Option
    desktop = input("Type 'n' for none, 'k' for KDE, 'g' for GNOME or 'x' for XFCE: ")
    
    # No desktop
    if desktop == str("N") or desktop == str("n"):
        proceed = input("\nNo desktop environment will be installed. Proceed? [Y / N]: ")
        
        if proceed == str("Y") or proceed == str("y"):
            print("\nUnderstood.")
        elif proceed == str("N") or proceed == str("n"):
            print("\nUnderstood, try again.\n")
            desktop()
        else:
            print("\nInvalid input, try again.\n")
            desktop()
    
    # KDE
    elif desktop == str("K") or desktop == str("k"):
        proceed = input("\nThe KDE desktop environment will be installed. Proceed? [Y / N]: ")
        
        if proceed == str("Y") or proceed == str("y"):
            print("\nUnderstood.\n")
            os.system(pac_refresh)
            os.system(kde_packages)
            os.system(kde_services)
            print("\nThe KDE desktop environment has been installed.")
        elif proceed == str("N") or proceed == str("n"):
            print("\nUnderstood, try again.\n")
            desktop()
        else:
            print("\nInvalid input, try again.\n")
            desktop()
    
    # GNOME
    elif desktop == str("G") or desktop == str("g"):
        proceed = input("\nThe GNOME desktop environment will be installed. Proceed? [Y / N]: ")
        
        if proceed == str("Y") or proceed == str("y"):
            print("\nUnderstood.\n")
            os.system(pac_refresh)
            os.system(gnome_packages)
            os.system(gnome_services)
            print("\nThe GNOME desktop environment has been installed.")
        elif proceed == str("N") or proceed == str("n"):
            print("\nUnderstood, try again.\n")
            desktop()
        else:
            print("\nInvalid input, try again.\n")
            desktop()
    
    # XFCE
    elif desktop == str("X") or desktop == str("x"):
        proceed = input("\nThe XFCE desktop environment will be installed. Proceed? [Y / N]: ")
        
        if proceed == str("Y") or proceed == str("y"):
            print("\nUnderstood.\n")
            os.system(pac_refresh)
            os.system(xfce_packages)
            os.system(xfce_services)
            print("\nThe XFCE desktop environment has been installed.")
        elif proceed == str("N") or proceed == str("n"):
            print("\nUnderstood, try again.\n")
            desktop()
        else:
            print("\nInvalid input, try again.\n")
            desktop()
    
    # Invalid
    else:
        print("\nInvalid input, try again.\n")
        desktop()

# End of operation
def finish():
    if os.path.exists("/sys/firmware/efi/efivars"):
        subprocess.run(["umount", "-R", "/mnt"])
        subprocess.run(["swapoff", disks.part2])
    else:
        subprocess.run(["umount", "-R", "/mnt"])
        subprocess.run(["swapoff", disks.part1])
    
    # Verbose
    print("""

###########################################################################################
My job is done, you can now reboot into your brand new operating system. Have fun Linuxing!
###########################################################################################
          
          """)
    
    # Kill the script
    exit()

###### EXECUTION AREA ######
try:
    # Always in sequence
    getInfo()
    pacUpd()
    disks()
    baseSys()
    grub()
    desktop()
    finish()
except KeyboardInterrupt:
    print("\nScript execution interrupted by user. (Pressed Ctrl+C)\n")
    cancel()

# script made by rin :)
