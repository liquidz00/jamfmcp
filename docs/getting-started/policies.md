# Policy & Configuration Tools

These tools provide access to policies, configuration profiles, scripts, and packages in Jamf Pro.

:::{note}
**About JSON Response Schemas**

The JSON examples throughout this document show the structure of data that JamfMCP returns. When using these tools through an AI assistant, you won't see raw JSON - the AI will interpret and present this information in a natural, conversational format.
:::

## Policy Management

(get_policies)=
### Getting Policies

List all policies in Jamf Pro.

**Tool:** `get_policies`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Install Google Chrome",
        "enabled": True,
        "category": "Software Installation",
        "frequency": "Once per computer",
        "scope": {
            "all_computers": False,
            "computer_groups": ["Staff Computers"]
        }
    },
    {
        "id": 2,
        "name": "Security Settings",
        "enabled": True,
        "category": "Security",
        "frequency": "Ongoing",
        "scope": {
            "all_computers": True
        }
    }
]
```

(get_policy_details)=
### Getting Policy Details

Get detailed information about a specific policy.

**Tool:** `get_policy_details`

**Parameters:**
- `policy_id` (str, required): Policy ID

**Returns:**
```python
{
    "id": 1,
    "name": "Install Google Chrome",
    "enabled": True,
    "category": {
        "id": 5,
        "name": "Software Installation"
    },
    "frequency": "Once per computer",
    "trigger": "CHECK_IN",
    "scope": {
        "all_computers": False,
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
        "use_for_self_service": True,
        "self_service_display_name": "Google Chrome",
        "install_button_text": "Install",
        "self_service_description": "Install the latest version of Google Chrome"
    }
}
```

## Configuration Profiles

(get_configuration_profiles)=
### Getting Configuration Profiles

List all macOS configuration profiles.

**Tool:** `get_configuration_profiles`

**Returns:**
```python
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

(get_profile_details)=
### Getting Configuration Profile Details

Get detailed information about a specific configuration profile.

**Tool:** `get_profile_details`

**Parameters:**
- `profile_id` (str, required): Configuration profile ID

**Returns:**
```python
{
    "id": 1,
    "name": "Wi-Fi Configuration",
    "description": "Corporate Wi-Fi settings",
    "level": "Computer",
    "uuid": "12345678-1234-1234-1234-123456789012",
    "distribution_method": "Install Automatically",
    "user_removable": False,
    "scope": {
        "all_computers": True,
        "all_jss_users": False,
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

## Scripts

(get_scripts)=
### Getting Scripts

List all scripts available in Jamf Pro.

**Tool:** `get_scripts`

**Returns:**
```python
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

(get_script_details)=
### Getting Script Details

Get detailed information about a specific script.

**Tool:** `get_script_details`

**Parameters:**
- `script_id` (str, required): Script ID

**Returns:**
```python
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

## Packages

(get_packages)=
### Getting Packages

List all packages available in Jamf Pro.

**Tool:** `get_packages`

**Returns:**
```python
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

(get_package_details)=
### Getting Package Details

Get detailed information about a specific package.

**Tool:** `get_package_details`

**Parameters:**
- `package_id` (str, required): Package ID

**Returns:**
```python
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
    "fill_user_template": False,
    "indexed": True,
    "fill_existing_user_template": False,
    "boot_volume_required": True,
    "allow_uninstalled": True,
    "os_install": False,
    "serial_number": "",
    "suppress_updates": False,
    "ignore_conflicts": False,
    "suppress_from_dock": False,
    "suppress_eula": False,
    "suppress_registration": False
}
```

## Patch Management

(get_patch_software_titles)=
### Getting Patch Software Titles

List all patch management software titles.

**Tool:** `get_patch_software_titles`

**Returns:**
```python
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
(get_patch_policies)=
### Getting Patch Policies

List all patch policies.

**Tool:** `get_patch_policies`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Chrome Auto-Update",
        "enabled": True,
        "target_version": "120.0.6099.129",
        "release_date": "2024-01-10T00:00:00Z",
        "incremental_updates": True,
        "reboot_required": False
    }
]
```

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

## Related Tools

- [`get_computer_inventory`](#get_computer_inventory) - Check policy receipts
- [`get_compliance_status`](#get_compliance_status) - Policy compliance
- [`get_smart_groups`](#get_smart_groups) - Computer groups
- [`get_categories`](#get_categories) - Policy categories
- [`get_extension_attributes`](#get_extension_attributes) - Custom attributes

:::{seealso}
- [Jamf Pro Policies API](https://developer.jamf.com/jamf-pro/reference/get_v1-policies)
- [Configuration Profiles API](https://developer.jamf.com/jamf-pro/reference/get_v1-macos-configuration-profiles)
- [Scripts API](https://developer.jamf.com/jamf-pro/reference/get_v1-scripts)
- [Packages API](https://developer.jamf.com/jamf-pro/reference/get_v1-packages)
:::
