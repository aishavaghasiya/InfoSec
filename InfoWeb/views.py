from django.shortcuts import render
import urllib.parse
from .models import contactUs,UserProfile1
import webbrowser
import re
import ipaddress
import nmap
import os
import subprocess
import random
import requests

# Render Static Pages

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    success_message = None

    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("message")

        if not name or not surname or not email or not mobile or not message:
            error = "All fields are required!"
            return render(request, "contact.html", {"error": error})
        
        contactUs.objects.create(name=name, surname=surname, email=email, mobile=mobile, message=message)

        success_message = "Your message has been successfully stored!"
        
    return render(request, 'contact.html', {"success_message": success_message} )

# Validate IP Address (IPv4 & IPv6)
def validate_ip(user_ip):
    """Check if the input is a valid IPv4 or IPv6 address."""
    if not user_ip:
        return False, " No IP address provided!"

    try:
        ip = ipaddress.ip_address(user_ip)
        if isinstance(ip, ipaddress.IPv4Address):
            return True, None
        elif isinstance(ip, ipaddress.IPv6Address):
            return True, None
    except ValueError:
        return False, f" Your enterd IP is not a valid IP address Eneter valid IP address for scan !!"

# Scan IP using Nmap
def scan_ip(valid_ip, scan_type="quick"):
    """Perform an Nmap scan with different scan types."""
    nm = nmap.PortScanner()

    scan_options = {
        "quick": "-T4 -F",
        "detailed": "-A -Pn",
        "ports": "-p 1-65535 -T4",
        "vuln": "--script=vuln",
        "os": "-O -Pn --osscan-guess --script banner",
        "nse": "--script=safe,default,http-title,ssh-auth-methods"
    }

    if scan_type not in scan_options:
        return [{"error": "Invalid scan type selected!"}]

    print(f"🔍 Running Scan on {valid_ip} with mode: {scan_type}")

    try:
        nm.scan(valid_ip, arguments=scan_options[scan_type], timeout=600)
    except Exception as e:
        return [{"error": f"❌ Scan Failed: {str(e)}"}]

    # Parse Scan Results
    result = []
    try:
        if scan_type == "os":
            os_info = nm[valid_ip].get("osmatch", [])
            if os_info:
                result.append({"os": os_info[0]["name"]})
            else:
                result.append({"error": "❌ OS detection failed. Try running as root."})
        elif scan_type == "nse":
            script_results = nm[valid_ip].get("hostscript", [])
            if script_results:
                for script in script_results:
                    result.append({"script": script["id"], "output": script["output"]})
            else:
                result.append({"error": "❌ No NSE script results available."})
        else:
            for protocol in nm[valid_ip].all_protocols():
                for port in nm[valid_ip][protocol].keys():
                    result.append({
                        "port": port,
                        "protocol": protocol,
                        "state": nm[valid_ip][protocol][port]["state"],
                        "service": nm[valid_ip][protocol][port]["name"]
                    })
    except KeyError:
        result.append({"error": "❌ No open ports found or host is down."})

    return result

# Handle IP Validation & Scanning View
def scann(request):
    """Handles IP validation, scanning, and sends results to the webpage."""
    valid_ip_message = None
    scan_results = None
    scan_type = "quick"

    if request.method == "POST":
        user_ip = request.POST.get("ipAddress", "").strip()
        scan_type = request.POST.get("scanType", "quick")

        is_valid, valid_ip_message = validate_ip(user_ip)

        if is_valid:
            scan_results = scan_ip(user_ip, scan_type)

    return render(request, 'scann.html', {
        "valid_ip": valid_ip_message, 
        "scan_results": scan_results, 
        "scanType": scan_type,
    })

# LAN scanning functions

def validate_local_ip(input_ip):
    """
    Validate if the given IP is a private (local) IP address.
    Returns None if valid, otherwise returns an error message.
    """
    try:
        ip_obj = ipaddress.ip_address(input_ip)
        if ip_obj.is_private:
            return None  # IP is valid
        else:
            return f" Your enterd IP is not a valid IP address Eneter valid IP address for scan !!"
    except ValueError:
        return f" Your enterd IP is not a valid IP address Eneter valid IP address for scan !!"

