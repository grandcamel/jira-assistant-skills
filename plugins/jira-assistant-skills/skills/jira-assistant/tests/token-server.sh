#!/usr/bin/env bash
#
# Token Server for OAuth Token Refresh
#
# Runs a minimal HTTP server on localhost that serves fresh OAuth tokens
# from the macOS Keychain. Designed to be called by apiKeyHelper in containers.
#
# Usage:
#   ./token-server.sh              # Start server on port 9876
#   ./token-server.sh --port 8888  # Start on custom port
#   ./token-server.sh --stop       # Stop running server
#   ./token-server.sh --status     # Check if server is running
#

set -e

PORT=9876
PID_FILE="/tmp/claude-token-server.pid"
LOG_FILE="/tmp/claude-token-server.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --stop)
            if [[ -f "$PID_FILE" ]]; then
                PID=$(cat "$PID_FILE")
                if kill -0 "$PID" 2>/dev/null; then
                    kill "$PID" 2>/dev/null || true
                    # Also kill any child processes
                    pkill -P "$PID" 2>/dev/null || true
                    rm -f "$PID_FILE"
                    echo "Token server stopped (PID: $PID)"
                else
                    rm -f "$PID_FILE"
                    echo "Token server was not running"
                fi
            else
                echo "No PID file found"
            fi
            exit 0
            ;;
        --status)
            if [[ -f "$PID_FILE" ]]; then
                PID=$(cat "$PID_FILE")
                if kill -0 "$PID" 2>/dev/null; then
                    echo "Token server running (PID: $PID, Port: $PORT)"
                    exit 0
                else
                    rm -f "$PID_FILE"
                    echo "Token server not running (stale PID file removed)"
                    exit 1
                fi
            else
                echo "Token server not running"
                exit 1
            fi
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --port PORT   Port to listen on (default: 9876)"
            echo "  --stop        Stop running server"
            echo "  --status      Check if server is running"
            echo "  --help        Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check for required tools
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required but not installed"
    exit 1
fi

if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed"
    echo "Install with: brew install jq"
    exit 1
fi

# Function to get fresh token from Keychain
get_token() {
    local creds
    creds=$(security find-generic-password -a "$USER" -s 'Claude Code-credentials' -w 2>/dev/null)
    if [[ -z "$creds" ]]; then
        echo ""
        return 1
    fi
    echo "$creds" | jq -r '.claudeAiOauth.accessToken' 2>/dev/null
}

# Check if port is available
if lsof -i ":$PORT" >/dev/null 2>&1; then
    echo "Error: Port $PORT is already in use"
    echo "Run '$0 --stop' to stop existing server, or use --port to specify another"
    exit 1
fi

# Verify we can get a token
TEST_TOKEN=$(get_token)
if [[ -z "$TEST_TOKEN" ]]; then
    echo "Error: Could not retrieve OAuth token from Keychain"
    echo "Make sure you're logged into Claude Code"
    exit 1
fi

echo "Starting token server on port $PORT..."
echo "Token retrieval verified (length: ${#TEST_TOKEN} chars)"

# Create Python HTTP server script in temp file
SERVER_SCRIPT="/tmp/claude-token-server.py"
cat > "$SERVER_SCRIPT" << 'PYEOF'
import http.server
import subprocess
import json
import sys

PORT = int(sys.argv[1])

class TokenHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logging

    def do_GET(self):
        try:
            # Get fresh token from Keychain
            result = subprocess.run(
                ['security', 'find-generic-password', '-a', subprocess.getoutput('whoami'),
                 '-s', 'Claude Code-credentials', '-w'],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                self.send_error(500, 'Failed to retrieve credentials')
                return

            creds = json.loads(result.stdout.strip())
            token = creds.get('claudeAiOauth', {}).get('accessToken', '')

            if not token:
                self.send_error(500, 'No token found in credentials')
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(token.encode())
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    with http.server.HTTPServer(('127.0.0.1', PORT), TokenHandler) as httpd:
        httpd.serve_forever()
PYEOF

# Start server in background
python3 "$SERVER_SCRIPT" "$PORT" >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Save PID
echo $SERVER_PID > "$PID_FILE"

# Wait a moment and verify it started
sleep 1

if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "Error: Token server failed to start"
    cat "$LOG_FILE" 2>/dev/null | tail -5
    rm -f "$PID_FILE"
    exit 1
fi

# Verify it responds
if ! curl -s "http://localhost:$PORT" >/dev/null 2>&1; then
    echo "Error: Token server not responding"
    kill "$SERVER_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
    exit 1
fi

echo "Token server started (PID: $SERVER_PID, Port: $PORT)"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"
echo ""
echo "Test with: curl -s http://localhost:$PORT"
echo "Stop with: $0 --stop"
