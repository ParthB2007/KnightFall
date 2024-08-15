import requests
import argparse
import os
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Global variable to track crawled links count
crawled_count = 0

# Function to set command-line arguments
def set_arguments():
    parser = argparse.ArgumentParser(prog='Web_Crawler.py',
                                     description="A powerful web crawler to fetch and store links from websites.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-pr', '--project', default='', type=str, required=False,
                        help='Specify the project name to save all data.\n'
                             'If not provided, the domain name of the URL will be used as the project name.\n'
                             'Example: -pr MyProject')

    parser.add_argument('-u', '--url', type=str, default='http://www.bbit.ac.in/', required=False,
                        help='Set the base URL to crawl through the website.\n'
                             'Default is http://www.tapidiploma.org/.\n'
                             'Example: -u http://example.com')

    parser.add_argument('-d', '--depth', default=2, type=int, required=False,
                        help='Set the number of pages to crawl.\n'
                             'Default is 2. Increasing this number will allow deeper crawling.\n'
                             'Example: -d 3')

    parser.add_argument('-e', '--extensions', nargs='+', type=str, default=['all'], required=False,
                        help='Specify the file extensions or domains to crawl.\n'
                             'Default is all, which means all links will be crawled.\n'
                             'Example: -e .html .php to crawl only .html and .php files.')

    parser.add_argument('-t', '--threads', default=10, type=int, required=False,
                        help='Specify the number of threads to use for crawling.\n'
                             'Default is 10. More threads can speed up crawling but may increase load on the server.\n'
                             'Example: -t 20')

    return parser

# Function to print the help section
def print_help(parser):
    help_text = parser.format_help()
    title = Text("Web Crawler Help", style="bold cyan")
    description = Text("This script allows you to crawl a website and store links found on the pages.\n\n", style="bold")
    usage = Text("Usage:\n", style="bold yellow")
    usage.append(f"  python {parser.prog} [options]\n\n")
    options = Text("Options:\n", style="bold yellow")
    options.append(help_text)
    footer = Text("\nFor more information, please refer to the documentation or use the --help option.\n", style="bold")

    panel = Panel.fit(description + usage + options + footer, title=title, border_style="bright_yellow")
    console.print(panel)

# Initialize data files and directories
def init_data_files(args):
    if args.project == "":
        args.project = extract_domain_name(args.url)

    console.print(f"Initializing project: [bold blue]{args.project}[/bold blue]")
    create_project_dir(args.project)

# Function to extract domain name from URL
def extract_domain_name(url):
    pattern = re.compile(r'https?://(www\.)?([^/#?]+)')
    domain = pattern.search(url).group(2)
    return domain

# Function to build URL
def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

# Function to connect to website and handle exceptions
def connect_to_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    console.print(f"Connecting to website: [green]{url}[/green]")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        console.print(f"Connected to website successfully. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        console.print(f"Error connecting to website: {url}\nError: {str(e)}")
        exit()

# Function to create project directory
def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to save crawled links to a file
def save_crawled_links_to_file(crawled_links, project_name):
    file_path = os.path.join(project_name, 'crawled_links.txt')
    with open(file_path, 'w') as file:
        for link in crawled_links:
            file.write(link + '\n')
    console.print(f"Saved crawled links to: [bold blue]{file_path}[/bold blue]")

# Function to crawl links
def crawl(url, max_depth, thread_count, extensions):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    global crawled_count
    queue = set()
    crawled = set()
    depth_counter = 0

    queue.add(url)
    all_crawled_links = set()

    while depth_counter < max_depth:
        new_links = set()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            future_to_link = {executor.submit(crawl_link, link, extensions, headers): link for link in queue}
            for future in as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    links = future.result()
                    if links:
                        new_links.update(links)
                        all_crawled_links.update(links)
                except Exception as e:
                    console.print(f"Error crawling {link}: {e}")

        crawled.update(queue)
        queue = new_links - crawled
        depth_counter += 1

    console.print(f"\nCrawling complete at depth {depth_counter}. Total links crawled: {crawled_count}")
    return list(all_crawled_links)

# Function to crawl a single link and scrape links
def crawl_link(url, extensions, headers):
    global crawled_count
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        console.print(f"\n\n[bold blue]Crawling: [green]{url}[/green]")

        links = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                if is_valid_link(full_url, extensions):
                    links.add(full_url)
                    console.print(f"[+]  {full_url}")
                    crawled_count += 1
                else:
                    console.print(f"[red][-] {full_url}[/red]")

        return links

    except requests.exceptions.RequestException as e:
        console.print(f"Error connecting to website: {url}\nError: {str(e)}")
        return set()

# Function to check if a link is valid based on extensions
def is_valid_link(url, extensions):
    parsed_url = urlparse(url)
    if extensions == ['all']:
        return True
    else:
        for ext in extensions:
            if parsed_url.path.endswith(ext):
                return True
    return False
def crawle_link_app(url, max_depth, thread_count, extensions):

    url = build_url(url)
    # Get the crawled links as a list
    crawled_links = crawl(url, max_depth, thread_count, extensions)

    # Initialize an empty dictionary to hold links sorted by extension
    extension_dict = {}

    # Iterate through each link and sort them by extension
    for link in crawled_links:
        # Extract the file extension
        ext = os.path.splitext(urlparse(link).path)[1].lower()

        # If no extension, categorize as 'no_extension'
        if not ext:
            ext = 'no_extension'

        # Add the link to the corresponding extension category
        if ext in extension_dict:
            extension_dict[ext].append(link)
        else:
            extension_dict[ext] = [link]

    # Return the dictionary with extensions as keys and lists of links as values
    return extension_dict

# Main function to run the Web_Crawler
def main():
    parser = set_arguments()
    args = parser.parse_args()

    if args.project.lower() in ('-h', '--help'):
        print_help(parser)
        exit()

    args.url = build_url(args.url)
    init_data_files(args)
    connect_to_website(args.url)
   
    start_time = time.time()
    all_crawled_links = crawl(args.url, args.depth, args.threads, args.extensions)
    end_time = time.time()  

    elapsed_time = end_time - start_time
    console.print(f"\nElapsed Time: [bold]{elapsed_time:.2f} seconds[/bold]")

    # Save the crawled links to a file
    save_crawled_links_to_file(all_crawled_links, args.project)

if __name__ == "__main__":
    main()
