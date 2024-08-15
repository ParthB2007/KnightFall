import time
import socket
import builtwith
import argparse
import requests
from rich.console import Console
from rich.text import Text

# Initialize Rich Console
console = Console()


def set_arguments():
    parser = argparse.ArgumentParser(
        prog="Simple Technology Stack Detector.",
        description="Detect the technology stack used by a webpage."
    )


    parser.add_argument(
        '-u',
        '--url',
        required=True,
        help="Enter the webpage URL"
    )

    parser.add_argument(
        '-o',
        '--output',
        default='result.txt',
        help="Output file to save the results"
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Increase output verbosity"
    )

    return parser


def detect_technologies(url, verbose):
    if verbose:
        console.print(f"[bold blue][-] Detecting technologies used in [bright_cyan]{url}[/]...\n")

    time.sleep(1)
    # Use builtwith to detect technologies
    data = builtwith.parse(url)

   
    for key, value in data.items():
        console.print(f"[bright_yellow]{key}[/bright_yellow]: {', '.join(value)}")

    return data


def get_ip_address(url):
    hostname = url.replace("http://", "").replace("https://", "").split('/')[0]
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_server_headers(url):
    response = requests.head(url)
    return response.headers


def save_result(output, formatted_result, verbose):
    if verbose:
        console.print(f"\nSaving results to [bright_magenta]{output}[/]...")
    with open(output, 'w') as f:
        f.write(formatted_result)
    if verbose:
        console.print("[bright_magenta]Results saved successfully.[/]")


def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()


def main():
    parser = set_arguments()
    args = parser.parse_args()

    args.url = build_url(args.url)

    if args.verbose:
        console.print(f"Starting detection for [bright_cyan]{args.url}[/]...")

    result = detect_technologies(args.url, args.verbose)

    if args.verbose:
        console.print("[bright_magenta]\nDetection completed. Fetching additional information...[/]")

    ip_address = get_ip_address(args.url)
    server_headers = get_server_headers(args.url)

    if args.verbose:
        console.print(f"[bright_yellow]IP Address:[/bright_yellow] {ip_address}")
        console.print("[bright_yellow]Server Headers:[/bright_yellow]")
        for key, value in server_headers.items():
            console.print(f"[bright_yellow]{key}[/bright_yellow]: {value}")

    formatted_result = "\n".join(f"{key}: {', '.join(values)}" for key, values in result.items())
    formatted_result += f"\n\nIP Address: {ip_address}\n\nServer Headers:\n"
    formatted_result += "\n".join(f"{key}: {value}" for key, value in server_headers.items())

    save_result(args.output, formatted_result, args.verbose)

    if args.verbose:
        console.print(f"Process completed for [bright_cyan]{args.url}[/].")


if __name__ == '__main__':
    main()
