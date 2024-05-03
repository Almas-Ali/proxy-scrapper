from typing import List, Union, Dict
import threading
import re
import socket

import requests
from requests.exceptions import SSLError, ConnectionError
import tqdm


def duplicate_url_remover(input_file: str, output_file: str) -> None:
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Remove duplicates
    unique_urls: List[str] = list(set(lines))

    with open(output_file, "w") as f:
        for line in unique_urls:
            f.write(line)

    print(f"File saved to {output_file}")


def get_ips(url: str, output_file: str) -> None:
    try:
        res: requests.Response = requests.get(url)

    except SSLError:
        # print(f'SSL issue with: {url}')
        return

    except ConnectionError:
        # print(f'Connection error with: {url}')
        return

    if res.status_code != 200:
        # print(f'Error: {res.status_code}')
        return

    ips = res.text.split()
    with threading.Lock():
        with open(output_file, "a") as f:
            for ip in ips:
                f.write(ip + "\n")


def run_save_ips_with_threads(input_file: str, output_file: str) -> None:
    with open(input_file, "r") as f:
        urls: List[str] = f.readlines()

    threads: List[threading.Thread] = []
    for url in urls:
        thread = threading.Thread(target=get_ips, args=(url.strip(), output_file))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def sanitize_ips(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        ips: List[str] = f.readlines()

    sanitized_ips: List[str] = []
    for ip in tqdm.tqdm(ips):
        ip = ip.strip()
        match: Union[re.Match[str], None] = re.match(
            r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d{1,5})?", ip
        )

        if match:
            try:
                sanitized_ips.append(match.group(1) + match.group(2))
            except TypeError:
                sanitized_ips.append(match.group(1))

    # duplicate removal
    sanitized_ips = list(set(sanitized_ips))

    return sanitized_ips


def run_sanitize_ips(input_file: str, output_file: str) -> None:
    ip_list: List[str] = sanitize_ips(input_file)

    with open(output_file, "w") as f:
        for ip in ip_list:
            f.write(ip + "\n")


def proxy_checker(proxy_ip: str, output_file: str) -> None:
    try:
        proxyDict: Dict[str, str] = {"http": proxy_ip, "https": proxy_ip}
        res: requests.Response = requests.get(
            "http://httpbin.org/ip", proxies=proxyDict, timeout=2
        )
        if res.status_code == 200:
            # print(f"Active Proxy: {proxy_ip}")
            with threading.Lock():
                with open(output_file, "a") as f:
                    f.write(proxy_ip + "\n")
    except Exception:
        pass


def run_proxy_checker(input_file: str, output_file: str) -> None:
    socket.setdefaulttimeout(120)

    with open(input_file, "r") as f:
        proxyList = f.readlines()

    # remove whitespace characters like `\n` at the end of each line
    proxyList = [x.rstrip("\n").strip() for x in proxyList]

    threads: List[threading.Thread] = []
    print("Checking %d proxies" % (len(proxyList)))
    for ip in proxyList:
        thread = threading.Thread(target=proxy_checker, args=(ip, output_file))
        threads.append(thread)

    print("Starting Proxy Checker")
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
