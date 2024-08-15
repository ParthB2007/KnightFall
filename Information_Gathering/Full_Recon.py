import time
import argparse
import os
from rich.console import Console
from rich.text import Text

from Tech_Detector import tech_detector
from SSL_TLS_Checker import SSL_TLS_check
from WHOIS import who_is

# Initialize Rich Console
console = Console()

def set_argument():
    parser = argparse.ArgumentParser(
        prog='Full_Recon.py',
        description="Print all web recon results"
    )

    parser.add_argument(
        '-u',
        '--url',
        required=True,
        help='Enter URL'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Increase output verbosity'
    )

    parser.add_argument(
        '-f',
        '--file',
        default='./full_recon_data.txt',
        help='Write all the results to the file'
    )

    parser.add_argument(
        '-sp',
        '--start_port',
        default=1,
        required=False,
        type=int,
        help="Starting Port Number for open Port Scanning"
    )

    parser.add_argument(
        '-ep',
        '--end_port',
        default=1000,
        required=False,
        type=int,
        help="End Port Number for open Port Scanning"
    )

    parser.add_argument(
        '-p',
        '--protocol',
        default='tcp',
        type=str,
        help="Protocol for open Port Scanning (TCP, UDP, or BOTH)"
    )
    return parser

def append_data(path, data):
    with open(path, 'a') as file:
        file.write(data + "\n")

def delete_file_contents(path):
    with open(path, 'w'):
        pass

def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

def replace_color(data):
    import re
    # Strip Rich's color codes from the string
    data = re.sub(r'\[/?\w+.*?\]', '', data)
    data = data.replace('[/]','')
    return data

def tech_detect_recon(url, verbose):
    result = tech_detector.detect_technologies(url, verbose)
    formatted_result = Text()
    for key, values in result.items():
        formatted_result.append(f"{key}: ", style="bold bright_magenta")
        formatted_result.append(", ".join(values) + "\n", style="bold bright_white")
    return formatted_result.plain

def ssl_tls_recon(url, verbose):
    results = SSL_TLS_check.check_ssl_tls(url, verbose=verbose)
    results = replace_color(results)
    return results

def who_is_recon(url, verbose):
    whois_result = who_is.display_whois_info(url, verbose)
    whois_result = replace_color(whois_result)
    return whois_result

def full_recon_app(url, verbose):
    url = build_url(url)
    result = ""

    tech_result = tech_detect_recon(url, verbose)
    result += f"<h2>Technology Stack for {url}</h2>"
    result += "<hr>"
    result += f"<pre>{tech_result}</pre>"
    
    ssl_result = ssl_tls_recon(url, verbose)
    result += f"<h2>SSL/TLS Details for {url}</h2>"
    result += "<hr>"
    result += f"<pre>{ssl_result}</pre>"
    
    whois_result = who_is_recon(url, verbose)
    result += f"<h2>WHOIS Information for {url}</h2>"
    result += "<hr>"
    result += f"<pre>{whois_result}</pre>"

    return result

def main():
    start_time = time.time()
    parser = set_argument()
    args = parser.parse_args()

    args.url = build_url(args.url)

    if os.path.isfile(args.file):
        delete_file_contents(args.file)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    append_data(args.file, f"Test Performed at {timestamp}\n\n")
    console.print(f"Scanning Start at : {timestamp}")
    console.print(f'URL : [bold cyan]{args.url}[/]\n\n')
    
    console.print(f"[bold blue][-] Scanning Technology Stack for [/][bold cyan]{args.url}[/]")
    tech_result = tech_detect_recon(args.url, args.verbose)
    append_data(args.file, "Technology Stack:")
    append_data(args.file, "------------------------------")
    append_data(args.file, tech_result)

    ssl_tls_result = ssl_tls_recon(args.url, args.verbose)
    append_data(args.file, "\nSSL/TLS Details:")
    append_data(args.file, "------------------------------")
    append_data(args.file, ssl_tls_result)

    console.print(f"\n[bold blue][-] Starting WHOIS Information scan for [/][bold cyan]{args.url}[/]")
    whois_result = who_is_recon(args.url, args.verbose)
    append_data(args.file, '\nWHOIS Information:')
    append_data(args.file, "------------------------------")
    append_data(args.file, whois_result)

    
    if args.verbose:
        console.print(f"\n[bold magenta][=] Results saved to {args.file}[/]")
        console.print(f"[bold magenta][=] Total time taken: {time.time() - start_time:.2f} seconds[/]")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
