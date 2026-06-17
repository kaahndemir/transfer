# AirTransit CLI 🚀

**AirTransit** is a lightweight, zero-dependency command-line file sharing tool designed to traverse highly restrictive school, university, and corporate firewalls (including Symmetric NATs) where traditional WebRTC or P2P connections fail.

It provides a completely anonymous, registration-free, and QR-code friendly way to send files between your computers and mobile devices.

---

## Features
* **Symmetric NAT Traversal**: Uses secure HTTPS (Port 443) relays, ensuring traffic is never blocked by strict firewalls (like 42 networks).
* **Zero Dependencies**: Written in pure Python 3 using standard libraries (`urllib`, `tkinter`, etc.). No `pip install` required!
* **Short Codes**: Generates short 6-character transfer codes (e.g. `f8agka.txt`) so you don't have to type long URLs.
* **Terminal QR Codes**: Renders a scannable ASCII QR code directly on your terminal screen when sending a file, allowing you to download files on your phone instantly.
* **Anonymous & Secure**: No accounts or sign-ups required. Files are encrypted in transit via TLS.

---

## How It Works (The Traversal)
In strict networks (like the 42 school network), routers employ a **Symmetric NAT** which dynamically rewrites your external port mapping for every new destination IP you connect to. This completely breaks standard WebRTC hole punching. 

AirTransit bypasses this by uploading and downloading files directly through standard HTTPS web endpoints. Since HTTPS traffic on port 443 is required for normal web browsing, it is never blocked by firewalls. Under the hood, files are temporarily hosted on a free anonymous storage relay (Catbox.moe) for up to 200MB per file.

---

## Installation

### macOS & Linux
1. Clone the repository:
   ```bash
   git clone https://github.com/ogudemir/transfer.git ~/kaahn/dev/transfer
   cd ~/kaahn/dev/transfer
   ```
2. Run the installer script:
   ```bash
   ./install.sh
   ```
3. That's it! The `transfer` command is now available globally in your terminal.

---

## Usage

### 1. Send a File (PC → Mobile / Another PC)
Upload any file (up to 200MB) from your terminal:
```bash
transfer send project.tar.gz
```
**Output:**
```text
Uploading 'project.tar.gz' (4.20 MB) to Catbox...

✓ Upload Successful!
----------------------------------------
Short Code:   j85pg4.txt
Direct URL:   https://files.catbox.moe/j85pg4.txt
----------------------------------------
To download on another PC, run:
  transfer receive j85pg4.txt

Scan to Download:
█████████████████████████████████████
█████████████████████████████████████
████ ▄▄▄▄▄ █▀█ █▄ ▀ █ ▄▄ █ ▄▄▄▄▄ ████
...
```
* **For Phones:** Point your phone camera at the terminal screen to scan the QR code and download the file.
* **For other PCs:** Run `transfer receive j85pg4.txt`.

### 2. Receive a File (Mobile / Another PC → PC)
1. On your sending device, open your browser and go to [catbox.moe](https://catbox.moe).
2. Upload your file anonymously. It will generate a link (e.g., `https://files.catbox.moe/x9ykd2.jpg`).
3. On your target PC terminal, run:
   ```bash
   transfer receive x9ykd2.jpg
   ```
   *(AirTransit will automatically resolve the short code and download the file directly into your current directory).*

---

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
