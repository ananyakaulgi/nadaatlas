#!/usr/bin/env bash
# generate_keys.sh — generate a JWT RS256 keypair for NādaAtlas
#
# Usage:
#   ./generate_keys.sh [secrets-dir]
#
# Default secrets-dir: ./secrets
#
# Run `chmod +x generate_keys.sh` once after cloning if the bit is not set.
#
set -euo pipefail

SECRETS_DIR="${1:-./secrets}"
mkdir -p "$SECRETS_DIR"

echo "Generating 4096-bit RSA private key..."
openssl genrsa -out "$SECRETS_DIR/jwt_private.pem" 4096

echo "Extracting public key..."
openssl rsa -in "$SECRETS_DIR/jwt_private.pem" -pubout -out "$SECRETS_DIR/jwt_public.pem"

# Restrictive permissions — private key readable only by owner
chmod 600 "$SECRETS_DIR/jwt_private.pem"
chmod 644 "$SECRETS_DIR/jwt_public.pem"

echo ""
echo "JWT keypair generated in $SECRETS_DIR/"
echo "  Private key : $SECRETS_DIR/jwt_private.pem  (mode 600)"
echo "  Public  key : $SECRETS_DIR/jwt_public.pem   (mode 644)"
echo ""
echo "IMPORTANT: Never commit these files."
echo "           Add '$SECRETS_DIR/' to .gitignore."
echo ""
echo "Set these environment variables (or .env):"
echo "  JWT_PRIVATE_KEY_PATH=$SECRETS_DIR/jwt_private.pem"
echo "  JWT_PUBLIC_KEY_PATH=$SECRETS_DIR/jwt_public.pem"
