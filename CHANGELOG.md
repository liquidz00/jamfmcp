<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.2] - 2025-11-15

### Added

- Entry point defined for `server.py` for leveraging `uvx` in MCP configurations
- `--write` CLI flag to create [MCP configuration](https://gofastmcp.com/integrations/mcp-json-configuration#mcp-json-configuration-standard) `.json` in appropriate directory

### Changed

- Renamed CLI from `jamfmcp` to `jamfmcp-cli` to separate entry points
- Single-command CLI; options can be passed directly instead of calling command (i.e, `jamfmcp-cli setup -p...` → `jamfmcp-cli -p claude-code...`)
- Default authentication type is now `oauth` instead of `basic`
- Project documentation structure, theme and content

### Removed

- Jamf API basic authentication methods in favor of [OAuth](https://developer.jamf.com/jamf-pro/recipes/client-credentials-authorization) for security
- Separate `validate` command as client validation on every invocation of the CLI
- Wrapped `fastmcp` CLI commands; server configuration is shown to `stdout` by default unless the `--write` flag is passed

### Fixed

- CLI setup outputs proper configurations per platform with `uvx` for PyPI installs and `uv run` for local installs
- Module path resolves properly when configuring MCP server from local installation

## [v1.0.1] - 2025-11-10

### Added

- Command line interface (`cli.py`) to assist end users in configuring JamfMCP with AI Platforms such as Claude and Cursor

### Changed

- Project documentation has been updated with CLI setup instructions
- Includes warning to Claude Desktop users to install `uv` via Homebrew for proper path resolution

## [v1.0.0] - 2025-11-08

### Added

- Initial version
