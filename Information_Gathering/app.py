from flask import Flask, render_template, request
import os
import time
from rich.console import Console
from Tech_Detector import tech_detector
from SSL_TLS_Checker import SSL_TLS_check
from WHOIS import who_is
from Port_Scanner import port_scanner

app = Flask(__name__)

# Initialize Rich Console
console = Console()

def build_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    start_port = int(request.form.get('start_port', 1))
    end_port = int(request.form.get('end_port', 1000))
    protocol = request.form.get('protocol', 'tcp')
    verbose = 'verbose' in request.form

    url = build_url(url)

    results = {}

    # Tech Detector
    tech_result = tech_detector.detect_technologies(url, verbose)
    formatted_tech_result = "\n".join([f"{k}: {', '.join(v)}" for k, v in tech_result.items()])
    results['tech'] = formatted_tech_result

    # SSL/TLS Checker
    ssl_tls_result = SSL_TLS_check.check_ssl_tls(url, verbose=verbose)
    ssl_tls_result = ssl_tls_result.replace('[bold green]', '').replace('[/]', '')
    results['ssl_tls'] = ssl_tls_result

    # WHOIS Information
    whois_result = who_is.display_whois_info(url, verbose)
    whois_result = whois_result.replace('[bold yellow]', '').replace('[/]', '')
    results['whois'] = whois_result

    # Open Port Scanner
    port_scanner_result = port_scanner.port_scanner(start_port, end_port, url, protocol, timeout=5)
    results['ports'] = port_scanner_result

    return render_template('results.html', url=url, results=results)

if __name__ == '__main__':
    app.run(debug=True)
