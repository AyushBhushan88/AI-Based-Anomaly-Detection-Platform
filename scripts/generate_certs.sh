#!/bin/bash

# Define directory
CERT_DIR="./certs/postgres"
mkdir -p "$CERT_DIR"

# Generate CA key and certificate
openssl req -new -x509 -days 365 -nodes -out "$CERT_DIR/server.crt" \
    -keyout "$CERT_DIR/server.key" -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set permissions for Postgres
chmod 600 "$CERT_DIR/server.key"
chmod 644 "$CERT_DIR/server.crt"

echo "Certificates generated in $CERT_DIR"
