# Policy & Configuration

:::{rst-class} lead
Tools for managing policies, configuration profiles, scripts, and packages in Jamf Pro.
:::

## Policy Management

(get_policies)=
### Get Policies

List all policies in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Install Google Chrome",
    "enabled": true,
    "category": "Software Installation",
    "frequency": "Once per computer",
    "scope": {
      "all_computers": false,
      "computer_groups": ["Staff Computers"]
    }
  },
  {
    "id": 2,
    "name": "Security Settings",
    "enabled": true,
    "category": "Security",
    "frequency": "Ongoing",
    "scope": {
      "all_computers": true
    }
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
Show me all policies in Jamf Pro
:::

:::{ai-prompt}
List all enabled policies and their categories
:::

:::{ai-prompt}
Get all policies that apply to all computers
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Policy Details
:link: get_policy_details
:link-type: ref

Detailed policy configuration
::::

::::{grid-item-card} Get Computer History
:link: get_computer_history
:link-type: ref

Policy execution logs
::::
:::::

---

(get_policy_details)=
### Get Policy Details

Get detailed information about a specific policy.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `policy_id`
    - str
    - **Yes**
    - Policy ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Install Google Chrome",
  "enabled": true,
  "category": {
    "id": 5,
    "name": "Software Installation"
  },
  "frequency": "Once per computer",
  "trigger": "CHECK_IN",
  "scope": {
    "all_computers": false,
    "computer_groups": [{
      "id": 10,
      "name": "Staff Computers"
    }],
    "exclusions": {
      "computers": [],
      "computer_groups": [{
        "id": 15,
        "name": "Lab Computers"
      }]
    }
  },
  "packages": [{
    "id": 25,
    "name": "GoogleChrome-120.0.pkg",
    "action": "Install"
  }],
  "scripts": [{
    "id": 30,
    "name": "Post-Install Configuration",
    "priority": "After"
  }],
  "self_service": {
    "use_for_self_service": true,
    "self_service_display_name": "Google Chrome",
    "install_button_text": "Install",
    "self_service_description": "Install the latest version of Google Chrome"
  }
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for policy ID 1
:::

:::{ai-prompt}
Show me the scope and exclusions for policy 45
:::

:::{ai-prompt}
What packages and scripts are included in policy ID 100?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

List all policies
::::

::::{grid-item-card} Get Packages
:link: get_packages
:link-type: ref

Package details
::::
:::::

---

## Configuration Profiles

(get_configuration_profiles)=
### Get Configuration Profiles

List all macOS configuration profiles.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Wi-Fi Configuration",
    "description": "Corporate Wi-Fi settings",
    "level": "Computer",
    "distribution_method": "Install Automatically",
    "payloads": ["com.apple.wifi.managed"]
  },
  {
    "id": 2,
    "name": "FileVault Configuration",
    "description": "Enable FileVault encryption",
    "level": "Computer",
    "distribution_method": "Install Automatically",
    "payloads": ["com.apple.MCX.FileVault2"]
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all configuration profiles
:::

:::{ai-prompt}
Show me all profiles that install automatically
:::

:::{ai-prompt}
Get all security-related configuration profiles
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Profile Details
:link: get_profile_details
:link-type: ref

Detailed profile configuration
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Installed profiles on computers
::::
:::::

---

(get_profile_details)=
### Get Configuration Profile Details

Get detailed information about a specific configuration profile.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `profile_id`
    - str
    - **Yes**
    - Configuration profile ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Wi-Fi Configuration",
  "description": "Corporate Wi-Fi settings",
  "level": "Computer",
  "uuid": "12345678-1234-1234-1234-123456789012",
  "distribution_method": "Install Automatically",
  "user_removable": false,
  "scope": {
    "all_computers": true,
    "all_jss_users": false,
    "computer_groups": [],
    "exclusions": {
      "computers": [],
      "computer_groups": []
    }
  },
  "payloads": [{
    "payload_type": "com.apple.wifi.managed",
    "payload_identifier": "com.company.wifi",
    "payload_display_name": "Wi-Fi",
    "payload_description": "Configures Wi-Fi settings"
  }]
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for configuration profile ID 1
:::

:::{ai-prompt}
Show me the scope for profile 10
:::

:::{ai-prompt}
What payloads are included in profile ID 5?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Configuration Profiles
:link: get_configuration_profiles
:link-type: ref

List all profiles
::::

::::{grid-item-card} Get Compliance Status
:link: get_compliance_status
:link-type: ref

Profile compliance
::::
:::::

---

## Scripts

(get_scripts)=
### Get Scripts

List all scripts available in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Install Homebrew",
    "category": "Utilities",
    "filename": "install_homebrew.sh",
    "info": "Installs Homebrew package manager",
    "notes": "Run with standard user privileges"
  },
  {
    "id": 2,
    "name": "Enable Firewall",
    "category": "Security",
    "filename": "enable_firewall.sh",
    "info": "Enables macOS firewall",
    "notes": "Requires admin privileges"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all scripts in Jamf Pro
:::

:::{ai-prompt}
Show me all security-related scripts
:::

:::{ai-prompt}
Get all utility scripts available
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Script Details
:link: get_script_details
:link-type: ref

Script content and parameters
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Policies using scripts
::::
:::::

---

(get_script_details)=
### Get Script Details

Get detailed information about a specific script.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `script_id`
    - str
    - **Yes**
    - Script ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Install Homebrew",
  "category": {
    "id": 5,
    "name": "Utilities"
  },
  "filename": "install_homebrew.sh",
  "info": "Installs Homebrew package manager",
  "notes": "Run with standard user privileges",
  "priority": "Before",
  "parameters": {
    "parameter4": "User to install for",
    "parameter5": "Install location",
    "parameter6": "",
    "parameter7": "",
    "parameter8": "",
    "parameter9": "",
    "parameter10": "",
    "parameter11": ""
  },
  "os_requirements": "10.15",
  "script_contents": "#!/bin/bash\n# Install Homebrew\n..."
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for script ID 1
:::

:::{ai-prompt}
Show me the contents of script 10
:::

:::{ai-prompt}
What parameters does script ID 5 accept?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Scripts
:link: get_scripts
:link-type: ref

List all scripts
::::

::::{grid-item-card} Get Policy Details
:link: get_policy_details
:link-type: ref

Policies using this script
::::
:::::

---

## Packages

(get_packages)=
### Get Packages

List all packages available in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Google Chrome",
    "filename": "GoogleChrome-120.0.pkg",
    "category": "Web Browsers",
    "info": "Google Chrome web browser",
    "size": "215 MB"
  },
  {
    "id": 2,
    "name": "Microsoft Office",
    "filename": "Office365-16.80.pkg",
    "category": "Productivity",
    "info": "Microsoft Office suite",
    "size": "2.1 GB"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all packages in Jamf Pro
:::

:::{ai-prompt}
Show me all web browser packages
:::

:::{ai-prompt}
Get all productivity software packages
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Package Details
:link: get_package_details
:link-type: ref

Package configuration details
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Policies deploying packages
::::
:::::

---

(get_package_details)=
### Get Package Details

Get detailed information about a specific package.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `package_id`
    - str
    - **Yes**
    - Package ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Google Chrome",
  "filename": "GoogleChrome-120.0.pkg",
  "category": {
    "id": 10,
    "name": "Web Browsers"
  },
  "info": "Google Chrome web browser",
  "notes": "Latest stable version",
  "size": "215 MB",
  "priority": 10,
  "os_requirements": "10.15",
  "fill_user_template": false,
  "indexed": true,
  "fill_existing_user_template": false,
  "boot_volume_required": true,
  "allow_uninstalled": true,
  "os_install": false,
  "serial_number": "",
  "suppress_updates": false,
  "ignore_conflicts": false,
  "suppress_from_dock": false,
  "suppress_eula": false,
  "suppress_registration": false
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for package ID 1
:::

:::{ai-prompt}
Show me the requirements for package 10
:::

:::{ai-prompt}
What is the size and OS requirement for package ID 5?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Packages
:link: get_packages
:link-type: ref

List all packages
::::

::::{grid-item-card} Get Policy Details
:link: get_policy_details
:link-type: ref

Policies using this package
::::
:::::

---

## Patch Management

(get_patch_software_titles)=
### Get Patch Software Titles

List all patch management software titles.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Google Chrome",
    "publisher": "Google",
    "app_name": "Google Chrome.app",
    "bundle_id": "com.google.Chrome",
    "current_version": "120.0.6099.129",
    "last_update": "2024-01-10T00:00:00Z",
    "installed_count": 450
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all patch management software titles
:::

:::{ai-prompt}
Show me software titles with available patches
:::

:::{ai-prompt}
Get all patch titles and their current versions
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Patch Policies
:link: get_patch_policies
:link-type: ref

Patch deployment policies
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Installed software versions
::::
:::::

---

(get_patch_policies)=
### Get Patch Policies

List all patch policies.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "name": "Chrome Auto-Update",
    "enabled": true,
    "target_version": "120.0.6099.129",
    "release_date": "2024-01-10T00:00:00Z",
    "incremental_updates": true,
    "reboot_required": false
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all patch policies
:::

:::{ai-prompt}
Show me enabled patch policies
:::

:::{ai-prompt}
Get all patch policies that don't require a reboot
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Patch Software Titles
:link: get_patch_software_titles
:link-type: ref

Available patch titles
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Related deployment policies
::::
:::::

---

## Best Practices

### Policy Analysis
1. **Check Scope**: Review which computers policies target
2. **Verify Enabled**: Ensure critical policies are enabled
3. **Review Frequency**: Check if frequency matches intent
4. **Audit Exclusions**: Verify exclusions are intentional

### Profile Management
1. **Payload Review**: Understand what each profile configures
2. **User Removable**: Check if users can remove critical profiles
3. **Distribution Method**: Ensure automatic where needed
4. **Scope Verification**: Confirm proper targeting

### Script Security
1. **Review Contents**: Audit script code for security
2. **Parameter Usage**: Check for hardcoded sensitive data
3. **Privilege Level**: Verify appropriate execution context
4. **OS Requirements**: Ensure compatibility

### Package Deployment
1. **Size Awareness**: Consider bandwidth for large packages
2. **Priority Order**: Check installation sequence
3. **Requirements**: Verify OS compatibility
4. **Update Strategy**: Plan for version management

:::{seealso}
- [Jamf Pro Policies API](https://developer.jamf.com/jamf-pro/reference/get_v1-policies)
- [Configuration Profiles API](https://developer.jamf.com/jamf-pro/reference/get_v1-macos-configuration-profiles)
- [Scripts API](https://developer.jamf.com/jamf-pro/reference/get_v1-scripts)
- [Packages API](https://developer.jamf.com/jamf-pro/reference/get_v1-packages)
:::
