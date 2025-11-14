# Installation Guide

## Requirements
- WebMin 1.900+
- WireGuard installed and configured
- Perl 5.10+

## Installation Steps

1. Copy the module to WebMin:
  
   sudo cp -r wg-manager /usr/share/webmin/

sudo chmod +x /usr/share/webmin/wg-manager/*.cgi
sudo chmod +x /usr/share/webmin/wg-manager/wg-*


### **6. Deployment Script mit Lizenz-Check:**

**deploy.sh:**
bash
#!/bin/bash
#
# WebMin WireGuard Manager - Deployment script
# Copyright (C) 2024 Reiner Hagn (df9ry) and contributors

set -e

echo "🚀 Deploying WebMin WireGuard Manager (GPL v3)"

# Lizenz-Check
if [ ! -f "LICENSE" ]; then
    echo "❌ LICENSE file missing - aborting deployment"
    exit 1
fi

echo "✅ GPL v3 License confirmed"

echo "📦 Building Debian package..."
if make deb; then
    DEB_FILE=$(ls ../webmin-wireguard-manager_*.deb | head -1)
    echo "✅ Package built: $DEB_FILE"
    
    echo "🔧 Installing package..."
    if sudo dpkg -i "$DEB_FILE"; then
        echo "🎉 Installation completed successfully!"
        echo "📋 Access via: WebMin → Networking → WireGuard Manager"
    else
        echo "❌ Package installation failed"
        exit 1
    fi
else
    echo "❌ Package build failed"
    exit 1
fi