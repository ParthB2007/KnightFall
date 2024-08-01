import requests
import os
import argparse
from rich.console import Console
import time
import urllib.parse

# Initialize the console for output
console = Console()


def set_arguments():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="XSS Scanner",
        description="A simple XSS scanner to check for XSS vulnerabilities on target websites."
    )

    parser.add_argument(
        '-t',
        '--target',
        required=True,
        help="Enter the target website to check for XSS injection"
    )

    parser.add_argument(
        '-p',
        '--payload',
        required=False,
        default="./payloads.txt",
        help="Enter a file containing payloads to perform XSS injection on the target"
    )

    parser.add_argument(
        '-r',
        '--report',
        required=False,
        default='report.txt',
        help='Save scanned report'
    )

    return parser


def load_payload(filepath):
    """Load payloads from a file."""
    data = []
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Payload file '{filepath}' not found.")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            data.append(line.strip())
    return data


def test_xss_in_link(session, url, payloads, report_file):
    """Test a URL for XSS vulnerabilities using the provided payloads."""
    for payload in payloads:
        xss_test_script = payload
        parsed_url = urllib.parse.urlparse(url)

        if parsed_url.query:
            # Append payload to the existing query parameter
            test_url = url + urllib.parse.quote_plus(xss_test_script)
        else:
            # Add payload as a new query parameter
            test_url = url + ('&' if '?' in url else '?') + urllib.parse.quote_plus(xss_test_script)

        try:
            response = session.get(test_url)
            if xss_test_script in response.content.decode():
                log_vulnerability("link", test_url, xss_test_script, report_file, True)
            else:
                log_vulnerability("link", test_url, xss_test_script, report_file, False)
        except Exception as e:
            console.print(f"Error testing link [red]{test_url}[/red]: {e}")


def log_vulnerability(type, url, payload, report_file, is_vulnerable):
    """Log the result of the vulnerability test."""
    if is_vulnerable:
        console.print(f"[green]Vulnerability found[/green] in {type} at {url} with payload: {payload}")
        with open(report_file, 'a') as report:
            report.write(f"Vulnerability found in {type} at {url} with payload: {payload}\n")
    else:
        console.print(f"[red]No vulnerability[/red] in {type} at {url} with payload: {payload}")


def run_scanner(target_url, payloads, report_file):
    """Run the XSS scanner on the target URL with the provided payloads."""
    session = requests.Session()
    console.print(f"[yellow]Testing link[/yellow] {target_url}")
    test_xss_in_link(session, target_url, payloads, report_file)


def main():
    """Main function to execute the scanner."""
    start_time = time.time()
    args = set_arguments().parse_args()
    payload_data = []

    try:
        payload_data = load_payload(args.payload)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        exit()

    console.print("Starting XSS scan...\n")
    run_scanner(args.target, payload_data, args.report)
    console.print(f"Scan complete. Report saved to [green]{args.report}[/green]")
    console.print(f"\nTime Taken: [blue]{time.time() - start_time:.2f} seconds[/blue]")


if __name__ == '__main__':
    main()
