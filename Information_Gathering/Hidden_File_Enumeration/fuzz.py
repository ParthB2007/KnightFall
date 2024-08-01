import requests
import argparse
from rich.console import Console
from time import time

console = Console()


def set_argument():
    parser = argparse.ArgumentParser(
        prog='Security_Header.py',
        description='Check security headers of a target URL to assess security configurations.'
    )

    parser.add_argument(
        '-u',
        '--url',
        required=False,
        default="https://www.nationwide.com/",
        help="Target URL to check (default: https://www.nationwide.com/)"
    )

    parser.add_argument(
        '-o',
        '--output',
        required=False,
        help="Output file to save the results (if specified, results will be saved in this file)"
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Enable verbose mode to get detailed output about the scanning process"
    )

    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=10,
        help="Timeout for HTTP requests in seconds (default: 10 seconds)"
    )

    parser.add_argument(
        '-a',
        '--agent',
        default='Mozilla/5.0 (compatible; SecurityHeaderChecker/1.0)',
        help="Custom User-Agent header for the request (default: Mozilla/5.0 (compatible; SecurityHeaderChecker/1.0))"
    )

    return parser


def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()


def header_scanner(args):
    url = args.url
    agent = args.agent
    timeout = args.timeout
    security_headers = {
        "Strict-Transport-Security": "Helps prevent man-in-the-middle attacks by enforcing secure (HTTP over SSL/TLS) connections to the server.",
        "Content-Security-Policy": "Prevents cross-site scripting (XSS), clickjacking, and other code injection attacks by specifying which sources of content are allowed.",
        "X-Content-Type-Options": "Prevents browsers from MIME-sniffing a response away from the declared content-type, which can help avoid some types of attacks.",
        "X-Frame-Options": "Protects against clickjacking attacks by controlling whether a browser should be allowed to render a page in a <frame>, <iframe>, <embed>, or <object>.",
        "X-XSS-Protection": "Enables cross-site scripting (XSS) filter built into most modern web browsers, helping to prevent some types of XSS attacks.",
        "Referrer-Policy": "Controls how much referrer information (sent via the Referer header) should be included with requests, which can help protect privacy.",
        "Permissions-Policy": "Defines a set of permissions for the web page or iframe, such as access to geolocation or camera.",
        "Expect-CT": "Allows sites to determine if they are ready for Certificate Transparency enforcement and report back to the site if any issues arise.",
        "Cache-Control": "Directives for caching mechanisms in both requests and responses, which can affect how sensitive data is cached.",
        "Pragma": "Used for backward compatibility with HTTP/1.0 caches, often related to cache control."
    }

    result = {}
    start_time = time()

    if args.verbose:
        console.print(f"Scanning [bright_yellow]{url}[/bright_yellow] for security headers...\n")
        console.print(
            f"Request Details:\nURL : [bright_magenta]{url}[/bright_magenta]\nUser-Agent : [bright_magenta]{agent}[/bright_magenta]\nTimeout : [bright_magenta]{timeout}[/bright_magenta] seconds\n")

    try:
        response = requests.get(url, headers={'User-Agent': agent}, timeout=timeout)
        elapsed_time = time() - start_time
        status_code = response.status_code
        web_headers = response.headers

        if args.verbose:
            console.print(
                f"\nReceived Response:\nStatus Code: [cyan bold]{status_code}[/cyan bold]\nResponse Time: [cyan bold]{elapsed_time:.2f}[/cyan bold] seconds")
            console.print("\nReceived Response Headers:")
            for header, value in web_headers.items():
                console.print(f"[cyan bold]{header}[/cyan bold]: [bright_white]{value}[/bright_white]")

        for header in security_headers:
            if header in web_headers:
                result[header] = 1
            else:
                result[header] = 0

        # Sort headers by existence (0 or 1), then alphabetically
        sorted_results = sorted(result.items(), key=lambda item: (-item[1], item[0]))

        console.print("\nSecurity Header Check Results:")
        missing_count = 0
        for header, exist in sorted_results:
            if exist == 1:
                console.print(f"[bold green]{header}: Present[/bold green]")
            else:
                console.print(f"[bold red]{header}: Missing[/bold red]")
                missing_count += 1

        # Print detailed descriptions in verbose mode
        if args.verbose:
            console.print("\nDetailed Header Descriptions:")
            for header, description in sorted(security_headers.items()):
                status = "Present" if result.get(header, 0) == 1 else "Missing"
                color = "bold green" if status == "Present" else "bold red"
                console.print(f"[{color}]{header}:[/{color}] {description}")

        console.print(
            f"\nSummary:\nTotal Headers Checked: [bright_blue]{len(security_headers)}[/bright_blue]\nHeaders Missing: [bold red]{missing_count}[/bold red]")

    except requests.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


def main():
    args = set_argument().parse_args()
    args.url = build_url(args.url)
    header_scanner(args)


if __name__ == '__main__':
    main()