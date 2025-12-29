FROM node:20-slim

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Create workspace
WORKDIR /workspace

# Copy plugin
COPY plugins/jira-assistant-skills /workspace/.claude-plugin/jira-assistant-skills

# Install Python dependencies
COPY plugins/jira-assistant-skills/skills/shared/scripts/lib/requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt

# Environment variables (override at runtime)
ENV JIRA_API_TOKEN=""
ENV JIRA_EMAIL=""
ENV JIRA_SITE_URL=""

# Default command
CMD ["claude"]
