#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Extract Docker DNS info BEFORE any flushing
DOCKER_DNS_RULES=$(iptables-save -t nat | grep "127\.0\.0\.11" || true)

# Flush existing rules and delete existing ipsets
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
ipset destroy allowed-domains 2>/dev/null || true

# Restore Docker DNS rules
if [ -n "$DOCKER_DNS_RULES" ]; then
    echo "Restoring Docker DNS rules..."
    iptables -t nat -N DOCKER_OUTPUT 2>/dev/null || true
    iptables -t nat -N DOCKER_POSTROUTING 2>/dev/null || true
    echo "$DOCKER_DNS_RULES" | xargs -L 1 iptables -t nat
else
    echo "No Docker DNS rules to restore"
fi

# Allow DNS, SSH, and localhost before restrictions
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Create ipset with CIDR support
ipset create allowed-domains hash:net

# Fetch and add GitHub IP ranges
echo "Fetching GitHub IP ranges..."
gh_ranges=$(curl -s https://api.github.com/meta)
if [ -z "$gh_ranges" ]; then
    echo "ERROR: Failed to fetch GitHub IP ranges"
    exit 1
fi

if ! echo "$gh_ranges" | jq -e '.web and .api and .git' >/dev/null; then
    echo "ERROR: GitHub API response missing required fields"
    exit 1
fi

echo "Processing GitHub IPs..."
while read -r cidr; do
    if [[ ! "$cidr" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        echo "ERROR: Invalid CIDR range from GitHub meta: $cidr"
        exit 1
    fi
    echo "Adding GitHub range $cidr"
    ipset add allowed-domains "$cidr"
done < <(echo "$gh_ranges" | jq -r '(.web + .api + .git)[]' | aggregate -q)

# Resolve and add allowed domains
# Includes: npm, Claude API, VS Code, Sentry, Statsig, and Atlassian/JIRA
for domain in \
    "registry.npmjs.org" \
    "api.anthropic.com" \
    "sentry.io" \
    "statsig.anthropic.com" \
    "statsig.com" \
    "marketplace.visualstudio.com" \
    "vscode.blob.core.windows.net" \
    "update.code.visualstudio.com" \
    "id.atlassian.com" \
    "api.atlassian.com" \
    "auth.atlassian.com"; do
    echo "Resolving $domain..."
    ips=$(dig +noall +answer A "$domain" | awk '$4 == "A" {print $5}')
    if [ -z "$ips" ]; then
        echo "WARNING: Failed to resolve $domain (may not be needed)"
        continue
    fi

    while read -r ip; do
        if [[ ! "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
            echo "WARNING: Invalid IP from DNS for $domain: $ip"
            continue
        fi
        echo "Adding $ip for $domain"
        ipset add allowed-domains "$ip" 2>/dev/null || true
    done < <(echo "$ips")
done

# Add Atlassian Cloud IP ranges (from their documentation)
# https://support.atlassian.com/organization-administration/docs/ip-addresses-and-domains-for-atlassian-cloud-products/
echo "Adding Atlassian Cloud IP ranges..."
for cidr in \
    "13.52.5.96/28" \
    "13.236.8.224/28" \
    "18.136.214.96/28" \
    "18.184.99.224/28" \
    "18.234.32.224/28" \
    "18.246.31.224/28" \
    "52.41.219.63/32" \
    "52.215.192.128/28" \
    "104.192.136.0/21" \
    "185.166.140.0/22"; do
    echo "Adding Atlassian range $cidr"
    ipset add allowed-domains "$cidr" 2>/dev/null || true
done

# Resolve user's JIRA site if JIRA_SITE_URL is set
if [ -n "${JIRA_SITE_URL:-}" ]; then
    # Extract hostname from URL
    JIRA_HOST=$(echo "$JIRA_SITE_URL" | sed -e 's|^https\?://||' -e 's|/.*$||')
    echo "Resolving JIRA site: $JIRA_HOST..."
    ips=$(dig +noall +answer A "$JIRA_HOST" | awk '$4 == "A" {print $5}')
    if [ -n "$ips" ]; then
        while read -r ip; do
            if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                echo "Adding $ip for $JIRA_HOST"
                ipset add allowed-domains "$ip" 2>/dev/null || true
            fi
        done < <(echo "$ips")
    fi
fi

# Get host IP from default route
HOST_IP=$(ip route | grep default | cut -d" " -f3)
if [ -z "$HOST_IP" ]; then
    echo "ERROR: Failed to detect host IP"
    exit 1
fi

HOST_NETWORK=$(echo "$HOST_IP" | sed "s/\.[0-9]*$/.0\/24/")
echo "Host network detected as: $HOST_NETWORK"

# Allow host network
iptables -A INPUT -s "$HOST_NETWORK" -j ACCEPT
iptables -A OUTPUT -d "$HOST_NETWORK" -j ACCEPT

# Set default policies to DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow outbound to allowed domains only
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Reject all other outbound traffic
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited

echo "Firewall configuration complete"

# Verify firewall blocks unauthorized domains
echo "Verifying firewall rules..."
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "ERROR: Firewall verification failed - was able to reach https://example.com"
    exit 1
else
    echo "Firewall verification passed - blocked https://example.com as expected"
fi

# Verify GitHub API access works
if ! curl --connect-timeout 5 https://api.github.com/zen >/dev/null 2>&1; then
    echo "ERROR: Firewall verification failed - unable to reach https://api.github.com"
    exit 1
else
    echo "Firewall verification passed - able to reach https://api.github.com"
fi

echo "Sandbox firewall active - only whitelisted domains accessible"
