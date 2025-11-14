# WebMin WireGuard Manager

A WebMin plugin for managing WireGuard VPN clients with a user-friendly web interface.

## Authors

- Reiner Hagn ([df9ry](https://github.com/df9ry)) - Primary developer
- DeepSeek AI - Development support and code assistance

## About DeepSeek AI
This project received development assistance from [DeepSeek AI](https://www.deepseek.com), 
an AI assistant created by 深度求索 (DeepSeek) that specializes in coding and technical projects.

## License
This project is licensed under the GPL v3 License - see the [LICENSE](LICENSE) file for details.

## Installation Methods

### Debian Package (Recommended)
```bash
# Download the latest .deb file from Releases
sudo dpkg -i webmin-wireguard-manager_1.0-1_all.deb
sudo apt-get install -f  # Install dependencies if needed
```

### Manual Installation
```bash
make install
```

### From Source
```bash
git clone https://github.com/df9ry/wg-manager-webmin
cd wg-manager-webmin
make install
```

### Building Debian Package
`bash
# Install build dependencies
sudo apt install devscripts debhelper dh-make

# Build package
make deb
`

`bash
make install
`

## Features
* [Full feature list...]

### **12. Build-Script für Entwickler (build-deb.sh):**
`bash
#!/bin/bash
#
# Build script for WebMin WireGuard Manager Debian package
# Copyright (C) 2024 Reiner Hagn (df9ry) and contributors

set -e

echo "🔨 Building Debian package for WebMin WireGuard Manager"

# Check dependencies
for cmd in dpkg-deb dh_builddeb; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ Missing required tool: $cmd"
        echo "💡 Install with: sudo apt install devscripts debhelper"
        exit 1
    fi
done

# Clean previous builds
make clean

# Build package
echo "📦 Building Debian package..."
dpkg-buildpackage -us -uc -b

# Find the built package
DEB_FILE=$(ls ../webmin-wireguard-manager_*.deb 2>/dev/null | head -1)

if [ -n "$DEB_FILE" ]; then
    echo "✅ Package built successfully: $DEB_FILE"
    echo "📊 Package info:"
    dpkg-deb -I "$DEB_FILE"
else
    echo "❌ Package build failed"
    exit 1
fi
`

## Build- und Installationsprozess:
### Für Entwickler
`
# Einfaches Bauen
make deb

# Oder mit dem Build-Script
chmod +x build-deb.sh
./build-deb.sh
´

### Für Benutzer:
´
# Installation des .deb Packages
sudo dpkg -i webmin-wireguard-manager_1.0-1_all.deb

# Falls Abhängigkeiten fehlen:
sudo apt-get install -f
´

