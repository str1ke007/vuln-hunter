import subprocess
import re
import sys
import threading
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Read services to remove from remove.txt
def load_services_to_remove(filename='remove.txt'):
    try:
        with open(filename, 'r') as f:
            services_to_remove = [line.strip() for line in f.readlines()]
        return services_to_remove
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {filename} not found. Proceeding without removal list.")
        return []

def run_nmap_version_scan(target, output_container):
    try:
        # Running nmap scan with version detection and grepable output
        result = subprocess.run(['nmap', '-sV', '-oG', '-', target], capture_output=True, text=True)
        output_container['version_scan'] = result.stdout
    except Exception as e:
        print(f"{Fore.RED}Error running nmap version scan: {e}")
        sys.exit(1)

def run_nmap_ports_scan(target, output_container):
    try:
        # Running nmap to show services running on various ports and piping it through grep
        command = f"nmap -sV {target} | grep -E '^[0-9]+/tcp'"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        output_container['ports_scan'] = result.stdout
    except Exception as e:
        print(f"{Fore.RED}Error running nmap ports scan: {e}")
        sys.exit(1)

def clean_service_version(service, version):
    # Clean the version by removing unwanted characters and extra spaces
    service = service.strip()  # Remove leading/trailing whitespace
    version = re.sub(r'[^a-zA-Z0-9\.\-]', '', version).strip()  # Keep only valid characters in version

    # If the cleaned version becomes empty, search only the service name
    if not version:
        return service, None

    return service, version

def remove_service_substrings(service, services_to_remove):
    # Replace each service in the remove list with an empty string
    for remove_item in services_to_remove:
        service = re.sub(rf'\b{remove_item}\b', '', service, flags=re.IGNORECASE).strip()
    return service

def parse_nmap_output(output, services_to_remove):
    services = []
    # Use the provided regex to capture service names and versions
    service_regex = re.compile(r'(?<=//)([A-Za-z]+(?:\s[A-Za-z]+)*)\s([\d\.X\-\w]+)')
    
    # Parse each line of grepable output
    for line in output.splitlines():
        # Match the regex to capture service and version
        matches = service_regex.findall(line)
        for match in matches:
            service, version = match
            service, version = clean_service_version(service.strip(), version.strip())

            # Remove specific substrings (but not the entire service name)
            service = remove_service_substrings(service, services_to_remove)

            services.append((service, version))
    
    return services

def search_exploits(service, version):
    try:
        # If the version is None, search only by service
        if version:
            search_term = f"{service} {version}"
        else:
            search_term = service

        # Running searchsploit to find vulnerabilities
        result = subprocess.run(['searchsploit', search_term], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"{Fore.RED}Error running searchsploit: {e}")
        return ""

def main():
    # Load services to remove from remove.txt
    services_to_remove = load_services_to_remove('remove.txt')

    target = input("Enter the IP/Host/Domain: ")
    
    # Output containers to store results of the two nmap scans
    output_container = {'version_scan': None, 'ports_scan': None}

    # Create two threads to run nmap scans concurrently
    version_scan_thread = threading.Thread(target=run_nmap_version_scan, args=(target, output_container))
    ports_scan_thread = threading.Thread(target=run_nmap_ports_scan, args=(target, output_container))

    print(f"{Fore.BLUE}Running nmap scans on {target}...")
    
    # Start both threads
    version_scan_thread.start()
    ports_scan_thread.start()

    # Wait for both threads to finish
    version_scan_thread.join()
    ports_scan_thread.join()

    # Display the results of the second nmap scan (ports scan)
    print(f"{Fore.CYAN}Nmap Ports Scan (Services running on various ports):")
    print(f"{Fore.YELLOW}{output_container['ports_scan']}")

    # Parse and process the version scan output
    print(f"{Fore.CYAN}Parsing nmap version scan results...")
    services = parse_nmap_output(output_container['version_scan'], services_to_remove)

    if not services:
        print(f"{Fore.RED}No services found.")
        return

    for service, version in services:
        print(f"{Fore.GREEN}Searching vulnerabilities for {service} {version}...")
        vuln_info = search_exploits(service, version)
        if vuln_info:
            print(f"{Fore.YELLOW}Vulnerabilities found for {service} {version}:")
            print(vuln_info)
        else:
            print(f"{Fore.RED}No vulnerabilities found for {service} {version}.")

if __name__ == "__main__":
    main()
