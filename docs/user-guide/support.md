# Support & Resources

:::{rst-class} lead
Get help with JamfMCP, connect with the community, and find resources for troubleshooting
:::

## Quick Help

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} {fas}`question-circle` First Time Setup?
Start with the [Prerequisites](prereqs) and [Installation Guide](install)
::::

::::{grid-item-card} {fas}`exclamation-triangle` Something Not Working?
Check the [Troubleshooting Guide](troubleshooting) for common issues
::::

::::{grid-item-card} {fas}`code` API Errors?
Review [Jamf API Setup](jamf-api-setup) for permission requirements
::::

::::{grid-item-card} {fas}`bug` Found a Bug?
Report it on [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues/new)
::::
:::::

## Getting Help

### Asking Good Questions

When asking for help, provide:
1. **Search first** - Check existing issues and discussions
2. **Context** - What are you trying to accomplish?
3. **Error messages** - Include complete error text
4. **Versions** - JamfMCP, Python, uv, and OS versions
5. **Steps to reproduce** - What exactly did you do?
6. **Configuration** - Sanitized config (no secrets!)

## Community Resources

### MacAdmins Slack
- **Channel**: [#jamfmcp](https://macadmins.slack.com/archives/C09RR0UGF0W)
- **What to ask**: Setup help, best practices, feature ideas
- **Response time**: Community-driven, usually within hours
- **Join**: [MacAdmins Slack Signup](https://macadmins.org/slack)

### GitHub
- **[Issues](https://github.com/liquidz00/jamfmcp/issues)**: Bug reports and feature requests
- **[Releases](https://github.com/liquidz00/jamfmcp/releases)**: Version history and changelogs

### Related Communities
- **[Jamf Nation](https://community.jamf.com)**: Jamf Pro community forum
- **[MacAdmins.org](https://macadmins.org)**: macOS administration resources
- **[SOFA](https://sofa.macadmins.io)**: macOS security feed used by JamfMCP

## Gathering System Information

When reporting issues, run this command to gather version info:

```bash
# Create a diagnostic report
cat << EOF > jamfmcp-info.txt
System Information for JamfMCP
==============================
Date: $(date)

Python Version:
$(python --version)

UV Version:
$(uv --version 2>&1 || echo "uv not installed")

JamfMCP Version:
$(uv pip show jamfmcp 2>&1 || echo "JamfMCP not installed")

Environment Variables (sanitized):
JAMF_URL: ${JAMF_URL:+[SET]}
JAMF_CLIENT_ID: ${JAMF_CLIENT_ID:+[SET]}
JAMF_CLIENT_SECRET: ${JAMF_CLIENT_SECRET:+[SET]}

Platform:
$(uname -a)
EOF

echo "Diagnostic info saved to jamfmcp-info.txt"
```

## Frequently Asked Questions

:::{dropdown} **Can I use JamfMCP with Jamf School or Jamf Now?**
No, JamfMCP is designed specifically for Jamf Pro and requires Jamf Pro API access.
:::

:::{dropdown} **What Jamf Pro version is required?**
JamfMCP requires Jamf Pro 10.49+ for full OAuth2 support. Basic functionality may work with older versions using basic auth.
:::

:::{dropdown} **Is JamfMCP officially supported by Jamf?**
No, JamfMCP is a community project and is not officially supported by Jamf. For official Jamf support, contact Jamf directly.
:::

:::{dropdown} **Can I contribute to JamfMCP?**
Yes! See our [Contributing Guide](../contributing/contributor-guide) for details on how to contribute.
:::

:::{dropdown} **How do I update JamfMCP?**
```bash
# Update to latest version
uv pip install --upgrade jamfmcp

# Update to specific version
uv pip install jamfmcp==1.2.3
```
:::

:::{dropdown} **Why am I getting "spawn uv ENOENT" errors?**
This means `uv` is not accessible to your MCP client. For Claude Desktop on macOS, install `uv` via Homebrew:
```bash
brew install uv
```
See [Prerequisites](prereqs) for platform-specific installation instructions.
:::

:::{dropdown} **Can I use JamfMCP in production?**
JamfMCP is in active development. While core features are stable, thoroughly test in your environment before production use. See the warning on our [homepage](../index) for details.
:::

:::{dropdown} **How do I rotate API credentials?**
1. Create new API client in Jamf Pro
2. Update environment variables with new credentials
3. Restart your MCP client
4. Test connection with a simple query
5. Remove old API client from Jamf Pro
:::

## Support Response Times

### Community Support
- **MacAdmins Slack**: Usually within hours during US business hours
- **GitHub Discussions**: 1-3 days for community responses
- **GitHub Issues**: Maintainers review weekly

### Priority Support
For critical production issues:
1. Check [Known Issues](https://github.com/liquidz00/jamfmcp/issues?q=is%3Aissue+label%3Abug)
2. Post in MacAdmins Slack for quick community help
3. Open a detailed GitHub issue with reproduction steps

:::{note}
JamfMCP is maintained by volunteers. Response times vary based on availability.
:::

## Helping Others

### Ways to Contribute Support
- Answer questions in MacAdmins Slack [#jamfmcp](https://macadmins.slack.com/archives/C09RR0UGF0W)
- Share your setup experiences in MacAdmins Slack
- Write blog posts or create videos about JamfMCP
- Improve documentation when you solve a problem
- Star the [GitHub repository](https://github.com/liquidz00/jamfmcp) to show support

### Becoming a Contributor
Ready to contribute code? See our [Development Guide](../contributing/development-guide) to get started.

## External Resources

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} MCP Protocol
- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [FastMCP Framework](https://gofastmcp.com)
- [MCP Debugging Guide](https://modelcontextprotocol.io/docs/debugging)
::::

::::{grid-item-card} Jamf Resources
- [Jamf Developer Portal](https://developer.jamf.com)
- [Jamf Pro API Reference](https://developer.jamf.com/jamf-pro/reference)
- [Jamf Pro Documentation](https://docs.jamf.com)
- [Jamf Pro SDK for Python](https://macadmins.github.io/jamf-pro-sdk-python/)
::::

::::{grid-item-card} Python Resources
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [httpx Documentation](https://www.python-httpx.org)
::::

::::{grid-item-card} AI Assistant Resources
- [Claude Desktop Documentation](https://claude.ai/docs)
- [Cursor IDE](https://cursor.sh)
- [GitHub Copilot](https://github.com/features/copilot)
::::
:::::

### Common Commands

```bash
# Check JamfMCP version
uv pip show jamfmcp

# Update JamfMCP
uv pip install --upgrade jamfmcp

# Run CLI configuration
jamfmcp-cli --platform claude-desktop

# Test connection (in Python)
python -c "from jamfmcp.auth import JamfAuth; JamfAuth()"

# View MCP logs (Claude Desktop on macOS)
tail -f ~/Library/Logs/Claude/*.log

# View MCP logs (Cursor)
tail -f ~/.cursor/logs/main.log
```

### Environment Variables

```bash
# Required
export JAMF_URL="https://your-instance.jamfcloud.com"
export JAMF_CLIENT_ID="your-client-id"
export JAMF_CLIENT_SECRET="your-client-secret"

# Optional
export JAMF_TIMEOUT=30  # Request timeout in seconds
export JAMF_DEBUG=true  # Enable debug logging
```

## License & Legal

JamfMCP is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/liquidz00/jamfmcp/blob/main/LICENSE) file for details.

This is a community project and is not affiliated with or endorsed by Jamf Software, LLC.

---

:::{tip}
**Need more help?** The MacAdmins community is friendly and helpful. Don't hesitate to ask questions!
:::
