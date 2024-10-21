import subprocess
from colorama import Fore

class WebScanner:
    def __init__(self, target):
        self.target = target
        self.results = []

    def scan(self):
        print(Fore.YELLOW + f"[*] Starting web application scan on {self.target}")
        try:
            output = subprocess.check_output(
                ["dirb", f"http://{self.target}", "/usr/share/dirb/wordlists/common.txt"],
                universal_newlines=True,
                stderr=subprocess.DEVNULL
            )
            self.parse_dirb_output(output)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error running dirb: {e}")

    def parse_dirb_output(self, output):
        lines = output.split('\n')
        for line in lines:
            if line.startswith("+ http"):
                self.results.append(line.split()[1])  # Get the discovered URL

    def get_results(self):
        return self.results
