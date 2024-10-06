# VulnHunter 🔎

**VulnHunter** is a powerful multi-threaded vulnerability scanning tool designed to streamline the process of identifying exposed services, their versions, and known vulnerabilities for a given IP, host, or domain. With integrated Nmap scanning and SearchSploit querying, VulnHunter provides efficient results, helping cybersecurity enthusiasts, network administrators, and penetration testers stay ahead of potential threats.

---

## 🚀 Features
- **Multi-threaded scanning**: Runs multiple Nmap scans simultaneously to detect open ports and service versions for faster results.
- **Service and version detection**: Automatically detects and parses service names and versions using Nmap's version detection.
- **Vulnerability search**: Uses SearchSploit to search for known vulnerabilities based on the identified services and versions.
- **Custom service filtering**: Remove unwanted service names or substrings using a custom `remove.txt` file.
- **Color-coded output**: Easily identify important information through the use of color-coded results in the terminal.
- **Cross-platform**: Runs on most Linux-based systems with Python and required tools installed.

---

## 📜 Requirements

To run **VulnHunter**, you'll need the following:

- **Python 3.6+**
- **Nmap** installed and accessible from the command line
- **SearchSploit** installed (part of the Exploit-DB toolkit)
- **Grep** (for filtering ports in Nmap output)
- **Openpyxl** (if using Excel output, optional)

---

## 🔧 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/VulnHunter.git
    cd VulnHunter
    ```

2. **Install required Python libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Nmap and SearchSploit** if you don't have them:
    ```bash
    sudo apt-get install nmap
    sudo apt-get install exploitdb
    ```

4. **Create a `remove.txt` file** in the root directory to exclude unwanted services from Nmap output:
    ```bash
    touch remove.txt
    ```
    Example content for `remove.txt`:
    ```
    httpd
    smbd
    ```

---

## 🔨 Usage

To start scanning a target, run VulnHunter as follows:

```bash
python vuln_hunter.py
```

---

You will be prompted to enter an IP, host, or domain to scan. VulnHunter will then run two simultaneous Nmap scans:

    Service detection scan: Detects running services and versions.
    Ports scan: Displays open ports and corresponding services.

Once the services and versions are detected, VulnHunter will use SearchSploit to search for known vulnerabilities associated with those services.
## Example Output:
```bash
Running nmap scans on 192.168.1.1...

Nmap Ports Scan (Services running on various ports):
22/tcp  open   ssh    OpenSSH 7.9p1
80/tcp  open   http   Apache 2.4.29
3306/tcp open  mysql  MySQL 5.7.26

Parsing nmap version scan results...
Searching vulnerabilities for OpenSSH 7.9p1...
Vulnerabilities found for OpenSSH 7.9p1:
- OpenSSH 7.9p1 - Remote Code Execution (exploit/path)
- OpenSSH < 7.9p1 - Local Privilege Escalation (exploit/path)

No vulnerabilities found for Apache 2.4.29.
```

---

## ⚙️ Configuration
```remove.txt```:
This file contains a list of service substrings to exclude from the final parsed service list. Add unwanted services (e.g., ```httpd``` or ```smbd```) to the file, and VulnHunter will remove them during output parsing.

---

## 📝 To-Do

- Implement additional output formats (JSON, CSV).
- Add more detailed vulnerability filtering options.
- Explore integration with external APIs for live vulnerability data.

---

## 🛡️ Disclaimer

This tool is intended for legal use only. The authors take no responsibility for any misuse or damage caused by this tool. Please ensure you have proper authorization before scanning any network or system.
