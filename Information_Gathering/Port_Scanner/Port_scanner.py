import argparse
import socket
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
import time
import os
import concurrent.futures

console = Console()

def set_argument():
    parser = argparse.ArgumentParser(
        prog="Port_scanner.py",
        description="The Port_Scanner is a powerful tool within the KnightFall pentesting framework designed to probe a target host or network for open ports. By identifying which ports are open, closed, or filtered, this tool helps security professionals assess the attack surface of their target and uncover potential vulnerabilities."
    )

    parser.add_argument(
        "-t",
        "--target",
        required=False,
        default="127.0.0.1",
        help="Enter the target you want to perform scan on. Default is your local machine 127.0.0.1."
    )

    parser.add_argument(
        '-sp',
        '--start_port',
        required=False,
        type=int,
        default=900,
        help="Enter the port number you want to start scanning from."
    )

    parser.add_argument(
        '-ep',
        '--end_port',
        required=False,
        type=int,
        default=950,
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc: #SOCK_STREAM = tcp scan
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

def port_scanner(args):
    start_port = args.start_port
    end_port = args.end_port
    total_ports = end_port - start_port + 1
    target = args.target
    timeout = args.timeout

    console.print(f"Connecting to the [blue]{args.target}[/blue]")
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
                futures = {}
                for port in range(start_port, end_port + 1):
                    if args.protocol in ['tcp', 'both']:
                        futures[executor.submit(scan_tcp_port, target, port, timeout)] = port
                    if args.protocol in ['udp', 'both']:
                        futures[executor.submit(scan_udp_port, target, port, timeout)] = port

                # Track completed ports
                completed_ports = set()
                for future in concurrent.futures.as_completed(futures):
                    port, is_open, service, protocol = future.result()
                    completed_ports.add(port)
                    if is_open:
                        console.print(f"Port [green]{port}/{protocol}[/green] is OPEN. Service: {service or 'unknown'}")

                    # Advance progress bar based on unique ports
                    if len(completed_ports) <= total_ports:
                        progress.advance(task)

    except KeyboardInterrupt:
        console.print("[red]\nScan interrupted by user. Stopping all tasks...[/red]")
        progress.stop()  # Ensure progress bar stops in case of interruption
        exit()

    console.print("[blue]Scanning complete[/blue]")

def main():
    start_time = time.time()
    args = set_argument().parse_args()
    check_parameters(args)

    try:
        port_scanner(args)
    except KeyboardInterrupt:
        console.print("[red]\nScan interrupted by user.[/red]")
        exit()

    console.print(f"Scan done in [green]{time.time() - start_time:.2f}[/green] seconds")

if __name__ == '__main__':
    os.system("cls" if os.name == "nt" else "clear")
    main()
