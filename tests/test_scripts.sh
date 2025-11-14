#!/bin/bash
# tests/test_scripts.sh

set -e

echo "🧪 Teste WireGuard Scripts..."

# Test directory for safe testing
TEST_DIR="/tmp/wg-test"
mkdir -p "$TEST_DIR"

# Backup original if exists
if [ -f "/etc/wireguard/wg0.conf" ]; then
    cp /etc/wireguard/wg0.conf "$TEST_DIR/wg0.conf.backup"
fi

# Create test wg0.conf
cat > "$TEST_DIR/wg0.conf" << 'EOF'
[Interface]
PrivateKey = TEST_SERVER_PRIVATE_KEY
Address = 10.7.0.1/24, fddd:2c4:2c4:2c4::1/64
ListenPort = 51820

# Existing clients will be listed here
EOF

# Test the addclient script
echo "📝 Teste wg-addclient..."
../scripts/wg-addclient "test-client" "10.7.0.99/32" "fddd:2c4:2c4:2c4::99/128"

# Check if client config was created
if [ -f "/etc/wireguard/clients/test-client.conf" ]; then
    echo "✅ wg-addclient: Erfolg"
else
    echo "❌ wg-addclient: Fehler - Client Config nicht erstellt"
    exit 1
fi

echo "🎉 Alle Tests erfolgreich!"