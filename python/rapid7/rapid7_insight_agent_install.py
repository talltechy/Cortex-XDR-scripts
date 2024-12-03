"""
Rapid7 Insight Agent Installer Script

This script automates the process of downloading and installing the Rapid7 Insight Agent.
It performs the following steps:
1. Parses command-line arguments for URL, target directory, and token.
2. Validates that the required URL and token are provided.
3. Validates and normalizes the target directory.
4. Ensures the target directory is writable.
5. Downloads the MSI installer to the target directory.
6. Installs the MSI installer using the provided token.

Usage:
    python rapid7_insight_agent_install.py --url <MSI_URL> --target_directory <TARGET_DIR> --token <TOKEN>

Arguments:
    --url: URL to download the MSI installer.
    --target_directory: Target directory for dependencies.
    --token: Custom token for installation.

Example:
    python rapid7_insight_agent_install.py --url https://example.com/installer.msi --target_directory C:/path/to/dir --token your_token

Dependencies:
    - requests: To download the MSI installer.
    - subprocess: To run the msiexec command for installation.
    - argparse: To parse command-line arguments.
    - os: To handle file and directory operations.
    - sys: To handle system-specific parameters and functions.

Raises:
    requests.exceptions.RequestException: If there is an issue with the HTTP request.
    IOError: If there is an issue writing the file to the target path.
    subprocess.CalledProcessError: If the msiexec command fails.

Author:
    Matt Wyen
    https://github.com/talltechy
    matt@wyen.me
"""

import argparse
import os
import subprocess
import sys
import requests

def download_file(url, target_path):
    """
    Downloads a file from the specified URL and saves it to the target path.

    Args:
        url (str): The URL of the file to download.
        target_path (str): The local file path where the downloaded file will be saved.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        IOError: If there is an issue writing the file to the target path.
    """
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with open(target_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def install_msi(msi_path, target_directory, token):
    """
    Installs an MSI package using the Windows Installer (msiexec) command.

    Args:
        msi_path (str): The file path to the MSI package to be installed.
        target_directory (str): The directory where the custom configuration will be stored.
        token (str): The custom token required for the installation.

    Raises:
        subprocess.CalledProcessError: If the msiexec command fails.
    """
    command = [
        "msiexec", "/i", msi_path,
        "/l*v", "insight_agent_install_log.log",
        f"CUSTOMCONFIGPATH={target_directory}",
        f"CUSTOMTOKEN={token}",
        "/quiet"
    ]
    subprocess.run(command, check=True)

def main():
    """
    Main function to download and install the Rapid7 Insight Agent.

    This function performs the following steps:
    1. Parses command-line arguments for URL, target directory, and token.
    2. Validates that the required URL and token are provided.
    3. Validates and normalizes the target directory.
    4. Ensures the target directory is writable.
    5. Downloads the MSI installer to the target directory.
    6. Installs the MSI installer using the provided token.

    If any required arguments are missing or if any errors occur during the
    download or installation process, the function will print an error message
    to stderr and exit with a non-zero status code.
    """
    parser = argparse.ArgumentParser(description="Download and install Rapid7 Insight Agent.")
    parser.add_argument("--url", required=True, help="URL to download the MSI installer")
    parser.add_argument("--target_directory", required=True, help="Target directory for dependencies")
    parser.add_argument("--token", required=True, help="Custom token for installation")
    args = parser.parse_args()

    url = args.url
    target_directory = os.path.abspath(args.target_directory)
    token = args.token

    # Validate and normalize the target directory
    if not os.path.isdir(target_directory):
        print(f"Error: The target directory '{target_directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Ensure the target directory is writable
    if not os.access(target_directory, os.W_OK):
        print(f"Error: The target directory '{target_directory}' is not writable.", file=sys.stderr)
        sys.exit(1)

    msi_path = os.path.join(target_directory, "agentInstaller.msi")

    try:
        print("Downloading MSI installer...")
        download_file(url, msi_path)
        print("Download complete.")

        print("Installing MSI installer...")
        install_msi(msi_path, target_directory, token)
        print("Installation complete.")
    except (requests.RequestException, subprocess.CalledProcessError, OSError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
