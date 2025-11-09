# Tools Troubleshooting

This guide helps resolve common issues when using JamfMCP tools.

## General Tool Issues

### Tool Not Found

**Symptoms:**
- "Unknown tool" errors
- Tool doesn't appear in list
- Function not available

**Solutions:**
1. **Verify Server Version**
   - Ensure you have the latest JamfMCP
   - Check tool availability in documentation

2. **Restart MCP Server**
   - Configuration changes require restart
   - Quit and restart your MCP client

### Slow Performance

**Symptoms:**
- Tools take long time to respond
- Timeouts on operations
- Incomplete results

**Solutions:**
1. **Optimize Requests**
   - Request only needed inventory sections
   - Use specific identifiers when known
   - Limit result sets where possible

2. **Check Network**
   - Verify connection to Jamf Pro
   - Check for proxy/firewall issues
   - Test during off-peak hours

3. **Review API Limits**
   - Check Jamf Pro rate limiting
   - Monitor concurrent connections
   - Implement caching where appropriate

## Computer Health Tools

### Health Scorecard Errors

**Symptoms:**
- Incomplete scorecard data
- Missing CVE information
- Score calculation errors

**Solutions:**
1. **Verify Inventory Data**
   ```
   # First check if inventory is complete
   get_computer_inventory with serial number
   ```

2. **Check SOFA Feed Access**
   - Ensure internet connectivity
   - Verify SOFA feed is accessible
   - Check for proxy restrictions

3. **Review Computer Data**
   - Ensure computer has recent check-in
   - Verify extension attributes populated
   - Check for missing required fields

### Diagnostic Failures

**Common Issues:**
- Missing uptime data
- No last check-in time
- Incomplete hardware info

**Solutions:**
- Verify computer is managed
- Check MDM communication
- Review inventory collection settings

## Inventory Tools

### Search Not Finding Computers

**Symptoms:**
- No results for known computers
- Partial results only
- Search timeouts

**Solutions:**
1. **Check Search Criteria**
   - Verify serial number format
   - Try different identifiers
   - Check case sensitivity

2. **Verify Permissions**
   - Ensure API user can read computers
   - Check site restrictions
   - Review computer group access

3. **Handle Special Characters**
   - Escape special characters in searches
   - Use exact match when possible
   - Try partial searches

### Incomplete Inventory

**Common Issues:**
- Missing applications
- No FileVault status
- Empty extension attributes

**Solutions:**
1. **Check Collection Settings**
   - Review Jamf Pro inventory settings
   - Verify collection frequency
   - Check extension attribute scripts

2. **Request Specific Sections**

   > "Get only general, hardware, and OS information for the computer"

3. **Verify MDM Profile**
   - Ensure MDM profile installed
   - Check privacy preferences
   - Review system extensions

### Missing Inventory Data
- Check computer's last inventory update
- Verify inventory collection settings
- Some sections may be empty if not applicable
- Review extension attribute population

### Search Returns No Results
- Verify the computer exists in Jamf Pro
- Check for typos in serial number
- Try searching by computer name instead
- Ensure API user has proper permissions

## Policy and Profile Tools

### Policy Not Found

**Symptoms:**
- Known policies not appearing
- Empty policy lists
- 404 errors on policy details

**Solutions:**
1. **Check API Permissions**
   - Verify read access to policies
   - Check site restrictions
   - Review category permissions

2. **Verify Policy Status**
   - Ensure policy is enabled
   - Check if in correct site
   - Review scope limitations

### Profile Details Missing

**Common Issues:**
- Payload information incomplete
- Scope data not showing
- Version history missing

**Solutions:**
- Check API version compatibility
- Verify profile type support
- Review MDM capabilities

### Missing Policy/Profile Details
- Confirm item ID is correct
- Check for deleted/archived items
- Verify complete API access

### Policy Scope Issues
- Review computer group membership
- Check for conflicting exclusions
- Verify site membership if using sites

## Organization Tools

### User/Department Not Found

**Symptoms:**
- LDAP users not appearing
- Department list empty
- Building information missing

**Solutions:**
1. **Check LDAP Integration**
   - Verify LDAP connection active
   - Test LDAP queries
   - Review mapping settings

2. **Verify Data Entry**
   - Check for typos
   - Review case sensitivity
   - Verify data exists in Jamf Pro

### Site Restrictions

