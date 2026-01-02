FROM node:20-slim

LABEL maintainer="jasonkrue@gmail.com"
LABEL description="Container for running JIRA Assistant Skills routing tests with Claude Code"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user for security
RUN useradd -m -s /bin/bash testrunner
USER testrunner
WORKDIR /home/testrunner

# Create virtual environment
RUN python3 -m venv /home/testrunner/venv
ENV PATH="/home/testrunner/venv/bin:$PATH"

# Install Python test dependencies
COPY --chown=testrunner:testrunner requirements-test.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements-test.txt

# Set up Claude Code config directory
ENV CLAUDE_CONFIG_DIR=/home/testrunner/.claude
RUN mkdir -p $CLAUDE_CONFIG_DIR

# Default environment variables for container operation
ENV CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
ENV CHOKIDAR_USEPOLLING=true

# Token refresh configuration (4 min TTL, before 5 min OAuth expiry)
# Used when apiKeyHelper is configured via mounted settings.json
ENV CLAUDE_CODE_API_KEY_HELPER_TTL_MS=240000

# Working directory for tests
WORKDIR /workspace

# Default command runs pytest
ENTRYPOINT ["pytest"]
CMD ["test_routing.py", "-v"]