def get_network_range(input_ip):
    """
    Get the network range (e.g., 192.168.1.0/24) based on the entered IP.
    """
    ip_obj = ipaddress.ip_address(input_ip)
    if ip_obj.version == 4:
        return f"{ip_obj.exploded.rsplit('.', 1)[0]}.0/24"
    return None

def scan_network(network_range):
    """
    Scan the local network and get a list of connected devices.
    Returns a list of dictionaries with IP and MAC addresses.
    """
    devices = []
    nm = nmap.PortScanner()

    try:
        print(f"🔍 Scanning network: {network_range}")
        nm.scan(hosts=network_range, arguments="-sn")  # Ping scan

        for host in nm.all_hosts():
            ip_address = nm[host]["addresses"].get("ipv4", "Unknown IP")
            mac_address = nm[host]["addresses"].get("mac", "Unknown MAC")

            devices.append({
                "ip": ip_address,
                "mac": mac_address
            })

    except Exception as e:
        print(f"❌ Error scanning network: {e}")

    return devices

def get_connected_devices():
    """
    Alternative method to scan network using ARP (for Windows/Linux).
    """
    devices = []

    try:
        if os.name == "nt":  # Windows
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        else:  # Linux/macOS
            result = subprocess.run(["arp", "-n"], capture_output=True, text=True)

        lines = result.stdout.split("\n")

        for line in lines:
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([\w:-]+)", line)
            if match:
                ip, mac = match.groups()
                mac = mac.upper().replace("-", ":")  # Normalize MAC address

                devices.append({"ip": ip, "mac": mac})

    except Exception as e:
        print(f"❌ Error running ARP command: {e}")

    return devices

def lan_scann(request):
    """
    Django view to validate IP and scan network if valid.
    """
    devices = []
    error_message = None

    if request.method == "POST":
        input_ip = request.POST.get("ip-Address", "").strip()
        error_message = validate_local_ip(input_ip)

        if error_message is None:
            network_range = get_network_range(input_ip)
            if network_range:
                devices = scan_network(network_range)  # Use nmap for scanning

                # If nmap fails, try ARP as a fallback
                if not devices:
                    print("Nmap failed. Trying ARP scan as a fallback...")
                    devices = get_connected_devices()

    return render(request, 'lan-scann.html', {"devices": devices, "error_message": error_message})

# password chaking service start from hear

STRENGTH_LEVELS = {
    'Very Weak': ('red', 20),
    'Weak': ('orange', 40),
    'Moderate': ('yellow', 60),
    'Strong': ('blue', 80),
    'Very Strong': ('green', 100)
}

