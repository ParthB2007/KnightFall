import os
import whois
import rich
from rich.console import Console
import argparse
import time

console = Console()

def set_arguments():
    parser = argparse.ArgumentParser(description="WHOIS Information Fetcher")
    parser.add_argument('-u', '--url', type=str, required=True, help='Enter URL to fetch WHOIS details')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed WHOIS information')
    parser.add_argument('-o', '--output', type=str, required=True, default='./WHOIS_info.txt', help='File path to save WHOIS details')
    return parser.parse_args()

def fetch_whois(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        console.print(f"[bold red]Error fetching WHOIS data: {e}[/bold red]")
        return None

def format_whois_info(domain, verbose):
    res = fetch_whois(domain)
    result = []

    if not res:
        return "[bold red]Failed to retrieve WHOIS information.[/bold red]"

    if verbose:
        console.print(f"[bold green]\n[+] WHOIS Information...[/]")
        for key, value in res.items():
            if isinstance(value, list):
                value = " , ".join(map(str, value))
            status = res.status if res.status else 'N/A'
            status = ",\n        ".join(status)
            result.append(f"[bold yellow]{key}:[/] {value}")
    else:
        result.append(f"[bold yellow]Registrar:[/] [bold cyan]{res.registrar if res.registrar else 'N/A'}[/]")
        creation_date = res.creation_date if res.creation_date else 'N/A'
        expiration_date = res.expiration_date if res.expiration_date else 'N/A'
        updated_date = res.updated_date if res.updated_date else 'N/A'
        result.append(f"[bold yellow]Creation Date:[/] [bold cyan]{creation_date}[/]")
        result.append(f"[bold yellow]Expiration Date:[/] [bold cyan]{expiration_date}[/]")
        result.append(f"[bold yellow]Updated Date:[/] [bold cyan]{updated_date}[/]")
        name_servers = "\n".join(res.name_servers) if res.name_servers else 'N/A'
        result.append(f"[bold yellow]Name Servers:[/] [bold cyan]{name_servers}[/]")
        status = res.status if res.status else 'N/A'
        status = ",\n        ".join(status)
        result.append(f"[bold yellow]Status:[/] [bold cyan]{status}[/]")
        result.append(f"[bold yellow]Organization:[/] [bold cyan]{res.org if res.org else 'N/A'}[/]")

    return "\n".join(result)

def display_whois_info(domain, verbose):
    formatted_info = format_whois_info(domain, verbose)
    console.print(formatted_info)
    return formatted_info

def write_into_file(output_file, formatted_info):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Clean up rich text formatting for plain text file
    formatted_info = formatted_info.replace('[bold yellow]', '').replace('[bold cyan]', '').replace('[/]', '')

    with open(output_file, 'w') as file:
        file.write(formatted_info)
    console.print(f"[bold green][-] WHOIS information saved to[/bold green] {output_file}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    start_time = time.time()
    args = set_arguments()

    console.print(f"[-] Connecting to: [bold cyan]{args.url}[/]")
    time.sleep(2)
    result = display_whois_info(args.url, args.verbose)

    if result:
        write_into_file(args.output, result)

    console.print(f"[bold blue][-] Time Taken:[/bold blue] {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
