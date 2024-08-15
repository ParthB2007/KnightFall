import argparse
import socket
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
import time
import concurrent.futures
import requests

console = Console()

def set_argument():
    parser = argparse.ArgumentParser(
        prog="port_scanner.py",
        description="The Port_Scanner is a powerful tool within the KnightFall pentesting framework designed to probe a target host or network for open ports. By identifying which ports are open, closed, or filtered, this tool helps security professionals assess the attack surface of their target and uncover potential vulnerabilities."
    )

    parser.add_argument(
        "-t",
        "--target",
        required=False,
        default="tapidiploma.org",
        help="Enter the target you want to perform scan on. Default is your local machine 127.0.0.1."
    )

    parser.add_argument(
        '-sp',
        '--start_port',
        required=False,
        type=int,
        default=1,
        help="Enter the port number you want to start scanning from."
    )

    parser.add_argument(
        '-ep',
        '--end_port',
        required=False,
        type=int,
        default=1023,
        help="Enter the port number where you want to end scanning."
    )

    parser.add_argument(
        '-to',
        '--timeout',
        required=False,
        type=float,
        default=0.5,
        help="Set the timeout for each port scan in seconds."
    )

    parser.add_argument(
        '-p',
        '--protocol',
        required=False,
        choices=['tcp', 'udp', 'both'],
        default='both',
        help="Specify the protocol to scan: tcp, udp, or both. Default is both."
    )

    return parser

def check_parameters(args):
    console.print("[blue]Checking arguments[/blue]")
    if args.start_port <= 0:
        console.print("[red]Starting port cannot be zero or negative.[/red]")
        exit()

    if args.end_port <= 0:
        console.print("[red]Ending port cannot be zero or negative.[/red]")
        exit()

    if args.end_port < args.start_port:
        console.print("[red]Ending port cannot be smaller than starting port.[/red]")
        exit()

def scan_tcp_port(target, port, timeout):
    socket.setdefaulttimeout(timeout)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        try:
            result = soc.connect_ex((target, port))
            service = socket.getservbyport(port, 'tcp') if result == 0 else None
            return port, result == 0, service, 'tcp'
        except socket.error:
            return port, False, None, 'tcp'

def scan_udp_port(target, port, timeout):
    socket.setdefaulttimeout(timeout)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as soc:
        try:
            soc.sendto(b'', (target, port))
            soc.settimeout(timeout)
            soc.recvfrom(1024)  # Expecting a response
            service = socket.getservbyport(port, 'udp')
            return port, True, service, 'udp'
        except socket.error:
            return port, False, None, 'udp'

def port_scanner_fun(start_port, end_port, target, protocol, timeout):

    protocol = protocol.lower()
    total_ports = end_port - start_port + 1
    result = []

    console.print(f"Connecting to the [blue]{target}[/blue]")
    console.print("[green]Starting scanning for open ports[/green]")
    try:
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Scanning ports...", total=total_ports)

            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(scan_tcp_port, target, port, timeout): port for port in range(start_port, end_port + 1) if protocol in ['tcp', 'both']}
                futures.update({executor.submit(scan_udp_port, target, port, timeout): port for port in range(start_port, end_port + 1) if protocol in ['udp', 'both']})

                for future in concurrent.futures.as_completed(futures):
                    port, is_open, service, protocol = future.result()
                    if is_open:
                        console.print(f"Port [green]{port}/{protocol}[/] is OPEN Service: {service or 'unknown'}")
                        result.append(f"{port}/{protocol} OPEN Service: {service or 'unknown'}")
                    progress.advance(task)

        console.print("[blue]Scanning complete[/blue]")
        return result


    except KeyboardInterrupt:
        console.print("[red]\nScan interrupted by user. Stopping all tasks...[/red]")
        progress.stop()
        return "Error"


    except Exception as e:
        console.print(f"[red]Error scanning open ports: {e}[/red]")

        return "Error scanning open ports"


def port_scanner_app(start_port, end_port, target, protocol, timeout):
    print("URL:", target, start_port, end_port, protocol)
    result = port_scanner_fun(start_port, end_port, target, protocol, timeout)

    # Check if the result is an error message
    if isinstance(result, str):
        # Handle the case where result is an error message
        return [{"port": "N/A", "protocol": "N/A", "status": result, "service": "N/A"}]

    # Convert the result list into a list of dictionaries for HTML rendering
    formatted_results = []
    for entry in result:
        parts = entry.split()
        port_protocol, status_info = parts[0], " ".join(parts[1:])
        port, protocol = port_protocol.split('/')
        status, service = status_info.split("Service:")
        formatted_results.append({
            "port": port,
            "protocol": protocol,
            "status": status.strip(),
            "service": service.strip()
        })

    print(formatted_results)
    return formatted_results



def main(): 
    start_time = time.time()
    args = set_argument().parse_args()
    check_parameters(args)
    
    res = port_scanner_fun(args.start_port, args.end_port, args.target, args.protocol, args.timeout)
    

    console.print(f"Scan done in [green]{time.time() - start_time:.2f}[/green] seconds")

if __name__ == '__main__':
    main()
