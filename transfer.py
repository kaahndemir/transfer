#!/usr/bin/env python3
import os
import sys
import uuid
import urllib.request
import urllib.parse

# Terminal color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def print_help():
    print(f"""{BOLD}{CYAN}AirTransit CLI{RESET} - Traverses strict school/NAT networks securely.

{BOLD}Usage:{RESET}
  transfer send <filepath>        {YELLOW}Upload a file (up to 200MB){RESET}
  transfer receive <code>         {YELLOW}Download a file using the short code or URL{RESET}

{BOLD}Examples:{RESET}
  transfer send project.tar.gz
  transfer receive abcdef.tar.gz
  transfer receive https://files.catbox.moe/abcdef.tar.gz
""")

def print_qr_code(url):
    try:
        # qrenco.de returns the ASCII QR code when accessed via curl User-Agent
        encoded_url = urllib.parse.quote(url, safe='')
        req = urllib.request.Request(
            f"https://qrenco.de/{encoded_url}",
            headers={"User-Agent": "curl/7.68.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            qr_text = response.read().decode('utf-8')
            print(f"\n{BOLD}{CYAN}Scan to Download:{RESET}")
            print(qr_text)
    except Exception:
        pass

def upload_file(path):
    if not os.path.exists(path):
        print(f"{RED}{BOLD}Error:{RESET} File '{path}' does not exist.")
        return
        
    if not os.path.isfile(path):
        print(f"{RED}{BOLD}Error:{RESET} '{path}' is not a file.")
        return
        
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > 200:
        print(f"{RED}{BOLD}Error:{RESET} File size ({size_mb:.2f}MB) exceeds the 200MB limit.")
        return

    filename = os.path.basename(path)
    print(f"{CYAN}Uploading '{filename}' ({size_mb:.2f} MB) to Catbox...{RESET}")
    
    try:
        boundary = uuid.uuid4().hex
        with open(path, 'rb') as f:
            file_data = f.read()
            
        parts = []
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(b'Content-Disposition: form-data; name="reqtype"')
        parts.append(b'')
        parts.append(b'fileupload')
        
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"'.encode('utf-8'))
        parts.append(b'Content-Type: application/octet-stream')
        parts.append(b'')
        parts.append(file_data)
        
        parts.append(f'--{boundary}--'.encode('utf-8'))
        parts.append(b'')
        
        payload = b'\r\n'.join(parts)
        
        req = urllib.request.Request(
            'https://catbox.moe/user/api.php',
            data=payload,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'Mozilla/5.0'
            }
        )
        
        with urllib.request.urlopen(req) as r:
            url = r.read().decode('utf-8').strip()
            
        code = url.split('/')[-1]
        
        print(f"\n{GREEN}{BOLD}✓ Upload Successful!{RESET}")
        print(f"----------------------------------------")
        print(f"{BOLD}Short Code:{RESET}   {MAGENTA}{BOLD}{code}{RESET}")
        print(f"{BOLD}Direct URL:{RESET}   {CYAN}{url}{RESET}")
        print(f"----------------------------------------")
        print(f"To download on another PC, run:")
        print(f"  {YELLOW}transfer receive {code}{RESET}")
        
        # Output the QR code for phones
        print_qr_code(url)
        
    except Exception as e:
        print(f"\n{RED}{BOLD}✗ Upload Failed!{RESET}")
        print(f"Network error or SSL verification issue: {e}")

def download_file(code):
    # If the user passed the full URL, parse the code out of it
    if code.startswith("http://") or code.startswith("https://"):
        url = code
        filename = url.split('/')[-1]
    else:
        url = f"https://files.catbox.moe/{code}"
        filename = code

    # Check if file already exists in local directory to prevent accidental overwrites
    if os.path.exists(filename):
        overwrite = input(f"{YELLOW}Warning: '{filename}' already exists. Overwrite? (y/N): {RESET}").strip().lower()
        if overwrite != 'y':
            print("Download cancelled.")
            return

    print(f"{CYAN}Downloading from {url}...{RESET}")
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as r:
            file_data = r.read()
            
        with open(filename, "wb") as f:
            f.write(file_data)
            
        print(f"\n{GREEN}{BOLD}✓ Download Successful!{RESET}")
        print(f"File saved as: {BOLD}{filename}{RESET} ({len(file_data) / 1024:.2f} KB)")
        
    except Exception as e:
        print(f"\n{RED}{BOLD}✗ Download Failed!{RESET}")
        print(f"Ensure the code is correct and you have internet access: {e}")

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()
    
    if command == "send":
        if len(sys.argv) < 3:
            print(f"{RED}Error: Please specify the file path to send.{RESET}")
            print("Usage: transfer send <filepath>")
            return
        upload_file(sys.argv[2])
    elif command in ("receive", "get"):
        if len(sys.argv) < 3:
            print(f"{RED}Error: Please specify the code or URL to receive.{RESET}")
            print("Usage: transfer receive <code>")
            return
        download_file(sys.argv[2])
    else:
        print(f"{RED}Unknown command: '{command}'{RESET}")
        print_help()

if __name__ == "__main__":
    main()
