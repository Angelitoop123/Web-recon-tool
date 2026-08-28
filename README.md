# 🔎 Web Recon Tool

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Development-orange)

**Web Recon Tool** is a Python-based command-line reconnaissance tool designed for learning and authorized security testing.

It provides several basic reconnaissance capabilities, including DNS enumeration, subdomain enumeration, TCP port scanning, HTTP header analysis, and SSL/TLS certificate inspection.

> ⚠️ **Disclaimer:** This project is intended for educational purposes and authorized security testing only. Do not use this tool against systems or domains without explicit permission.

---

## ✨ Features

* 🌐 DNS Enumeration
* 🔎 Subdomain Enumeration
* 🔌 TCP Port Scanning
* 🧾 HTTP Header Analysis
* 🔐 SSL/TLS Information
* 🌍 IP Geolocation Information
* ⚡ Concurrent subdomain checking
* 🎨 Colored terminal output
* 🖥️ Command-line interface

---

## 📋 Requirements

* Python 3.9+
* Internet connection
* A domain that you own or are authorized to test

### Python dependencies

The project uses the following external libraries:

```text
Faker
dnspython
pyfiglet
requests
rich
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/web-recon-tool.git
```

Enter the project directory:

```bash
cd web-recon-tool
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

General syntax:

```bash
python recon.py -t TARGET [OPTIONS]
```

Display the help menu:

```bash
python recon.py -h
```

---

# 🌐 DNS Enumeration

The DNS enumeration module queries common DNS record types:

* `A`
* `AAAA`
* `MX`
* `NS`

### Example

```bash
python recon.py -t example.com
```

Example output:

```text
[+] Results for: A
[1] 93.184.216.34

[+] Results for: MX
[1] mail.example.com.
```

---

# 🔎 Subdomain Enumeration

The subdomain enumeration module uses a wordlist to generate and resolve possible subdomains.

Create a file called:

```text
subdominios.txt
```

Example:

```text
www
mail
api
dev
admin
portal
blog
test
vpn
ftp
```

Run:

```bash
python recon.py -t example.com -s subdominios.txt
```

The tool will generate:

```text
www.example.com
mail.example.com
api.example.com
dev.example.com
admin.example.com
```

Example output:

```text
[+] www.example.com analyzed.
[+] api.example.com analyzed.
[!] admin.example.com refused.
[+] mail.example.com analyzed.
```

The enumeration uses `ThreadPoolExecutor` to perform multiple DNS queries concurrently.

---

# 🔌 Port Scanner

The port scanner checks whether a specified TCP port is open or closed on the IP addresses resolved from the target.

### Example

```bash
python recon.py -t example.com -p 443
```

Example:

```text
[*] Port 443 is open for -> 93.184.216.34
```

You can test ports such as:

```text
22
80
443
8080
```

---

# 🧾 HTTP Header Analysis

The HTTP header module retrieves a specific HTTP response header.

### Example

```bash
python recon.py -t example.com -H Server
```

The tool attempts to connect using:

```text
http://example.com
https://example.com
```

Example:

```text
[*] Header -> Server -> nginx
```

A random User-Agent is generated using the `Faker` library.

---

# 🔐 SSL/TLS Information

The SSL/TLS module establishes a TLS connection with the target and retrieves information from its certificate and connection.

### Example

```bash
python recon.py -t example.com -I
```

The module can display:

* Domain
* IP address
* Port
* Certificate issuer
* Serial number
* TLS version
* Cipher
* Encryption bits
* Subject Alternative Names
* Authority Information Access

Example:

```text
[*] Filtering results:

[+] Domain -> example.com
[+] IP address -> 93.184.216.34
[+] Port -> 443

[*] Version:
[+] Recent version -> TLSv1.3

[*] Encryption algorithm:
[+] Name -> TLS_AES_256_GCM_SHA384
[+] Bits -> 256
```

---

# 🌍 IP Geolocation

The information module also retrieves approximate geolocation and network information associated with the target IP.

Information may include:

```text
Country
Region
City
Coordinates
ISP
Organization
AS
```

Example:

```text
[+] Country: United States (US)
[+] Region/State: California
[+] City: Los Angeles
[+] Coordinates: ...
[+] Internet Service Provider (ISP): ...
[+] Organization / AS: ...
```

---

# 🛠️ Command-Line Options

| Option                | Description                |
| --------------------- | -------------------------- |
| `-t`, `--target`      | Target domain              |
| `-s`, `--subdomain`   | Subdomain wordlist         |
| `-p`, `--port`        | TCP port to scan           |
| `-H`, `--headers`     | HTTP header to retrieve    |
| `-I`, `--information` | SSL/TLS and IP information |
| `-h`, `--help`        | Display help               |

---

# 📁 Project Structure

```text
web-recon-tool/
│
├── recon.py
├── subdominios.txt
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📦 requirements.txt

The `requirements.txt` file should contain:

```text
Faker
dnspython
pyfiglet
requests
rich
```

Install them with:

```bash
pip install -r requirements.txt
```

---

# 🧠 Concepts Practiced

This project was created to practice Python and introductory cybersecurity concepts.

### Python

* Object-Oriented Programming
* Functions
* Exception handling
* File handling
* List comprehensions
* Command-line arguments
* Multithreading/concurrency

### Networking

* DNS
* IPv4
* TCP
* HTTP
* HTTP headers
* SSL/TLS
* Digital certificates
* IP addresses

### Libraries

* `socket`
* `ssl`
* `dns.resolver`
* `requests`
* `ThreadPoolExecutor`
* `argparse`
* `Rich`
* `Faker`
* `PyFiglet`

---

# 🔮 Future Improvements

Planned improvements may include:

* [ ] Multiple port scanning
* [ ] Better DNS error handling
* [ ] Export results to `.txt`
* [ ] Export results to `.json`
* [ ] Improved progress indicators
* [ ] IPv6 support
* [ ] DNS record expansion
* [ ] Better subdomain enumeration
* [ ] Configurable DNS timeout
* [ ] More HTTP information
* [ ] Improved CLI interface

---

# ⚠️ Legal Disclaimer

This tool is provided for **educational purposes and authorized security testing**.

You are responsible for ensuring that you have permission to test the target systems.

Do not use this software to scan or enumerate systems, domains, networks, or services without authorization.

The author is not responsible for damage, misuse, or unauthorized activity performed with this software.

---

# 👨‍💻 Author

Utrilla Solis, Angel Kyle

Python • Networking • Cybersecurity

---

## ⭐ Support

If you find this project useful for learning Python, networking, or cybersecurity, consider giving the repository a ⭐ on GitHub.
