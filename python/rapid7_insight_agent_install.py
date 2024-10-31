import argparse
import requests
import os
import subprocess
import sys

def download_file(url, target_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(target_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def install_msi(msi_path, target_directory, token):
    command = [
        "msiexec", "/i", msi_path,
        "/l*v", "insight_agent_install_log.log",
        f"CUSTOMCONFIGPATH={target_directory}",
        f"CUSTOMTOKEN={token}",
        "/quiet"
    ]
    subprocess.run(command, check=True)

def load_env_file(file_path):
    if not os.path.exists(file_path):
        return {}
    env_vars = {}
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars

def main():
    env_vars = load_env_file('.env')

    parser = argparse.ArgumentParser(description="Download and install Rapid7 Insight Agent.")
    parser.add_argument("--url", help="URL to download the MSI installer")
    parser.add_argument("--target_directory", help="Target directory for dependencies")
    parser.add_argument("--token", help="Custom token for installation")
    args = parser.parse_args()

    # Get values from environment variables if not provided via command-line arguments
    url = args.url or env_vars.get("RAPID7_URL")
    target_directory = args.target_directory or env_vars.get("RAPID7_TARGET_DIRECTORY")
    token = args.token or env_vars.get("RAPID7_TOKEN")

    # Prompt user for input if values are still not provided
    if not url:
        url = input("Please enter the URL to download the MSI installer: ")
    if not target_directory:
        target_directory = input("Please enter the target directory for dependencies: ")
    if not token:
        token = input("Please enter the custom token for installation: ")

    # Validate and normalize the target directory
    target_directory = os.path.abspath(target_directory)
    if not os.path.isdir(target_directory):
        print(f"Error: The target directory '{target_directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    msi_path = os.path.join(target_directory, "agentInstaller.msi")

    try:
        print("Downloading MSI installer...")
        download_file(url, msi_path)
        print("Download complete.")

        print("Installing MSI installer...")
        install_msi(msi_path, target_directory, token)
        print("Installation complete.")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()