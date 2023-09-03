#!/bin/bash

# Autoarch Personal v3.0.7
# FINAL SCRIPT

# Install personal packages
sudo pacman -S --needed chromium firefox qbittorrent discord telegram-desktop audacious audacity mpv vlc obs-studio avidemux-qt kdenlive gimp krita kcalc ark kate plasma konsole dolphin sddm kvantum-qt5 kcolorchooser kaccounts-providers kaccounts-integration kio-gdrive dolphin-plugins gvfs gvfs-afc gvfs-goa gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs gvfs-smb openssl sshfs cmake libx11 libxrandr libxnvctrl dotnet-sdk-6.0 guvcview-qt gwenview android-file-transfer android-tools lutris steam steam-native-runtime gamemode xf86-input-wacom vulkan-icd-loader lib32-vulkan-icd-loader vdpauinfo mesa-vdpau libvdpau-va-gl libvdpau libva-vdpau-driver lib32-mesa-vdpau lib32-libvdpau lib32-libva-vdpau-driver gstreamer-vaapi libva-utils libva-mesa-driver lib32-libva-mesa-driver easyeffects gst-plugin-pipewire lib32-pipewire terminus-font ttf-bitstream-vera ttf-croscore ttf-dejavu ttf-droid gnu-free-fonts ttf-ibm-plex ttf-liberation ttf-linux-libertine noto-fonts ttf-roboto tex-gyre-fonts ttf-ubuntu-font-family ttf-anonymous-pro ttf-cascadia-code ttf-fantasque-sans-mono otf-fantasque-sans-mono ttf-fira-mono otf-fira-mono ttf-fira-code ttf-hack otf-hermit ttf-inconsolata ttc-iosevka ttf-jetbrains-mono ttf-monofur adobe-source-code-pro-fonts cantarell-fonts inter-font ttf-opensans adobe-source-sans-fonts gentium-plus-font ttf-junicode noto-fonts-cjk ttf-khmer ttf-tibetan-machine noto-fonts-emoji ttf-joypixels texlive-core texlive-fontsextra otf-latin-modern otf-latinmodern-math unrar unarchiver p7zip wine-staging giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libxinerama libgcrypt lib32-libgcrypt ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs xorg atomicparsley python-pycryptodome meson ninja samba jre-openjdk flameshot ksysguard mlocate vim qemu virt-manager virt-viewer dnsmasq vde2 bridge-utils openbsd-netcat ebtables iptables-nft numlockx neofetch catimg chafa youtube-dl bash-completion fwupd gnome-keyring libgnome-keyring kwalletmanager seahorse gcc-libs libnatpmp miniupnpc rust zerotier-one sassc htop btop strace python-secretstorage python-gnupg gparted ntfs-3g gpart partitionmanager fatresize filelight kdialog winetricks libxss nss cups libnotify libwnck3 python-gobject python-pyxdg python-setuptools dbus gcc-libs glew glfw-x11 glslang lib32-dbus lib32-libglvnd nlohmann-json python-mako spdlog vulkan-headers lib32-gcc-libs lib32-libx11 qt5pas glxgears vulkan-tools cairo desktop-file-utils hicolor-icon-theme libappimage libbsd libxpm qt5-base shared-mime-info boost gtest qt5-tools curl gst-plugins-ugly gstreamer nspr libsecret libappindicator-gtk3 python-pypubsub python-wxpython xdg-utils ffmpeg fzf pacman-contrib extra-cmake-modules kconfigwidgets kcoreaddons kdecoration kguiaddons kiconthemes kwindowsystem qt5-declarative qt5-x11extras pyside6 python-requests qt6-tools python-build python-installer python-wheel imagemagick unzip lib32-gcc-libs lib32-libxext python-cachetools python-pycryptodomex python-six python-google-api-python-client python-mock python-protobuf python-pytest-cov python-vcrpy python-yaml python-gevent python-nose python-coverage nodejs jq npm go ttf-carlito pavucontrol cheese vkd3d lib32-vkd3d vulkan-mesa-layers lib32-vulkan-mesa-layers vulkan-validation-layers lib32-vulkan-validation-layers vulkan-extra-layers xf86-video-amdgpu ocl-icd lib32-ocl-icd amdvlk lib32-amdvlk lib32-vkd3d lib32-vulkan-icd-loader lib32-vulkan-mesa-layers lib32-vulkan-radeon lib32-vulkan-validation-layers vkd3d vulkan-extra-layers vulkan-extra-tools vulkan-headers vulkan-icd-loader vulkan-mesa-layers vulkan-radeon vulkan-tools vulkan-validation-layers ocl-icd lib32-ocl-icd cdemu-client cdemu-daemon bitwarden libreoffice-fresh libreoffice-fresh-pt-br kalarm gnome-clocks
sudo pacman -R --noconfirm discover

# Generate home directories
cd ~
mkdir Documentos "Arquivos de configuração" Backups Capturas Discos Drivers Estudos "Entradas de desktop" Firmwares Jogos Mods Pacotes Patches "Personalização" Projetos Random Saves Scripts Servidores Soundboard Temp Torrents VMs

# Generate home subdirectories
mkdir ~/Documentos/ASCII ~/Capturas/Flameshot ~/Capturas/Steam ~/Capturas/OBS ~/Jogos/steam ~/Projetos/DaVinci ~/Projetos/Python ~/Projetos/GIMP ~/Projetos/OBS ~/.local/bin ~/.local/share/applications
mkdir -p ~/.config/obs-studio/plugins/nvfbc/bin/64bit

# Copy repository files to home
cp -r ~/Git/autoarch/personal/dotfiles/* ~/"Arquivos de configuração"
cp ~/Git/autoarch/personal/ascii/* ~/Documentos/ASCII

# Git hell
cd ~/Git
git clone https://aur.archlinux.org/yay-bin.git
git clone https://github.com/ishitatsuyuki/LatencyFlex.git
git clone https://github.com/noisetorch/NoiseTorch.git
git clone https://github.com/Keylase/nvidia-patch.git
git clone https://gitlab.com/fzwoch/obs-nvfbc.git
mkdir ~/Git/NoiseTorch/build
mkdir ~/Git/LatencyFlex/build

# Build and install yay
cd ~/Git/yay-bin
makepkg
cp *.pkg.tar.zst ~/Pacotes
sudo pacman -U --noconfirm *.pkg.tar.zst

# Build and install obs-nvfbc
cd ~/Git/obs-nvfbc
meson build
ninja -C build
cp build/nvfbc.so ~/.config/obs-studio/plugins/nvfbc/bin/64bit
cd ~

# Libvirt torture
sudo systemctl enable libvirtd
sudo systemctl start libvirtd
sudo gpasswd -a markp libvirt
sudo virsh net-define --file /etc/libvirt/qemu/networks/default.xml
sudo virsh net-autostart --network default
sudo systemctl restart libvirtd

# Autostart stuff
sudo systemctl enable sddm
sudo systemctl enable zerotier-one
sudo gnome-keyring-daemon --start
gnome-keyring-daemon --start

# AUR packages
yay -S -a mangohud goverlay-bin appimagelauncher youtube-music-bin downgrade lightly-qt protonup-qt whatsapp-nativefier toilet toilet-fonts discord-screenaudio droidcam kde-cdemu-manager virtual-studio-code-bin

# I FORGOR ZONE
printf "

!!! FINAL THINGS TO DO !!!
* Configure neofetch for user and root.
* Configure fish and omf for user and root.

"