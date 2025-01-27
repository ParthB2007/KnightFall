# KnightFall: Advanced Web Reconnaissance and Vulnerability Scanning Framework

**KnightFall** is a robust, Python-based framework for web reconnaissance and penetration testing. This tool is designed for ethical hackers, cybersecurity enthusiasts, and penetration testers. It provides in-depth analysis of websites through both **CLI support** and a **Flask-based web app** with **multithreading** capabilities for enhanced performance.

## Features

### Web Reconnaissance
1. **Web Page Scraping**  
   - Extracts links, resources, and metadata from websites.

2. **Hidden File/Directory Finder**  
   - Enumerates hidden files and directories using custom wordlists.

3. **NS Lookup**  
   - Performs DNS and Name Server lookups for detailed network information.

4. **SSL Certificate Checker**  
   - Analyzes the SSL/TLS certificates of websites to ensure proper security configuration.

5. **WHOIS Lookup**  
   - Fetches domain registration details, expiration dates, and ownership information.

6. **Technology Stack Detection**  
   - Identifies the frameworks, libraries, and technologies used by the website.

7. **Open Port Scanner**  
   - Scans for hidden open ports on the target website (supports TCP and UDP protocols).
     
8. **Security Header Scanner**  
   - Checks for the presence and configuration of critical HTTP security headers.
     
### Vulnerability Scanning (Work in Progress) 

1. **XSS Scanner (Work in Progress)**  
   - Detects vulnerabilities that could lead to Cross-Site Scripting (XSS) attacks.

## Key Highlights
- **Multithreaded Performance**: Handles large-scale tasks efficiently.
- **Dual Support**: Can be used as a **command-line tool** or a **web application** powered by Flask.
- **Extensive Command-Line Options**: Each tool offers a variety of customizable arguments and flags for flexibility.
- **Python-Powered**: Built entirely in Python using libraries like `requests`, `bs4`, `socket`, `rich`, and others.

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/ParthB2007/KnightFall.git
   cd KnightFall
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tool in CLI mode:
   ```bash
   python Full_Recon.py --url <target_url>
   ```
4. Run the tool in Flask web app mode:
   ```bash
   python app.py
   Access the web interface at http://127.0.0.1:5000.
   ```

### Usage
## CLI Mode
   ```bash
   python Full_Recon.py --url <target_url> [OPTIONS]
   ```
## Options:

--output <file>: Save results to a file.

--verbose: Display detailed logs.

--depth <level>: Customize crawling depth for web pages.

--port-scan: Enable port scanning (supports TCP and UDP).

--timeout <seconds>: Set timeout for requests and scans.

--wordlist <file>: Use a custom wordlist for hidden file and directory enumeration.

And many more! Use --help with each tool for the complete list of options.



## Contributing
We welcome contributions from the community! Feel free to fork the repository, submit pull requests, or open issues for feature requests and bug reports.

License
This project is licensed under the MIT License.

### Screenshots
![Full Recon CLI]()
![Open Port Scanner CLI]()
![Open Port Scanner GUI]()
![Open Port Scanner Result GUI]()


### Contact
Author: Parth B.

GitHub: [ParthB2007](https://github.com/ParthB2007)

LinkedIn: [Parth B.](https://www.linkedin.com/in/parthb2007)

Email: parthbaldha2007@gmail.com
