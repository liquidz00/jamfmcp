# Connectivity Troubleshooting

This guide helps resolve network and connectivity issues with JamfMCP.

## Common Connectivity Issues

### Connection Refused

**Error Messages:**
```
Connection refused
Failed to establish a new connection
[Errno 111] Connection refused
```

**Possible Causes:**
1. Wrong server URL or port
2. Firewall blocking connection
3. Jamf Pro server is down
4. Network connectivity issues

**Quick Checks:**

```bash
# Test basic connectivity
ping your-server.jamfcloud.com

# Test HTTPS port
nc -zv your-server.jamfcloud.com 443

# Test with curl
curl -I https://your-server.jamfcloud.com

# Check DNS resolution
nslookup your-server.jamfcloud.com
```

### Connection Timeout

**Error Messages:**
```
Connection timeout
The request timed out
TimeoutError: [Errno 60] Operation timed out
```

**Common Causes:**
1. Network latency
2. Proxy configuration issues
3. Firewall dropping packets
4. Server overloaded

**Solutions:**

#### Increase Timeout
```python
# In custom implementation
import httpx

client = httpx.AsyncClient(timeout=30.0)  # 30 seconds
```

#### Test Network Path
```bash
# Traceroute to server
traceroute your-server.jamfcloud.com

# Check for packet loss
ping -c 10 your-server.jamfcloud.com

# Test specific port
telnet your-server.jamfcloud.com 443
```

### DNS Resolution Failed

**Error Messages:**
```
Name or service not known
getaddrinfo failed
DNS resolution failed for hostname
```

**Debug Steps:**

```bash
# Check DNS resolution
nslookup your-server.jamfcloud.com
dig your-server.jamfcloud.com

# Try with IP directly (temporary test)
curl https://IP_ADDRESS/api/v1/jamf-pro-version

# Check /etc/hosts
cat /etc/hosts | grep jamf

# Flush DNS cache
# macOS
sudo dscacheutil -flushcache
# Linux
sudo systemctl restart systemd-resolved
```

## SSL/TLS Issues

### Certificate Errors

**Error Messages:**
```
SSL: CERTIFICATE_VERIFY_FAILED
certificate verify failed: unable to get local issuer certificate
SSL handshake failed
```

**Common Scenarios:**

#### Self-Signed Certificates
```bash
# View certificate
openssl s_client -connect your-server.com:443 -showcerts

# Test ignoring cert (INSECURE - testing only)
curl -k https://your-server.com/api/v1/jamf-pro-version
```

#### Certificate Chain Issues
```bash
# Check full certificate chain
openssl s_client -connect your-server.com:443 -showcerts < /dev/null

# Verify certificate
openssl s_client -connect your-server.com:443 -servername your-server.com
```

#### Corporate Proxy/MITM
1. Get corporate CA certificate
2. Add to system trust store:
   ```bash
   # macOS
   sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain corporate-ca.crt

   # Linux
   sudo cp corporate-ca.crt /usr/local/share/ca-certificates/
   sudo update-ca-certificates
   ```

### TLS Version Mismatch

**Error:**
```
SSL: TLSV1_ALERT_PROTOCOL_VERSION
TLS/SSL connection has been closed
```

**Solution:**
Ensure TLS 1.2 or higher:

```python
import ssl
import httpx

# Force TLS 1.2 minimum
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_2

client = httpx.AsyncClient(verify=context)
```

## Proxy Configuration

### Behind Corporate Proxy

**Symptoms:**
- Works on corporate network only
- Connection timeouts
- "Proxy Authentication Required"

**Configure Proxy:**

#### System Environment
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

#### In Python
```python
import httpx

proxies = {
    "http://": "http://proxy.company.com:8080",
    "https://": "http://proxy.company.com:8080",
}

client = httpx.AsyncClient(proxies=proxies)
```

#### Proxy Authentication
```bash
export HTTPS_PROXY=http://username:password@proxy.company.com:8080
```

