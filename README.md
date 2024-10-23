# VulnHunter 🔎

## Description
A comprehensive vulnerability scanner that utilizes Nmap and the Vulscan NSE script to identify open ports and their associated vulnerabilities. This tool supports scanning using various vulnerability databases and provides detailed output for each identified issue.

## Features
- Scan IP addresses or domain names for open ports.
- Utilize multiple vulnerability databases:
  - scipvuldb.csv
  - securityfocus.csv
  - xforce.csv
  - exploitdb.csv (default)
  - openvas.csv
  - securitytracker.csv
  - osvdb.csv
- Enable verbose output for detailed scan information.
- Parse and display vulnerability information in a user-friendly format.

## Requirements
- Python 3.x
- Nmap
- Colorama
- Other dependencies (if any)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/str1ke007/vuln-hunter.git
   cd vuln-hunter
   ```

2. **Install required Python libraries**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔨 Usage

Run the scanner using the following command:

```bash
python3 src/main.py <target> -db <database>
```

Arguments
- ```<target>```: The IP address or domain name to scan.

- ```-db <database>```: Specify the vulnerability database to use (e.g., exploitdb.csv).

---

## 📝 To-Do

- Add more detailed vulnerability filtering options.
- Explore integration with external APIs for live vulnerability data.

---

## 🛡️ Disclaimer

This tool is intended for legal use only. The authors take no responsibility for any misuse or damage caused by this tool. Please ensure you have proper authorization before scanning any network or system.
