"""
The CLI module for the proxy_scrapper package. This module is the entry point for the package and provides a CLI interface for the user to interact with the package.
"""

import os

import proxy_scrapper.scan_url_file as internals


def get_and_save_ips_from_file_urls() -> None:
    """Get and save IP addresses from URLs in a file"""
    # ask for file path
    file_path = input("Enter the path to the file containing the URLs: ").strip()

    # check if the file exists
    if not os.path.exists(file_path):
        print("[!] File does not exist.")
        return

    # check if the file is a file
    if not os.path.isfile(file_path):
        print("[!] Invalid file path.")
        return

    # get the output file path
    output_file = input(
        "Enter the output path for the IP addresses (default: output.txt): "
    ).strip()

    # check if the output file is provided
    if not output_file:
        output_file = "output.txt"

    # check if the output file is a text file
    if not output_file.endswith(".txt"):
        output_file += ".txt"

    # remove duplicate urls
    internals.duplicate_url_remover(file_path, output_file)
    # now every work will be done on the output file

    # run the threads
    internals.run_save_ips_with_threads(output_file, output_file)

    # sanitize the ips
    internals.run_sanitize_ips(output_file, output_file)


def run_proxy_checker_test() -> None:
    """Run the proxy checker test"""

    # get the file path
    file_path = input("Enter the file path: ").strip()

    # check if the file exists
    if not os.path.exists(file_path):
        print("[!] File does not exist.")
        return

    # check if the file is a file
    if not os.path.isfile(file_path):
        print("[!] Invalid file path.")
        return

    # get the output file path
    output_file = input(
        "Enter the output path for active proxies (default: output.txt): "
    ).strip()

    # check if the output file is provided
    if not output_file:
        output_file = "output.txt"

    # check if the output file is a text file
    if not output_file.endswith(".txt"):
        output_file += ".txt"

    # run the proxy checker
    internals.run_proxy_checker(file_path, output_file)


def main() -> None:
    """Main CLI function for the proxy_scrapper package"""

    while True:
        print(
            """
Welcome to the Proxy Scrapper CLI
    1. Get and save IP addresses from URLs
    2. Check proxy status
    0. Exit
        """
        )
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            get_and_save_ips_from_file_urls()
        elif choice == "2":
            run_proxy_checker_test()
        elif choice == "0":
            print("[-] Exiting...")
            break
        else:
            print("[!] Invalid choice. Please try again.")
            continue


if __name__ == "__main__":
    main()
