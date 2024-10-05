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
