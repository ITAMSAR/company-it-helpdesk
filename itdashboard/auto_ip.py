"""
Auto IP Detection untuk Django
Automatically detect local IP address untuk QR code system
"""

import socket
import subprocess
import re
import platform

def get_local_ip():
    """
    Auto detect local IP address menggunakan multiple methods
    Returns: string IP address (e.g., "192.168.100.89")
    """
    
    # Method 1: Connect to external server (paling reliable)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        
        # Validate IP format
        if _is_valid_ip(ip) and not ip.startswith('127.'):
            return ip
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Parse system network commands
    try:
        if platform.system() == "Windows":
            return _get_ip_windows()
        else:
            return _get_ip_linux()
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Method 3: Socket gethostname (fallback)
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if _is_valid_ip(ip) and not ip.startswith('127.'):
            return ip
    except Exception as e:
        print(f"Method 3 failed: {e}")
    
    # Method 4: Last resort - return common default
    print("All methods failed, using fallback IP")
    return "192.168.100.89"

def _get_ip_windows():
    """Get IP on Windows using ipconfig"""
    result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
    lines = result.stdout.split('\n')
    
    # Look for WiFi adapter first
    wifi_keywords = ['Wireless LAN adapter Wi-Fi:', 'Wi-Fi:', 'WiFi', 'Wireless']
    
    for keyword in wifi_keywords:
        for i, line in enumerate(lines):
            if keyword in line and 'adapter' in line.lower():
                # Found WiFi adapter, look for IPv4 in next 15 lines
                for j in range(i, min(i + 15, len(lines))):
                    if 'IPv4 Address' in lines[j] or 'IP Address' in lines[j]:
                        # Extract IP using regex
                        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', lines[j])
                        if match:
                            ip = match.group(1)
                            if _is_valid_ip(ip) and not ip.startswith('127.'):
                                return ip
    
    # Fallback: look for any IPv4 address
    for line in lines:
        if 'IPv4 Address' in line:
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            if match:
                ip = match.group(1)
                if _is_valid_ip(ip) and not ip.startswith('127.'):
                    return ip
    
    raise Exception("No valid IP found in ipconfig")

def _get_ip_linux():
    """Get IP on Linux/Mac using ifconfig or ip"""
    try:
        # Try ifconfig first
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        output = result.stdout
    except:
        try:
            # Try ip command
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            output = result.stdout
        except:
            raise Exception("Neither ifconfig nor ip command available")
    
    # Look for WiFi interfaces first
    wifi_patterns = [r'wlan\d+', r'wifi\d+', r'wlp\d+s\d+']
    
    for pattern in wifi_patterns:
        matches = re.finditer(pattern + r'.*?(?=\n\n|\n[^\s]|\Z)', output, re.DOTALL)
        for match in matches:
            interface_block = match.group(0)
            ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', interface_block)
            if ip_match:
                ip = ip_match.group(1)
                if _is_valid_ip(ip) and not ip.startswith('127.'):
                    return ip
    
    # Fallback: any non-loopback interface
    ip_matches = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', output)
    for ip in ip_matches:
        if _is_valid_ip(ip) and not ip.startswith('127.'):
            return ip
    
    raise Exception("No valid IP found in network interfaces")

def _is_valid_ip(ip):
    """Validate IP address format"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        for part in parts:
            num = int(part)
            if not 0 <= num <= 255:
                return False
        
        return True
    except:
        return False

def get_dynamic_allowed_hosts():
    """
    Get comprehensive list of allowed hosts including current IP
    Returns: list of hostnames/IPs
    """
    
    # Base hosts (always include)
    hosts = [
        'localhost', 
        '127.0.0.1', 
        '0.0.0.0',
        '*',  # Allow all (for development)
    ]
    
    try:
        # Get current IP
        current_ip = get_local_ip()
        hosts.append(current_ip)
        
        # Add common IP variations for same subnet
        ip_parts = current_ip.split('.')
        if len(ip_parts) == 4:
            base_network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
            
            # Add some common IPs in same subnet (not all 254, just common ones)
            common_endings = [1, 10, 50, 89, 100, 150, 200, 254]
            for ending in common_endings:
                hosts.append(f"{base_network}.{ending}")
        
        print(f"✅ Auto-detected IP: {current_ip}")
        
    except Exception as e:
        print(f"❌ Failed to auto-detect IP: {e}")
        
        # Add common IP ranges as fallback
        common_ranges = [
            '192.168.1', '192.168.0', '192.168.100', 
            '10.0.0', '172.16.0'
        ]
        
        for range_base in common_ranges:
            hosts.extend([
                f"{range_base}.1", f"{range_base}.10", f"{range_base}.50",
                f"{range_base}.89", f"{range_base}.100", f"{range_base}.200"
            ])
    
    # Remove duplicates and return
    return list(set(hosts))

def update_qr_code_with_current_ip(equipment_code):
    """
    Generate QR code URL with current IP
    Returns: complete URL string
    """
    try:
        current_ip = get_local_ip()
        url = f"http://{current_ip}:9000/item/{equipment_code}/"
        print(f"✅ QR URL generated: {url}")
        return url
    except Exception as e:
        print(f"❌ Failed to generate QR URL: {e}")
        # Fallback to localhost
        return f"http://localhost:9000/item/{equipment_code}/"

# Test function
def test_ip_detection():
    """Test all IP detection methods"""
    print("=== Testing IP Detection ===")
    
    print("Current IP:", get_local_ip())
    print("Allowed hosts:", get_dynamic_allowed_hosts()[:10])  # Show first 10
    print("Sample QR URL:", update_qr_code_with_current_ip("APM/TEST/001"))
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_ip_detection()