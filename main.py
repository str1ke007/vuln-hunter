import argparse
import textwrap
from colorama import init, Fore
from modules.port_scanner import PortScanner
from modules.web_scanner import WebScanner

init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description=("Vuln-Hunter"), epilog=textwrap.dedent(f"""
            {Fore.RESET}Example usage:
            {Fore.GREEN}/path/to/venv/python3 main.py <target_ip_or_domain> -db {Fore.YELLOW}exploitdb.csv,securityfocus.csv{Fore.RESET} | 
            {Fore.GREEN}/path/to/venv/python3 main.py <target_ip_or_domain> -v -db {Fore.YELLOW}securityfocus.csv{Fore.RESET} | 
            {Fore.GREEN}/path/to/venv/python3 main.py <target_ip_or_domain> -v"""))
    parser.add_argument("target", help="IP address or domain name to scan")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-db", "--database", help=f"Add one database from an arsenal available here(to reduce the output): {Fore.BLUE}[scipvuldb.csv securityfocus.csv xforce.csv exploitdb.csv{Fore.YELLOW}(default){Fore.BLUE} openvas.csv securitytracker.csv osvdb.csv]")
    args = parser.parse_args()

    print(Fore.GREEN + "Welcome to the Comprehensive Vulnerability Scanner")
    print(Fore.YELLOW + f"Scanning target: {args.target}")

    # Port Scanning and Service-Specific NSE Scans
    port_scanner = PortScanner(args.target, args.database)
    port_scanner.scan()
    
    # Run vulscan for all open ports in parallel
    port_scanner.run_vulscan()
    port_scanner.print_results()

    # Web Scanning
    web_scanner = WebScanner(args.target)
    web_scanner.scan()
    web_results = web_scanner.get_results()

    # Display web scanning results
    print(Fore.CYAN + "\nWeb Scanning Results:")
    for result in web_results:
        print(result)

if __name__ == "__main__":
    main()
