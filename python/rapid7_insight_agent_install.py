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

def main():
    parser = argparse.ArgumentParser(description="Download and install Rapid7 Insight Agent.")
    parser.add_argument("url", help="URL to download the MSI installer")
    parser.add_argument("target_directory", help="Target directory for dependencies")
    parser.add_argument("token", help="Custom token for installation")
    args = parser.parse_args()

    # Validate and normalize the target directory
    target_directory = os.path.abspath(args.target_directory)
    if not os.path.isdir(target_directory):
        print(f"Error: The target directory '{target_directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    msi_path = os.path.join(target_directory, "agentInstaller.msi")

    try:
        print("Downloading MSI installer...")
        download_file(args.url, msi_path)
        print("Download complete.")

        print("Installing MSI installer...")
        install_msi(msi_path, target_directory, args.token)
        print("Installation complete.")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()