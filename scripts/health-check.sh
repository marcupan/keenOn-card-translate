#!/bin/bash
# Health check script for keenOn-card-translate service

set -e

# Configuration
HOST="localhost"
PORT="50051"
TIMEOUT=5
RETRIES=3

# Function to check if the service is healthy
check_health() {
  # Try to connect to the gRPC service
  if command -v grpcurl &> /dev/null; then
    # If grpcurl is available, use it to check the health endpoint
    if grpcurl -plaintext -connect-timeout $TIMEOUT $HOST:$PORT health.Health/Check &> /dev/null; then
      return 0
    fi
  else
    # Fallback to a simple TCP connection check
    if nc -z -w $TIMEOUT $HOST $PORT &> /dev/null; then
      return 0
    fi
  fi

  # Try a Python-specific check as another fallback
  if command -v python3 &> /dev/null; then
    if python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout($TIMEOUT); s.connect(('$HOST', $PORT)); s.close()" &> /dev/null; then
      return 0
    fi
  fi

  return 1
}

# Main health check logic
echo "Checking health of keenOn-card-translate service at $HOST:$PORT..."

for i in $(seq 1 $RETRIES); do
  if check_health; then
    echo "Service is healthy!"
    exit 0
  else
    echo "Health check failed (attempt $i/$RETRIES)..."
    sleep 1
  fi
done

echo "Service is unhealthy after $RETRIES attempts."
exit 1
