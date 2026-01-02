#!/usr/bin/env bash
#
# Run routing tests in a Docker container with isolated environment
#
# IMPORTANT: Container tests require an API key (ANTHROPIC_API_KEY).
# OAuth tokens do NOT work in containers due to Claude Code's native
# macOS Keychain integration.
#
# For free testing with OAuth subscription, run tests directly on the host:
#   pytest test_routing.py -v
#   ./fast_test.sh --skill agile --fast
#
# Usage:
#   ./run_container_tests.sh [options] [-- pytest-args...]
#
# Examples:
#   ./run_container_tests.sh --api-key                  # Run with API key
#   ./run_container_tests.sh --api-key --parallel 4     # Parallel execution
#   ./run_container_tests.sh --api-key -- -k "TC001"    # Single test
#
# Environment Variables:
#   ANTHROPIC_API_KEY     - API key (required)
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
            echo "Run routing tests in a Docker container."
            echo ""
            echo "IMPORTANT: Container tests require an API key (ANTHROPIC_API_KEY)."
            echo "OAuth tokens do NOT work in containers."
            echo ""
            echo "For free testing with OAuth subscription, run tests on the host:"
            echo "  pytest test_routing.py -v"
            echo "  ./fast_test.sh --skill agile --fast"
            echo ""
            echo "Options:"
            echo "  --api-key       Use ANTHROPIC_API_KEY (required)"
            echo "  --build         Rebuild Docker image before running"
            echo "  --parallel N    Run N tests in parallel (requires pytest-xdist)"
            echo "  --model NAME    Use specific model (sonnet, haiku, opus)"
            echo "  --keep          Don't remove container after run"
            echo "  --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  export ANTHROPIC_API_KEY='sk-ant-api03-...'"
            echo "  $0 --api-key                    # Run all tests"
            echo "  $0 --api-key --parallel 4       # 4 parallel workers"
            echo "  $0 --api-key -- -k 'TC001' -v   # Single test"
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
    if [[ "$USE_API_KEY" != "true" ]]; then
        echo_error "Container tests require --api-key flag"
        echo ""
        echo "OAuth tokens do NOT work in containers. Use one of:"
        echo ""
        echo "1. Run with API key (container):"
        echo "   export ANTHROPIC_API_KEY='sk-ant-api03-...'"
        echo "   $0 --api-key"
        echo ""
        echo "2. Run on host (free with OAuth subscription):"
        echo "   pytest test_routing.py -v"
        echo "   ./fast_test.sh --skill agile --fast"
        exit 1
    fi

    if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
        echo_error "ANTHROPIC_API_KEY is not set"
        echo ""
        echo "Export your API key:"
        echo "  export ANTHROPIC_API_KEY='sk-ant-api03-...'"
        echo ""
        echo "Get an API key at: https://console.anthropic.com/settings/keys"
        exit 1
    fi

    echo_info "Using API key authentication"
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

    # API key authentication
    docker_args+=("-e" "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}")

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

    # Build the full command: install plugin, then run pytest
    local install_cmd="claude plugins add /workspace/plugin --local 2>/dev/null || true"

    # Build pytest command
    local pytest_cmd="pytest test_routing.py -v"

    # Add parallel option
    if [[ -n "$PARALLEL" ]]; then
        pytest_cmd+=" -n $PARALLEL"
    fi

    # Add user-provided pytest args
    if [[ ${#PYTEST_ARGS[@]} -gt 0 ]]; then
        pytest_cmd+=" ${PYTEST_ARGS[*]}"
    fi

    # Combine: install plugin then run tests
    local full_cmd="$install_cmd && $pytest_cmd"

    # Override entrypoint to run shell command
    docker_args+=("--entrypoint" "/bin/bash")
    docker_args+=("$IMAGE_NAME:$IMAGE_TAG")
    docker_args+=("-c" "$full_cmd")

    # Run container
    echo_info "Running: docker ${docker_args[*]}"
    docker "${docker_args[@]}"
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
