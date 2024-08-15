from flask import Flask, request, render_template
from Full_Recon import full_recon_app  # Import your existing functions
from Web_Crawler import crawler
from Hidden_File_Enumeration import fuzz
from Port_Scanner import port_scanner

# Create the Flask app instance
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')
        verbose = request.form.get('verbose') == 'on'
        try:
            result = full_recon_app(url, verbose)
        except Exception as e:
            return f"An error occurred: {e}", 500
        return render_template('recon_result.html', content=result)
    return render_template('recon_scan.html')


@app.route('/web-crawler', methods=['GET', 'POST'])
def web_crawler_page():
    if request.method == 'POST':
        url = request.form.get('url', '')
        max_depth = request.form.get('max_depth')
        thread_count = request.form.get('thread_count')
        extensions = request.form.getlist('extensions')  # Use getlist for multiple values
        try:
            max_depth = int(max_depth) if max_depth else 2  # Default to 2 if not provided
            thread_count = int(thread_count) if thread_count else 10  # Default to 10 if not provided
        except ValueError:
            return "Invalid number for depth or threads. Please enter valid integers.", 400

        if not extensions:
            extensions = ['all']  # Default to 'all' if no extensions provided

        try:
            result = crawler.crawle_link_app(url, max_depth, thread_count, extensions)
        except Exception as e:
            return f"An error occurred: {e}", 500
        return render_template('crawl_results.html', content=result)
    return render_template('web_crawler.html')

@app.route('/hidden-web-enumeration', methods=['GET', 'POST'])
def hidden_web_enumeration_page():
    if request.method == 'POST':
        url = request.form.get('url', '')
        threads = request.form.get('threads', 10)  # Default to 10 if not provided

        try:
            threads = int(threads)
        except ValueError:
            return "Invalid number for threads. Please enter a valid integer.", 400

        try:
            result = fuzz.fuzz_app(url, threads)
        except Exception as e:
            return f"An error occurred: {e}", 500
        return render_template('fuzz_result.html', results=result)
    return render_template('hidden_web_enumeration.html')


@app.route('/open-port-scanner', methods=['GET', 'POST'])
def open_port_scanner_page():
    if request.method == 'POST':
        target = request.form.get('target')
        start_port = int(request.form.get('start-port'))
        end_port = int(request.form.get('end-port'))
        protocol = request.form.get('protocol')
        timeout = float(request.form.get('timeout'))

        # Call port_scanner_app function
        results = port_scanner.port_scanner_app(start_port, end_port, target, protocol, timeout)
        
        # Render results in the template
        return render_template('open_port_scanner_results.html', results=results)

    return render_template('open_port_scanner.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Explicitly specify the port
