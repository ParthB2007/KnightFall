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
            "Fuzz.py is a tool for discovering hidden pages and directories on a website using a wordlist. "
            "This tool sends requests to the target URL with paths provided in the wordlist file and checks if they exist on the server."
        )
    )

    parser.add_argument(
        '-s', '--save',
        type=str,
        help="Specify a file to save all the found hidden files. "
             "If this option is not provided, results will be printed to the console."
    )

    parser.add_argument(
        '-u', '--url',
        required=False,
        default="www.bbit.ac.in",
        help="Specify the base URL to be fuzzed. "
             "Ensure that the URL includes the protocol."
    )

    parser.add_argument(
        '-w', '--wordlist',
        required=False,
        default=".\Information_Gathering\Hidden_File_Enumeration\directory-list-1.0.txt",
        help="Provide the path to the wordlist file. "
             "The wordlist should contain potential paths to hidden files or directories, "
             "with each path on a new line."
    )

    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=10,
        help="Specify the number of concurrent threads to use for fuzzing. "
             "Default is 10 threads."
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=5,
        help="Set the request timeout in seconds. "
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

def connect_to_website(url):
    """
    Connect to the website and check if it's reachable.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    console.print(f"Connecting to [green]{url}[/green]...", style="bold cyan")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        console.print(f"Connected to website successfully. Status Code: {response.status_code}", style="bold green")
        return f"Connected to {url}. Status Code: {response.status_code}"
    except requests.exceptions.ConnectTimeout:
        console.print(f"Connection to {url} timed out.", style="bold yellow")
        return "Connection Timeout"
    except requests.exceptions.RequestException as e:
        console.print(f"Error connecting to website: {url}\nError: {str(e)}", style="bold red")
        return f"Error: {str(e)}"

def wordlist_to_file(path):
    """
    Read the wordlist from the specified file.
    """
    try:
        with open(path, 'r') as directory:
            return [line.strip() for line in directory]
    except FileNotFoundError:
        console.print(f"Wordlist file not found: {path}", style="bold red")
        return []

def check_url(url, timeout):
    """
    Check the URL and return status if not 404.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code != 404:
            return url, response.status_code, len(response.content)
    except requests.RequestException:
        return None

def fuzzer(url, wordlist_set, threads, timeout):
    """
    Perform fuzzing on the target URL using the wordlist.
    """
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

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(check_url, f"{url}/{word}", timeout): word for word in wordlist_set}

            for future in as_completed(futures):
                result = future.result()
                if result:
                    link, status_code, length = result
                    console.print(
                        f"[blue][+][/blue] [green]{link.ljust(40)} [bold blue]Status Code: {status_code}   Length: {length}[/bold blue]")
                    results.append(result)
                    found_count += 1

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

def fuzz_app(url, threads):
    url = build_url(url)
    connection_status = connect_to_website(url)
    if connection_status.startswith("Error"):
        return {"connection_status": connection_status, "found_results": []}

    wordlist_set = wordlist_to_file(".\Information_Gathering\Hidden_File_Enumeration\directory-list-1.0.txt")
    if not wordlist_set:
        return {"connection_status": "Wordlist file not found or empty.", "found_results": []}

    found_results = fuzzer(url, wordlist_set, threads, timeout=5)
    
    # Format found results into a list of dictionaries
    formatted_results = []
    for result in found_results:
        if isinstance(result, tuple):
            formatted_results.append({
                'url': result[0],
                'status_code': result[1],
                'response_size': result[2]
            })
        else:
            formatted_results.append({
                'url': result,
                'status_code': 'N/A',
                'response_size': 'N/A'
            })
    
    return {"connection_status": connection_status, "found_results": formatted_results}




def main():
    """
    Main function to run the fuzzing tool.
    """
    parser = set_arguments()
    args = parser.parse_args()
    console.print(f"Building URL: {args.url}", style="bold blue")
    args.url = build_url(args.url)

    connect_to_website(args.url)
    wordlist_set = wordlist_to_file(args.wordlist)
    results = fuzzer(args.url, wordlist_set, args.threads, args.timeout)

    if args.save:
        save_to_file(args.save, results)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
