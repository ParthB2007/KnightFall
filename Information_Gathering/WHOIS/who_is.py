import os

import whois
import rich
from rich.console import Console
import argparse
import time
console = Console()
def set_arguments():
    parser = argparse.ArgumentParser(
        description="WHOIS Information Fetcher")

    parser.add_argument(
        '-u',
        '--url',
        type=str,
        required=True,
        help='Enter URL to fetch WHOIS details'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Print detailed WHOIS information')

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=True,
        help='File path to save WHOIS details')
    return parser.parse_args()

def fetch_whois(domain):
    return whois.whois(domain)

def format_whois_info(domain, verbose):
    res = fetch_whois(domain)
    result = []

    if not res:
        return "[bold red]Failed to retrieve WHOIS information.[/bold red]"

    if verbose:
        result.append(f"[bold cyan]\n\n[+] WHOIS Information for {domain}:[/bold cyan]\n")
        for key, value in res.items():
            if isinstance(value, list):
                value = "\n".join(map(str, value))
            result.append(f"[bold yellow]{key}:[/bold yellow] {value}\n")
    else:
        result.append(f"[bold cyan]\n\n[+] WHOIS Information for {domain}:[/bold cyan]")
        result.append(f"[bold yellow]Registrar:[/bold yellow] {res.registrar if res.registrar else 'N/A'}")
        creation_date = res.creation_date if res.creation_date else 'N/A'
        expiration_date = res.expiration_date if res.expiration_date else 'N/A'
        updated_date = res.updated_date if res.updated_date else 'N/A'
        result.append(f"[bold yellow]Creation Date:[/bold yellow] {creation_date}")
        result.append(f"[bold yellow]Expiration Date:[/bold yellow] {expiration_date}")
        result.append(f"[bold yellow]Updated Date:[/bold yellow] {updated_date}")
        name_servers = "\n".join(res.name_servers) if res.name_servers else 'N/A'
        result.append(f"[bold yellow]Name Servers:[/bold yellow] {name_servers}")
        result.append(f"[bold yellow]Status:[/bold yellow] {res.status if res.status else 'N/A'}")
        result.append(f"[bold yellow]Organization:[/bold yellow] {res.org if res.org else 'N/A'}")

    return "\n".join(result)

def display_whois_info(domain, verbose, output_file):


    formatted_info = format_whois_info(domain, verbose)


    # Print to the console
    console.print(formatted_info)

    write_into_file(output_file,formatted_info)
    # Save to a file if specified
def write_into_file(output_file,formatted_info):
    if output_file:
        with open(output_file, 'w') as file:
            file.write(formatted_info)
        console.print(f"[bold green][-] WHOIS information saved to[/bold green] {output_file}")

def main():
    start_time = time.time()
    args = set_arguments()

    console.print(f"[-] Connecting to the : [bold cyan]{args.url}[/]")
    time.sleep(2)
    display_whois_info(args.url, args.verbose, args.output)

    console.print(f"Time Taken : {time.time()-start_time}")
if __name__ == '__main__':
    os.system('cls')
    main()
