import requests
import argparse
import os
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console

console = Console()

# Global variable to track crawled links count
crawled_count = 0


# Function to set command-line arguments
def set_arguments():
    parser = argparse.ArgumentParser(prog='Web_Crwaler.py',
                                     description="A web Web_Crwaler to fetch and store links from websites.")

    parser.add_argument('-pr', '--project', default='', type=str, required=False,
                        help='Set the project name to save all data.')

    parser.add_argument('-u', '--url', type=str, default='http://www.tapidiploma.org/', required=False,
                        help='Set the base URL to crawl through the website. Default is http://www.bbit.ac.in/.')

    parser.add_argument('-p', '--path', default='./link.txtw', type=str, required=False,
                        help='Set the path to save generated data files. Default is the current directory.')

    parser.add_argument('-d', '--depth', default=2, type=int, required=False,
                        help='Set the number of pages to crawl. Default is 2.')

    parser.add_argument('-e', '--extensions', nargs='+', type=str, default=['all'], required=False,
                        help='Specify the file extensions or domains to crawl. Default is all.')

    parser.add_argument('-t', '--threads', default=10, type=int, required=False,
                        help='Specify the number of threads to use for crawling. Default is 10.')

    return parser


# Initialize data files and directories
def init_data_files(args):
    if args.project == "":
        args.project = extract_domain_name(args.url)

    console.print(f"Initializing project: [bold blue]{args.project}[/bold blue]")
    create_project_dir(args.project)
    create_data_files(args.project, args.url)


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
def connect_to_website(url, headers):
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


# Function to create data files
def create_data_files(project_name, base_url):
    queue_file = os.path.join(project_name, 'queue.txt')
    crawled_file = os.path.join(project_name, 'link.txt')
    if not os.path.isfile(queue_file):
        with open(queue_file, 'w') as f:
            f.write(base_url + '\n')
    if not os.path.isfile(crawled_file):
        with open(crawled_file, 'w') as f:
            f.write('')


# Function to crawl links and JavaScript files
def crawl(url, max_depth, thread_count, extensions, headers, args):
    global crawled_count
    queue = set()
    crawled = set()
    depth_counter = 0

    queue.add(url)
    while depth_counter < max_depth:
        new_links = set()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = {executor.submit(crawl_link, link, extensions, headers, args): link for link in queue}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    links = future.result()
                    if links:
                        new_links.update(links)
                except Exception as e:
                    console.print(f"Error crawling {url}: {e}")

        crawled.update(queue)
        queue = new_links - crawled
        update_files(queue, crawled, args)
        depth_counter += 1

    console.print(f"\nCrawling complete at depth {depth_counter}. Total links crawled: {crawled_count}")


# Function to crawl a single link and scrape links and JavaScript files
def crawl_link(url, extensions, headers, args):
    global crawled_count
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        console.print(f"Crawling: [green]{url}[/green]")

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

        # Extract JavaScript files if no specific extensions are provided or if .js is among the specified extensions
        if extensions == ['all'] or '.js' in extensions:
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    full_url = urljoin(url, src)
                    if is_valid_link(full_url, ['.js']):
                        links.add(full_url)
                        console.print(f"[+][bold blue] {full_url}[/bold blue]")
                        crawled_count += 1

        # Update the crawled file immediately after processing a URL
        with open(f"{args.project}/link.txt", 'a') as f:
            f.write(url + '\n')

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


# Function to update files with crawled and queue links
def update_files(queue, crawled, args):
    queue_file = f"{args.project}/queue.txt"
    with open(queue_file, 'w') as f:
        for link in queue:
            f.write(link + '\n')

    crawled_file = f"{args.project}/link.txt"
    with open(crawled_file, 'w') as f:
        for link in crawled:
            f.write(link + '\n')


# Main function to run the Web_Crwaler
def main():
    parser = set_arguments()
    args = parser.parse_args()

    args.url = build_url(args.url)
    init_data_files(args)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    connect_to_website(args.url, headers)

    start_time = time.time()
    crawl(args.url, args.depth, args.threads, args.extensions, headers, args)
    end_time = time.time()

    elapsed_time = end_time - start_time
    console.print(f"\nElapsed Time: [bold]{elapsed_time:.2f} seconds[/bold]")

