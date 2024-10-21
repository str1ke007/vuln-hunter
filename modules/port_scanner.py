import subprocess
import shlex
import time
from colorama import Fore, Style
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    def __init__(self, target, database=None):
        self.target = target
        self.results = []
        self.nse_results = {}
        self.open_ports = []
        self.database = database

    def scan(self):
        print(Fore.YELLOW + f"[*] Starting port scan on {self.target}")
        try:
            command = f"nmap -sV {shlex.quote(self.target)} -oX -"
            output = subprocess.check_output(shlex.split(command), universal_newlines=True)
            self.parse_nmap_output(output)
            self.open_ports = [result['port'] for result in self.results if result['state'] == 'open']
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error running nmap: {e}")

    def parse_nmap_output(self, output):
        root = ET.fromstring(output)
        for port in root.findall(".//port"):
            port_id = port.get('portid')
            state = port.find('state').get('state')
            service = port.find('service')
            service_name = service.get('name', '').lower() if service is not None else "unknown"
            service_version = service.get('version', '') if service is not None else ""
            self.results.append({
                'port': port_id,
                'state': state,
                'service': service_name,
                'version': service_version
            })

    def run_vulscan(self):
        print(Fore.YELLOW + f"[*] Starting vulnerability scan on open ports")
        with ThreadPoolExecutor(max_workers=len(self.open_ports)) as executor:
            future_to_port = {executor.submit(self._run_vulscan_for_port, port): port for port in self.open_ports}
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    self.nse_results[port] = future.result()
                except Exception as exc:
                    print(Fore.RED + f"Error scanning port {port}: {exc}")

    def _run_vulscan_for_port(self, port):
        db_arg = f"--script-args=vulscandb={self.database}" if self.database else "--script-args=vulscandb=exploitdb.csv"
        command = f"nmap -sV -p{port} --script=vulscan/vulscan.nse {db_arg} {shlex.quote(self.target)}"
        try:
            output = subprocess.check_output(shlex.split(command), universal_newlines=True)
            return self.parse_vulscan_output(output)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error running vulscan for port {port}: {e}")
            return []

    def parse_vulscan_output(self, output):
        parsed_results = []
        capture = True
        for line in output.split('\n'):
            line = line.strip()
            if capture:
                if line:
                    # Stop capturing if we hit a line that likely indicates the end of the vulnerability information
                    if line.startswith("MAC Address") or line.startswith("Service Info"):
                        break
                    parsed_results.append(line)
        return parsed_results

    def print_results(self):
        print(Fore.CYAN + Style.BRIGHT + "\nPort Scanning Results:")
        for result in self.results:
            print(f"Port {result['port']}: {Fore.GREEN if result['state'] == 'open' else Fore.RED}{result['state']} - {Fore.YELLOW}{result['service']} {result['version']}")
        print(Fore.CYAN + Style.BRIGHT + "\nVulnerability Scan Results:")
        for port, results in self.nse_results.items():
            print(Fore.GREEN + f"\nResults for port {port}:")
            for result in results:
                if "CRITICAL" in result:
                    print(Fore.RED + Style.BRIGHT + result)
                elif "HIGH" in result:
                    print(Fore.YELLOW + result)
                else:
                    print(Fore.BLUE + result)
        print(Style.RESET_ALL)
