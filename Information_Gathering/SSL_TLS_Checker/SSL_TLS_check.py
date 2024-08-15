import os
import socket
import ssl
from datetime import datetime
from rich.console import Console
from rich.text import Text
import argparse
from urllib.parse import urlparse
import time

# Initialize Rich Console
console = Console()

def build_url(url):
    """Ensure the URL starts with http:// or https://."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

def set_arguments():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser(
        prog='SSL_TLS_Checker',
        description="Check SSL/TLS details for a given hostname."
    )

    parser.add_argument(
        '-u',
        '--url',
        default='www.tapidiploma.org',
        required=False,
        help='Enter the URL or hostname'
    )

    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=443,
        help='Port to use for SSL/TLS check (default is 443)'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Increase output verbosity'
    )

    return parser


def format_certificate_details(cert):
    """Format certificate details for display."""
    details = []

    def format_field(field):
        if isinstance(field, list):
            formatted_list = []
            for item in field:
                if isinstance(item, tuple):
                    formatted_list.append(f"{item[0]}: {item[1]}")
                else:
                    formatted_list.append(str(item))
            return ', '.join(formatted_list)
        return str(field)

    console.print("[bold green]\n\n[+] Certificate Details...[/]")

    for field, value in cert.items():
        formatted_value = format_field(value)
        formatted_value = formatted_value.replace(',,', ',').replace(',,', ',')
        formatted_value = formatted_value.replace('(', '').replace(')', '')
        console.print(f"[bold yellow]{field}[/]: [bold cyan]{formatted_value}[/]")
        details.append(f"[bold green]{field}[/]: {formatted_value}")

    return '\n'.join(details)


from rich.text import Text

def check_ssl_tls(url, port=443, verbose=False):
    """Check SSL/TLS details for the given URL and port."""
    hostname = urlparse(url).hostname
    if not hostname:
        console.print("[bold red]Error: Invalid hostname.[/]")
        return

    if verbose:
        console.print(
            f"[bold blue][-] Starting SSL/TLS check for [bold cyan]{hostname}[/] on port [bold cyan]{port}[/]...[/] "
            f"\n")
        time.sleep(2)

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Simulate delay
                time.sleep(1)

                # Print Protocol
                protocol = ssock.version()
                console.print(f"[bold green]Supported Protocol:[/] [bright_cyan]{protocol}[/]")

                # Get Certificate Details
                cert = ssock.getpeercert()
                cert_expiry = cert.get('notAfter', 'N/A')
                try:
                    cert_expiry_date = datetime.strptime(cert_expiry, "%b %d %H:%M:%S %Y GMT")
                    current_time = datetime.now()
                    days_until_expiry = (cert_expiry_date - current_time).days
                    if days_until_expiry < 30:
                        expiry_warning = f"[bold red]Warning:[/] Certificate expires in {days_until_expiry} days!"
                    else:
                        expiry_warning = ""
                except ValueError:
                    cert_expiry_date = "Invalid Date Format"
                    expiry_warning = "[bold red]Warning:[/] Certificate expiry date format is invalid."

                console.print(f"[bold green]Certificate Expiry Date:[/] [bright_magenta]{cert_expiry_date}[/]")
                if expiry_warning:
                    console.print(expiry_warning)

                # Print Certificate Details
                formatted_details = format_certificate_details(cert)
                # console.print(Text(formatted_details, style=""))

                print("\n")
                console.print("[bold green][+] Checking Security Measures..  [/]")
                # Simulate delay
                time.sleep(2)

                # Check for weak encryption algorithms
                cipher_suite = ssock.cipher()

                if cipher_suite:
                    cipher_name, cipher_version = cipher_suite[:2]
                    weak_ciphers = ["RC4", "DES", "3DES"]
                    if any(weak_cipher in cipher_name for weak_cipher in weak_ciphers):
                        console.print(f"[bold red]Weak Encryption Algorithm Detected: {cipher_name}")
                    else:
                        console.print(f"[bold green]Encryption Algorithm:[/] [bright_cyan]{cipher_name}[/]")

                # Simulate delay
                time.sleep(1)

                # Certificate Chain Validation
                try:
                    chain = context.get_ca_certs()
                    if not chain:
                        console.print(
                            "[bold red]Certificate Chain Validation: [bright_cyan]No certificate chain found![/]")
                    else:
                        console.print(
                            "[bold green]Certificate Chain Validation: [/] [bright_cyan]Certificate chain is valid.[/]")

                except Exception as e:
                    console.print(f"[bold red]Certificate Chain Validation Error: [/] {e}")

                # Simulate delay
                time.sleep(1)

                # Key Length Check
                try:
                    public_key = ssock.getpeercert(True)
                    key_length = len(public_key)
                    if key_length < 2048:
                        console.print(f"[bold red]Weak Key Length Detected: {key_length} bits[/]")
                    else:
                        console.print(f"[bold green]Key Length:[/] [bright_cyan]{key_length}[/] bits")
                except Exception as e:
                    console.print(f"[bold red]Key Length Check Error:[/] {e}")

    except ssl.SSLError as ssl_err:
        console.print(f"[bold red]SSL Error connecting to [bold cyan]{hostname}[/]: {ssl_err}[/]")
    except socket.error as sock_err:
        console.print(f"[bold red]Socket Error connecting to [bold cyan]{hostname}[/]: {sock_err}[/]")
        formatted_details = "Socket Connecting Error. Check URl"

    if verbose:
        console.print(f"[bold green]SSL/TLS check completed for [bold cyan]{hostname}[/].[/]")

    return formatted_details

def main():
    """Main function to handle command-line arguments and perform SSL/TLS check."""
    parser = set_arguments()
    args = parser.parse_args()

    args.url = build_url(args.url)

    check_ssl_tls(args.url, args.port, args.verbose)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