**Common Issues:**
- Limited visibility to sites
- Cross-site data not available
- Full site access needed

**Solutions:**
- Verify API user site access
- Check full access permissions
- Review site membership

### Assignment Discrepancies
- Review computer check-in status
- Verify user/location updates are processed
- Check for data sync delays

### Organization Search Issues
- Use exact names when possible
- Check for special characters
- Verify case sensitivity
- Review site restrictions

## Security Tools

### CVE Analysis Failures

**Symptoms:**
- No CVE data returned
- Outdated vulnerability info
- SOFA feed errors

**Solutions:**
1. **Check SOFA Feed**

   > "Get CVE information for computer with serial ABC123"

2. **Verify OS Version**
   - Ensure OS version is recognized
   - Check for beta OS versions
   - Review version formatting

### Compliance Status Issues

**Common Problems:**
- Compliance always shows non-compliant
- Missing compliance data
- Incorrect status reporting

**Solutions:**
- Verify compliance policies configured
- Check smart group membership
- Review configuration profiles

### Compliance Failures
- Verify policy scope is correct
- Check computer group membership
- Review policy logs for errors
- Ensure inventory is up-to-date

### License Discrepancies
- Audit actual installations
- Check for duplicate entries
- Verify scope configurations
- Review assignment logic

### Device Lock Issues
- Ensure MDM is properly configured
- Verify computer supports device lock
- Check MDM communication
- Review command history

(utility_tools)=
## Utility Tools

### Webhook Failures

**Symptoms:**
- Webhooks not triggering
- Event data missing
- Connection errors

**Solutions:**
1. **Verify Webhook Config**
   - Check endpoint URL
   - Verify authentication
   - Test with webhook.site

2. **Review Event Types**
   - Ensure events are enabled
   - Check event filtering
   - Verify payload format

### Extension Attribute Issues

**Common Problems:**
- Scripts not executing
- Data type mismatches
- Empty attribute values

**Solutions:**
- Test scripts locally first
- Verify script permissions
- Check data type settings
- Review error handling

### LDAP Problems
- Test connection from Jamf Pro
- Verify service account permissions
- Check network connectivity
- Review SSL certificate validity
- Enable LDAP debug logging

### Webhook Configuration Issues
- Verify endpoint accessibility
- Check authentication headers
- Test with webhook.site first
- Review event subscriptions
- Monitor webhook history in Jamf

## Performance Optimization

### Reducing Response Times

1. **Use Specific Sections**

   **Good:**
   > "Get general and hardware information for the computer"

   **Avoid:**
   > "Get all information for the computer"

2. **Implement Caching**
   - Cache frequently used data
   - Set reasonable TTLs
   - Invalidate on changes

3. **Batch Operations**
   - Group related queries
   - Use async where possible
   - Minimize round trips

### Handling Large Datasets

1. **Use Pagination**
   - Set appropriate page sizes
   - Handle pagination tokens
   - Process incrementally

2. **Filter Results**
   - Use search criteria
   - Apply filters early
   - Limit result fields

## Error Messages

### Common Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Verify credentials |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify resource exists |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Check Jamf Pro status |
| 503 | Service Unavailable | Wait and retry |

## Debug Techniques

### Enable Verbose Logging

```json
{
  "env": {
    "LOG_LEVEL": "DEBUG",
    "SHOW_API_CALLS": "true"
  }
}
```

### Test Individual Tools

1. Start with simple tools (ping)
2. Test with known good data
3. Gradually increase complexity
4. Document what works/fails

### Collect Diagnostic Data

When reporting issues, include:
- Tool name and parameters
- Error messages (complete)
- Debug logs if available
- Jamf Pro version
- JamfMCP version

## Related Guides

- [Configuration Troubleshooting](configuration) - Setup and config issues
- [Authentication Troubleshooting](authentication) - Permission problems
- [Connectivity Troubleshooting](connectivity) - Network issues
- [Tools Overview](../getting-started/tools-overview) - Tool documentation

## Getting Support

1. **Search Existing Issues**
   - [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
   - Check closed issues too

2. **Ask the Community**
   - [MacAdmins Slack #jamfmcp](https://macadmins.slack.com/archives/C07EH1R7LB0)
   - Include error details

3. **File a Bug Report**
   - Provide reproduction steps
   - Include system information
   - Attach debug logs