### Bypass Proxy for Jamf

Add to NO_PROXY:
```bash
export NO_PROXY=localhost,127.0.0.1,*.jamfcloud.com,your-server.com
```

## Firewall Issues

### Required Ports

JamfMCP requires outbound access to:

| Service | Port | Protocol | Direction |
|---------|------|----------|-----------|
| Jamf Pro API | 443 | HTTPS | Outbound |
| Jamf Pro (custom) | 8443 | HTTPS | Outbound |
| SOFA Feed | 443 | HTTPS | Outbound |

### Test Connectivity

```bash
# Test Jamf Pro
curl -I https://your-server.com:443/api/v1/jamf-pro-version

# Test SOFA feed
curl -I https://sofafeed.macadmins.io/v1/macos_data_feed.json

# Check local firewall (macOS)
sudo pfctl -s rules

# Check macOS firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Check Linux firewall
sudo iptables -L
```

## Network Diagnostics

### Comprehensive Network Test

Save as `network_test.py`:

```python
#!/usr/bin/env python3
"""Network connectivity test for JamfMCP."""

import socket
import ssl
import urllib.parse
import subprocess
import sys

def test_dns(hostname):
    """Test DNS resolution."""
    print(f"\n1. Testing DNS resolution for {hostname}...")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ Resolved to: {ip}")
        return ip
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        return None

def test_port(hostname, port=443):
    """Test port connectivity."""
    print(f"\n2. Testing port {port} connectivity...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = sock.connect_ex((hostname, port))
        if result == 0:
            print(f"✅ Port {port} is open")
            return True
        else:
            print(f"❌ Port {port} is closed or filtered")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    finally:
        sock.close()

def test_ssl(hostname, port=443):
    """Test SSL/TLS connection."""
    print(f"\n3. Testing SSL/TLS connection...")
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"✅ SSL/TLS connection successful")
                print(f"   Protocol: {ssock.version()}")
                print(f"   Cipher: {ssock.cipher()[0]}")
                cert = ssock.getpeercert()
                print(f"   Certificate CN: {cert['subject'][0][0][1]}")
                return True
    except Exception as e:
        print(f"❌ SSL/TLS connection failed: {e}")
        return False

def test_http(url):
    """Test HTTP(S) request."""
    print(f"\n4. Testing HTTPS request to {url}...")
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'JamfMCP/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"✅ HTTPS request successful")
            print(f"   Status: {response.status}")
            print(f"   Server: {response.headers.get('Server', 'Unknown')}")
            return True
    except Exception as e:
        print(f"❌ HTTPS request failed: {e}")
        return False

def test_traceroute(hostname):
    """Run traceroute."""
    print(f"\n5. Running traceroute to {hostname}...")
    try:
        if sys.platform == "win32":
            cmd = ["tracert", "-h", "10", hostname]
        else:
            cmd = ["traceroute", "-m", "10", hostname]

        subprocess.run(cmd, timeout=30)
    except FileNotFoundError:
        print("⚠️  Traceroute command not found")
    except subprocess.TimeoutExpired:
        print("⚠️  Traceroute timed out")
    except Exception as e:
        print(f"⚠️  Traceroute failed: {e}")

def main():
    """Run all network tests."""
    print("JamfMCP Network Connectivity Test")
    print("=" * 50)

    # Get Jamf URL
    jamf_url = input("Enter your Jamf Pro URL: ").strip()
    if not jamf_url:
        print("❌ No URL provided")
        return

    # Parse URL
    if not jamf_url.startswith(('http://', 'https://')):
        jamf_url = f"https://{jamf_url}"

    parsed = urllib.parse.urlparse(jamf_url)
    hostname = parsed.hostname
    port = parsed.port or 443

    print(f"\nTesting connectivity to: {hostname}:{port}")

    # Run tests
    ip = test_dns(hostname)
    if ip:
        port_ok = test_port(hostname, port)
        if port_ok:
            ssl_ok = test_ssl(hostname, port)
            test_http(f"{parsed.scheme}://{hostname}:{port}/api/v1/jamf-pro-version")

    # Test SOFA feed
    print("\n" + "=" * 50)
    print("Testing SOFA feed connectivity...")
    test_dns("sofafeed.macadmins.io")
    test_port("sofafeed.macadmins.io", 443)
    test_http("https://sofafeed.macadmins.io/v1/macos_data_feed.json")

    # Optional traceroute
    if input("\nRun traceroute? (y/n): ").lower() == 'y':
        test_traceroute(hostname)

    print("\n" + "=" * 50)
    print("Network tests complete!")

if __name__ == "__main__":
    main()
```

