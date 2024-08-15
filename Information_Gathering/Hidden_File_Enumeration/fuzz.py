import os
import requests
import argparse
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()

def set_arguments():
    """
    Set up command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(
        prog="fuzz.py",
        description=(
            "Fuzz.py is a tool for discovering hidden pages and directories on a website using a wordlist. This tool sends requests to the target URL with paths provided in the wordlist file and checks if they exist on the server. It can be useful for security assessments, finding unlinked pages, "
            "or discovering hidden resources.\n\n"
            "Example usage:\n"
            "python fuzz.py -u http://example.com -w wordlist.txt -t 20 --timeout 10 -s found_pages.txt\n\n"
            "In this example, the tool will fuzz http://example.com using wordlist.txt with 20 concurrent "
            "threads and a 10-second timeout for each request. The found hidden pages will be saved to found_pages.txt.")
    )

    parser.add_argument(
        '-s', '--save',
        type=str,
        required=False,
        help="Specify a file to save all the found hidden files. "
             "If this option is not provided, results will be printed to the console."
    )

    parser.add_argument(
        '-u', '--url',
        required=False,
        default="www.tapidiploma.org",
        help="Specify the base URL to be fuzzed. "
             "Ensure that the URL includes the protocol."
    )

    parser.add_argument(
        '-w', '--wordlist',
        required=False,
        default=".\directory-list-1.0.txt",
        help="Provide the path to the wordlist file. "
             "The wordlist should contain potential paths to hidden files or directories, "
             "with each path on a new line."
    )

    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=10,
        required=False,
        help="Specify the number of concurrent threads to use for fuzzing. "
             "More threads can speed up the process but may put more load on the server. "
             "Default is 10 threads."
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=5,
        required=False,
        help="Set the request timeout in seconds. "
             "This defines how long the tool will wait for a server response before timing out. "
             "Default is 5 seconds."
    )

    return parser

def build_url(url):
    """
    Ensure the URL starts with http:// or https://.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

def connect_to_website(url,headers):
    """
    Connect to the website and check if it's reachable.
    """


    console.print(f"Connecting to the [green]{url}[/green]...", style="bold cyan")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        console.print(f"Connected to website successfully. Status Code: {response.status_code}", style="bold green")
    except requests.exceptions.ConnectTimeout:
        # Handle the connection timeout silently
        console.print(f"Connection to {url} timed out.", style="bold yellow")
        exit()
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions
        console.print(f"Error connecting to website: {url}\nError: {str(e)}", style="bold red")
        exit()


def wordlist_to_file(path):
    """
    Read the wordlist from the specified file.
    """
    result = []
    try:
        with open(path, 'r') as directory:
            for line in directory:
                result.append(line.strip())
    except FileNotFoundError:
        console.print(f"Wordlist file not found: {path}", style="bold red")
        exit()
    return result

def check_url(url, timeout):
    """
    Check the URL and return status if not 404.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code != 404:
            return url, response.status_code, len(response.content)
    except requests.RequestException as e:
        # console.print(f"Request failed for {url}: {str(e)}", style="bold red")
        return None


def fuzzer(args, wordlist_set,headers):
    """
    Perform fuzzing on the target URL using the wordlist.
    """
    url = args.url
    total = len(wordlist_set)
    results = []
    found_count = 0

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TextColumn("[bold red]Found:[/bold red] [bold yellow]{task.fields[found_count]:>5}[/bold yellow]"),
            console=console
    ) as progress:

        task = progress.add_task("[green]Fuzzing...", total=total, found_count=0)
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            # Submit all futures
            futures = []
            for word in wordlist_set:
                future = executor.submit(check_url, f"{url}/{word}", args.timeout)
                futures.append(future)

            # Process results as they complete
            for future in as_completed(futures):
                result = future.result()
                if result:
                    link, status_code, length = result
                    # Print results in a simple line format
                    if status_code == 200:
                        console.print(
                        f"[blue][+][/blue] [green]{link.ljust(40)} [bold blue]Status Code: {status_code}   Length: {length}[/bold blue]")
                        results.append(result)
                        found_count += 1

                # Update progress bar
                progress.update(task, found_count=found_count)
                progress.advance(task)

    return results


def save_to_file(path, results):
    """
    Save the results to the specified file.
    """
    with open(path, 'w') as file:
        for link, status_code, length in results:

            file.write(f"{link} {status_code} {length}\n")

def main():
    """
    Main function to run the fuzzing tool.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    os.system('cls' if os.name == 'nt' else 'clear')
    parser = set_arguments()
    args = parser.parse_args()
    console.print(f"Building URL: {args.url}", style="bold blue")
    args.url = build_url(args.url)

    connect_to_website(args.url, headers)
    wordlist_set = wordlist_to_file(args.wordlist)
    results = fuzzer(args, wordlist_set,headers)

    if args.save:
        save_to_file(args.save, results)

if __name__ == '__main__':
    main()
