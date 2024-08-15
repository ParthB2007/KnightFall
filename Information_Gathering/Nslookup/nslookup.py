import subprocess
import argparse
from rich.console import Console

console = Console()

def set_arguments():
    parser = argparse.ArgumentParser(
        prog='nslookup.py',
        description='Provide detailed Name Server information for a given website'
    )

    parser.add_argument(
        '-u',
        '--url',
        default='www.tapidiploma.org',
        help='Provide the URL for nslookup',
        required=False
    )

    return parser

def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

def parse_nslookup_output(output):
    lines = output.splitlines()
    parsed_output = {
        "Server": None,
        "Address": None,
        "Name": None,
        "Aliases": [],
        "Addresses": [],
        "Mail Exchange (MX)": [],
        "Other": []
    }

    for line in lines:
        if "Server:" in line:
            parsed_output["Server"] = line.split(":", 1)[1].strip()
        elif "Address:" in line and not parsed_output["Address"]:
            parsed_output["Address"] = line.split(":", 1)[1].strip()
        elif "Name:" in line:
            parsed_output["Name"] = line.split(":", 1)[1].strip()
        elif "canonical name" in line or "CNAME" in line:
            cname = line.split("=")[1].strip() if "=" in line else line.split()[-1]
            parsed_output["Aliases"].append(cname)
        elif "MX" in line or "mail exchanger" in line:
            parsed_output["Mail Exchange (MX)"].append(line.strip())
        elif "Address:" in line:
            parsed_output["Addresses"].append(line.split(":", 1)[1].strip())
        else:
            parsed_output["Other"].append(line.strip())

    return parsed_output

def nslookup(url):
    console.print(f"[bold yellow][+] Fetching NSLOOKUP information from[/] [bold cyan]{url}[/]")
    result = subprocess.run(['nslookup', url], capture_output=True, text=True)
    output = result.stdout

    parsed_output = parse_nslookup_output(output)

    if parsed_output["Server"]:
        console.print(f"[bold green][+] Server:[/] [bold white]{parsed_output['Server']}[/]")
    if parsed_output["Address"]:
        console.print(f"[bold green][+] Address:[/] [bold white]{parsed_output['Address']}[/]")
    if parsed_output["Name"]:
        console.print(f"[bold green][+] Name:[/] [bold white]{parsed_output['Name']}[/]")
    if parsed_output["Aliases"]:
        console.print(f"[bold green][+] Aliases (CNAME):[/]")
        for alias in parsed_output["Aliases"]:
            console.print(f"   [bold cyan]{alias}[/]")
    if parsed_output["Addresses"]:
        console.print(f"[bold green][+] Additional Addresses:[/]")
        for address in parsed_output["Addresses"]:
            console.print(f"   [bold cyan]{address}[/]")
    if parsed_output["Mail Exchange (MX)"]:
        console.print(f"[bold green][+] Mail Exchange (MX) Records:[/]")
        for mx_record in parsed_output["Mail Exchange (MX)"]:
            console.print(f"   [bold cyan]{mx_record}[/]")
    if parsed_output["Other"]:
        console.print(f"[bold yellow][+] Other Information:[/]")
        for info in parsed_output["Other"]:
            console.print(f"   [bold cyan]{info}[/]")

def main():
    parser = set_arguments()
    args = parser.parse_args()

    url = args.url

    console.print(f"[-] Building URL")
    url = build_url(url)

    console.print(f"[bold yellow][-] Connecting to website[/] [bold cyan]{url}[/]")

    nslookup(url)

if __name__ == '__main__':
    main()

