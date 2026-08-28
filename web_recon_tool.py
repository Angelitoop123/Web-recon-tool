from concurrent.futures import ThreadPoolExecutor
from faker import Faker
from rich.console import Console
from rich.theme import Theme
from rich.progress import track


import argparse
import dns.resolver
import pyfiglet
import requests
import socket
import ssl
import sys
import time

theme = Theme({
    "success": "green",
    "error": "red",
    "info": "cyan",
    "banner": "purple"
})

console = Console(theme=theme)

faker = Faker()

resolver = dns.resolver.Resolver()

def progress_bar() -> None:
    for _ in track(range(10), description="Loading..."):
        time.sleep(0.5)

def fake_agent() -> str:
    return faker.user_agent()


class WebReconTool:
    def __init__(self, args):
        self.args = args

    def run(self):
        if not self.args.subdomain and not self.args.port and not self.args.headers and not self.args.information:
            self.dns_enumaration()

        if self.args.target and self.args.subdomain:
            self.subdomain_enumeration()

        if self.args.target and self.args.port:
            self.port_scanner()

        if self.args.target and self.args.headers:
            self.http_headers()

        if self.args.target and self.args.information:
            self.information()

        
      


    def dns_enumaration(self):
        respuestas = ["A", "AAAA", "MX", "NS"]

        if self.args.target:
            for respuesta in respuestas:
                console.print(f'[+] Results for: {respuesta}', style="success")
                try:
                    resp = resolver.resolve(self.args.target, respuesta)
                    print("\n")
                    for i, r in enumerate(resp, start=1):
                        console.print(f'[{i}] {r}', style="info")
                    print("\n")
                except Exception:
                    continue


    def subdomain_enumeration(self):
        if self.args.subdomain and self.args.target:
            subdominios_reales = []
            subdominios_falsos = []

            try:
                with open(f'{self.args.subdomain}', "r") as file:
                    subdominios = [f'{subdominio.strip()}.{self.args.target}' for subdominio in file if subdominio.strip()]
            except FileNotFoundError:
                console.print(f'[!] File Not found!! -> {self.args.subdomain}')
                sys.exit()

            def verificar_subdominio(subdominio):
                try:
                    if resolver.resolve(subdominio):
                        subdominios_reales.append(subdominio)
                        return f"[+] {subdominio} analyzed." 
                except Exception:
                    subdominios_falsos.append(subdominio)
                    return f'[!] {subdominio} refused.'
            

            with ThreadPoolExecutor() as executor:
                resultados = executor.map(verificar_subdominio, subdominios)
                for resultado in resultados:
                    if resultado.startswith("[+]"):
                        console.print(resultado, style="success")
                    elif resultado.startswith("[!]"):
                        console.print(resultado, style="error")



    def port_scanner(self):
        if self.args.port and self.args.target:
            direcciones = resolver.resolve(self.args.target, "A")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            for direccion in direcciones:
                result = sock.connect_ex((str(direccion), self.args.port))
                if result == 0:
                    console.print(f'[*] Port {self.args.port} is open for -> {str(direccion)}', style="info")
                else:
                    console.print(f'[*] Port {self.args.port} is closed for -> {str(direccion)}', style="info")



    def http_headers(self):
        if self.args.headers and self.args.target:
            protocols = ("http", "https")
            h = {
                "user-agent": fake_agent()
            }

            try:
                for protocol in protocols:
                    response = requests.get(f'{protocol}://{self.args.target}'.strip(), headers=h)
                    if 200 <= response.status_code < 399:
                       try:
                            headers = response.headers
                            console.print(f"[*] Header -> {self.args.headers} -> {headers[self.args.headers]}")
                            break
                       except KeyError:
                           console.print(f"[!] Header -> {self.args.headers} not found!!", style="error")
                    else:
                        continue
            except requests.exceptions.ConnectionError:
                console.print("[!] Connection Error detected!!", style="error")
                sys.exit()



    def information(self):
       if self.args.information and self.args.target:
           context = ssl.create_default_context()
           progress_bar()

           with socket.create_connection((self.args.target, 443)) as sock:
               with context.wrap_socket(sock, server_hostname=self.args.target) as ssock:
                   ip, port, _, _ = ssock.getpeername()
                   cert = ssock.getpeercert()

                   console.print("[*] Filtering results:", style="info")
                   console.print(f'[+] Domain -> {self.args.target}', style="success")
                   console.print(f"[+] IP address (IPV6) -> {ip}", style="success")
                   console.print(f'[+] Port -> {port}\n\n', style="success")

                   console.print("[*] User information:", style="info")
                   for item in cert["issuer"]:
                       console.print(f'[+] {item[0][0]} -> {item[0][1]}', style="success")

                   console.print(f'\n\n[*] Serial number:', style="info")
                   console.print(f"[+] All serial numbers -> {cert.get('serialNumber')}", style="success")

                   version_tls = ssock.version()
                   c_name, c_version, bits = ssock.cipher()

                   console.print("\n\n[*] Version:", style="info")
                   console.print(f"[+] Recent version -> {version_tls}\n", style="success")

                   console.print("\n[*] Encryption algorithm:", style="info")
                   console.print(f'[+] Name -> {c_name}', style="success")
                   console.print(f'[+] Bits -> {bits}', style="success")

                   console.print("\n\n[*] OCSP / CA Validation Links", style="info")
                   aia_data = cert.get("authorityInfoAccess")

                   if aia_data:
                       for aia in aia_data:
                           console.print(f'[+]    {aia[0]} -> {aia[1]}', style="success")
                   else:
                       console.print("[-] Not AIA DATA", style="error")

                   console.print("\n\n[*] Domains and subdomains:", style="info")
                   for item in cert["subjectAltName"]:
                       console.print(f'[+] {item[1]}', style="success")

           console.print("\n\n[*] Ubication:", style="info")
           try:
               h = {
                   "User-Agent": fake_agent()
               }
               ip = socket.gethostbyname(self.args.target)
               url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
               response = requests.get(url, timeout=5, headers=h)
               data = response.json()

               if data.get("status") == "success":
                   console.print(f"[+] Country: {data.get('country')} ({data.get('countryCode')})",style="success")
                   console.print(f"[+] Region/State: {data.get('regionName')}", style="success")
                   console.print(f"[+] City: {data.get('city')}", style="success")
                   console.print(f"[+] Coordinates: {data.get('lat')}, {data.get('lon')}", style="success")
                   console.print(f"[+] Internet Service Provider (ISP): {data.get('isp')}", style="success")
                   console.print(f"[+] Organization / AS: {data.get('org')} ({data.get('as')})", style="success")
               else:
                    console.print(f"[-] Could not access to ubication!!: {data.get('message')}", style="error")
           except Exception as e:
               console.print(f"[!] Error: {e}", style="error")



if __name__ == "__main__":
    banner = pyfiglet.figlet_format("WEB RECON TOOL", font="slant")
    console.print(banner, style="banner")

    parser = argparse.ArgumentParser(description="Python Web Recon Scanner")

    parser.add_argument("-t", "--target", help="Domain", required=True)
    parser.add_argument("-s", "--subdomain", help="Enter subdomain list file")
    parser.add_argument("-p", "--port", help="Port Scanner [22, 80, 443, 8080]", type=int)
    parser.add_argument("-H", "--headers", help="Get information for a header")
    parser.add_argument("-I", "--information", help="SSL/TTL Information", type=bool)


    args = parser.parse_args()

    tool = WebReconTool(args=args)
    tool.run()
