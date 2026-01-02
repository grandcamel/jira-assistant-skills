#!/usr/bin/env bash
#
# Run routing tests in a Docker container with isolated environment
#
# This script supports two authentication modes:
# 1. OAuth Token (ANTHROPIC_AUTH_TOKEN) - Uses your Claude subscription (free)
# 2. API Key (ANTHROPIC_API_KEY) - Uses API credits (paid)
#
# Usage:
#   ./run_container_tests.sh [options] [-- pytest-args...]
#
# Examples:
#   ./run_container_tests.sh                           # Run with OAuth token
#   ./run_container_tests.sh --api-key                 # Run with API key
#   ./run_container_tests.sh --build                   # Rebuild image first
#   ./run_container_tests.sh --parallel 4              # Run 4 tests in parallel
#   ./run_container_tests.sh -- -k "TC001" -v          # Pass args to pytest
#   ./run_container_tests.sh --model haiku             # Use haiku model
#
# Environment Variables:
#   ANTHROPIC_AUTH_TOKEN  - OAuth token for subscription-based auth
#   ANTHROPIC_API_KEY     - API key for API-based auth
#   ANTHROPIC_MODEL       - Model to use (default: claude-sonnet-4-20250514)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
IMAGE_NAME="jira-skills-test-runner"
IMAGE_TAG="latest"

# Default options
USE_API_KEY=false
BUILD_IMAGE=false
PARALLEL=""
MODEL=""
KEEP_CONTAINER=false
PYTEST_ARGS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key)
            USE_API_KEY=true
            shift
            ;;
        --build)
            BUILD_IMAGE=true
            shift
            ;;
        --parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --keep)
            KEEP_CONTAINER=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options] [-- pytest-args...]"
            echo ""
            echo "Options:"
            echo "  --api-key      Use ANTHROPIC_API_KEY instead of OAuth token"
            echo "  --build        Rebuild Docker image before running"
            echo "  --parallel N   Run N tests in parallel (requires pytest-xdist)"
            echo "  --model NAME   Use specific model (sonnet, haiku, opus)"
            echo "  --keep         Don't remove container after run"
            echo "  --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                         # Run all tests with OAuth"
            echo "  $0 --build --parallel 4    # Rebuild and run 4 parallel"
            echo "  $0 -- -k 'direct' -v       # Run only direct tests"
            echo ""
            echo "Authentication:"
            echo "  OAuth (default): Set ANTHROPIC_AUTH_TOKEN"
            echo "  API Key:         Set ANTHROPIC_API_KEY and use --api-key flag"
            exit 0
            ;;
        --)
            shift
            PYTEST_ARGS=("$@")
            break
            ;;
        *)
            PYTEST_ARGS+=("$1")
            shift
            ;;
    esac
done

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Validate authentication
validate_auth() {
    if [[ "$USE_API_KEY" == "true" ]]; then
        if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
            echo_error "ANTHROPIC_API_KEY is not set"
            echo "Export your API key: export ANTHROPIC_API_KEY='sk-ant-...'"
            exit 1
        fi
        echo_info "Using API key authentication (paid)"
    else
        if [[ -z "${ANTHROPIC_AUTH_TOKEN:-}" ]]; then
            echo_error "ANTHROPIC_AUTH_TOKEN is not set"
            echo ""
            echo "To get your OAuth token:"
            echo "  1. Open Claude Code in a terminal"
            echo "  2. Run: claude --print-auth-token"
            echo "  3. Export: export ANTHROPIC_AUTH_TOKEN='<token>'"
            echo ""
            echo "Or use --api-key flag with ANTHROPIC_API_KEY"
            exit 1
        fi
        echo_info "Using OAuth token authentication (subscription)"
    fi
}

# Build Docker image
build_image() {
    echo_info "Building Docker image: $IMAGE_NAME:$IMAGE_TAG"

    docker build \
        -t "$IMAGE_NAME:$IMAGE_TAG" \
        -f "$SCRIPT_DIR/Dockerfile" \
        "$SCRIPT_DIR"

    echo_info "Image built successfully"
}

# Check if image exists
check_image() {
    if ! docker image inspect "$IMAGE_NAME:$IMAGE_TAG" &>/dev/null; then
        echo_warn "Image not found, building..."
        build_image
    fi
}

# Run tests in container
run_tests() {
    echo_info "Starting container tests..."

    # Build docker run command
    local docker_args=(
        "run"
    )

    # Remove container after run unless --keep
    if [[ "$KEEP_CONTAINER" != "true" ]]; then
        docker_args+=("--rm")
    fi

    # Mount plugin directory read-only
    docker_args+=(
        "-v" "$PLUGIN_ROOT:/workspace/plugin:ro"
        "-v" "$SCRIPT_DIR:/workspace/tests:ro"
    )

    # Set working directory
    docker_args+=("-w" "/workspace/tests")

    # Pass authentication
    if [[ "$USE_API_KEY" == "true" ]]; then
        docker_args+=("-e" "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}")
    else
        docker_args+=("-e" "ANTHROPIC_AUTH_TOKEN=${ANTHROPIC_AUTH_TOKEN}")
    fi

    # Container-specific environment
    docker_args+=(
        "-e" "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1"
        "-e" "CLAUDE_CODE_ACTION=bypassPermissions"
    )

    # Model selection
    if [[ -n "$MODEL" ]]; then
        case "$MODEL" in
            haiku)
                docker_args+=("-e" "ANTHROPIC_MODEL=claude-haiku-3-5-20241022")
                ;;
            sonnet)
                docker_args+=("-e" "ANTHROPIC_MODEL=claude-sonnet-4-20250514")
                ;;
            opus)
                docker_args+=("-e" "ANTHROPIC_MODEL=claude-opus-4-20250514")
                ;;
            *)
                docker_args+=("-e" "ANTHROPIC_MODEL=$MODEL")
                ;;
        esac
    fi

    # Add image name
    docker_args+=("$IMAGE_NAME:$IMAGE_TAG")

    # Build pytest command
    local pytest_cmd=("test_routing.py" "-v")

    # Add parallel option
    if [[ -n "$PARALLEL" ]]; then
        pytest_cmd+=("-n" "$PARALLEL")
    fi

    # Add user-provided pytest args
    if [[ ${#PYTEST_ARGS[@]} -gt 0 ]]; then
        pytest_cmd+=("${PYTEST_ARGS[@]}")
    fi

    # Run container
    echo_info "Running: docker ${docker_args[*]} ${pytest_cmd[*]}"
    docker "${docker_args[@]}" "${pytest_cmd[@]}"
}

# Main execution
main() {
    echo "=============================================="
    echo "JIRA Skills Container Test Runner"
    echo "=============================================="
    echo ""

    # Validate authentication
    validate_auth

    # Build image if requested or needed
    if [[ "$BUILD_IMAGE" == "true" ]]; then
        build_image
    else
        check_image
    fi

    # Run tests
    run_tests

    echo ""
    echo_info "Container tests completed"
}

main "$@"