def check_password_strength(password):
    strength = "Very Weak"
    score = 0
    
    # Criteria for password strength
    if len(password) >= 8:
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[@$!%*?&#]", password):
        score += 1
    
    # Assign strength levels
    if score == 1:
        strength = "Very Weak"
    elif score == 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    elif score == 5:
        strength = "Very Strong"
    
    return strength, STRENGTH_LEVELS[strength][0], STRENGTH_LEVELS[strength][1]

def suggest_password():
    words = ["Secure", "Cyber", "Shield", "Strong", "Pass", "Guard", "Lock","User","Exception","Creep","Passcode"]
    special_chars = "@$!%*?&#"
    
    suggestion = random.choice(words) + str(random.randint(10, 99)) + random.choice(special_chars) + random.choice(words)
    return suggestion

def pass_scann(request):
    strength = None
    color = None
    progress = 0
    suggestion = None
    
    if request.method == "POST":
        user_password = request.POST.get("userpass")
        strength, color, progress = check_password_strength(user_password)
        suggestion = suggest_password()
    
    return render(request, "pass-scann.html", {"strength": strength, "color": color, "progress": progress, "suggestion": suggestion})

# subdomain finder service start from here
# def domain_enum(request):
#     return render(request, "domain-enum.html")

COMMON_SUBDOMAINS = ['www', 'mail','suport','status','doc','documents', 'ftp', 'blog', 'shop', 'dev', 'test','mail2','ns2','ns1','localhost'
,'m','mobile','ns3','smtp','search','api','dev','secure','webmail','admin','img','news','sms','marketing','test','video','www2'
,'media','static','ads','mail2','beta','wap','blogs','download','dns1','www3','origin','shop','forum'
,'chat','www1','image','new','tv','dns','services','music','images','pay','ddrint','conc']

def get_status_code(url):
    """Function to get the HTTP status code of a given URL."""
    try:
        response = requests.get(url, timeout=3)
        return response.status_code
    except requests.RequestException:
        return "Failed"

def check_subdomains(domain):
    """Check status codes for the main domain and its subdomains."""
    results = []
    
    # Check main domain status
    main_url = f"https://{domain}"
    main_status = get_status_code(main_url)
    results.append({'subdomain': main_url, 'status': main_status})

    # Check common subdomains
    for sub in COMMON_SUBDOMAINS:
        subdomain_url = f"https://{sub}.{domain}"
        subdomain_status = get_status_code(subdomain_url)
        results.append({'subdomain': subdomain_url, 'status': subdomain_status})
    
    return results

def domain_enum(request):
    results = []
    if request.method == "POST":
        domain = request.POST.get("domain")  # Get domain from form input
        if domain:
            results = check_subdomains(domain)

    return render(request, "domain-enum.html", {"results": results})

# Google Dork options
DORKS = {
    "Publicly exposed documents": 'site:{} ext:pdf OR ext:doc OR ext:xls',
    "Directory listing vulnerabilities": 'site:{} intitle:"index of"',
    "Configuration files exposed": 'site:{} ext:ini OR ext:conf OR ext:log',
    "Database files exposed": 'site:{} ext:sql OR ext:db',
    "Log files exposed": 'site:{} ext:log',
    "Backup and old files": 'site:{} ext:bak OR ext:old OR ext:backup',
    "Login pages": 'site:{} inurl:login',
    "SQL errors": 'site:{} intext:"SQL syntax error"',
    "PHP errors / warnings": 'site:{} intext:"Warning: " OR intext:"Fatal error: "',
    "phpinfo()": 'site:{} inurl:phpinfo',
    "Search pastebin.com / pasting sites": 'site:pastebin.com "{}"',
    "Search github.com and gitlab.com": 'site:github.com "{}" OR site:gitlab.com "{}"',
    "Search stackoverflow.com": 'site:stackoverflow.com "{}"',
    "Signup pages": 'site:{} inurl:signup',
    "Find Subdomains": 'site:*.{} -www',
    "Find Sub-Subdomains": 'site:*.*.{}',
    "Search in Wayback Machine": 'site:web.archive.org/web/*/{}',
    "Show only IP addresses": 'site:{} -www -inurl:www',
}

def google_dork(request):
    if request.method == 'POST':
        target = request.POST.get('target')
        dork_type = request.POST.get('dork_type')

        if target and dork_type in DORKS:
            google_query = DORKS[dork_type].format(target)
            encoded_query = urllib.parse.quote(google_query)  # Encode for URL
            search_url = f"https://www.google.com/search?q={encoded_query}"

            # Open new browser window automatically
            webbrowser.open_new(search_url)

    return render(request, 'gdork.html', {'dorks': DORKS.keys()})


def Evo_os(request):
    return render(request, 'Evo-os.html')


def login(request):
    success_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")


        if not username or not email or not role or not password:
            error = "All fields are required!"
            return render(request, "login.html", {"error": error})

        # Save data
        UserProfile1.objects.create(
            username=username,
            email=email,
            role=role,
            password=password,
        )

        success_message = "Login successful!!"
    return render(request, 'login.html', {"success_message": success_message})