## Performance Issues

### Slow Response Times

**Symptoms:**
- Commands take long to complete
- Timeouts on large requests
- Inconsistent performance

**Diagnostics:**

```bash
# Measure response time
time curl -o /dev/null -s -w '%{time_total}\n' \
  https://your-server.com/api/v1/jamf-pro-version

# Check bandwidth
# Install speedtest-cli first
speedtest-cli

# Monitor network usage
# macOS
nettop -m tcp
# Linux
nethogs
```

**Solutions:**

1. **Reduce Data Requested**:
   ```python
   # Request only needed sections
   inventory = await get_computer_inventory(
       serial="ABC123",
       sections=["GENERAL", "HARDWARE"]  # Not "ALL"
   )
   ```

2. **Check Jamf Pro Performance**:
   - Review Jamf Pro server specs
   - Check database performance
   - Monitor during off-peak hours

3. **Implement Caching**:
   - Cache SOFA feed data
   - Cache static data locally

## Regional Issues

### Geographic Latency

**For Jamf Cloud customers:**

```bash
# Check which region you're in
nslookup your-instance.jamfcloud.com

# Typical regions:
# - Americas: us-east-1, us-west-2
# - Europe: eu-central-1, eu-west-1
# - APAC: ap-southeast-2
```

**High Latency Solutions:**
1. Check with Jamf about regional options
2. Implement local caching
3. Batch operations when possible

## Advanced Debugging

### Packet Capture

```bash
# Capture traffic (macOS/Linux)
sudo tcpdump -i any -w jamf.pcap host your-server.com

# Analyze with Wireshark
wireshark jamf.pcap

# Quick TLS handshake check
sudo tcpdump -i any -s 0 -w - host your-server.com | \
  grep -E "Client Hello|Server Hello"
```

### MTU Issues

```bash
# Check MTU
ping -D -s 1472 your-server.com

# Find optimal MTU
for size in {1500..1200..10}; do
    ping -D -s $size -c 1 your-server.com >/dev/null 2>&1 && \
    echo "MTU: $((size + 28))" && break
done
```

## When Network is Fine

If network tests pass but JamfMCP still fails:

1. **Check Authentication**: See [Authentication Troubleshooting](authentication)
2. **Verify API Endpoints**: Ensure Jamf Pro version supports required APIs
3. **Review Rate Limits**: Check if hitting API rate limits
4. **Check Server Load**: Jamf Pro might be overloaded

## Getting Help

When reporting connectivity issues, provide:

1. **Network test results** from diagnostic script
2. **Traceroute output** to Jamf server
3. **Error messages** including full stack trace
4. **Environment details**:
   - OS and version
   - Network type (corporate, home, VPN)
   - Proxy configuration if any
5. **Timing information**:
   - When it works vs. when it fails
   - Consistency of the issue

:::{seealso}
- [Jamf Cloud Architecture](https://docs.jamf.com/technical-papers/jamf-pro/jamf-cloud-architecture/)
- [FastMCP Networking](https://gofastmcp.com/servers/deployment#networking)
- [Python httpx Documentation](https://www.python-httpx.org/)
:::
