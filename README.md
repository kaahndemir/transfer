# AirTransit CLI 🚀

**AirTransit** is a Python command-line tool for sharing files through the Catbox HTTPS service, with short download codes and terminal QR codes. It uses a hosted relay instead of a direct peer-to-peer connection.

Project maintainer: [Kaan Demir](https://kaahn.com/hakkimda/) (Oğuz Kaan Demir), software developer in Istanbul.

No Catbox account is required by the upload command. Files are uploaded to a third-party host, and the download URL is also sent to qrenco.de to generate the terminal QR code.

---

## Features
* **HTTPS Relay**: Uploads and downloads through Catbox, avoiding the need for a direct P2P connection. Availability depends on the network and service.
* **No Python Package Dependencies**: Uses the Python 3 standard library. No `pip install` required; Catbox and qrenco.de are external services.
* **Short Codes**: Uses the filename returned by Catbox (e.g. `f8agka.txt`) so you don't have to type long URLs.
* **Terminal QR Codes**: Renders a scannable ASCII QR code directly on your terminal screen when sending a file, allowing you to download files on your phone instantly.
* **HTTPS Uploads**: The upload endpoint uses TLS. The tool does not encrypt file contents before uploading or add access control to the returned link.

---

## How It Works (The Traversal)
Direct peer-to-peer transfers can fail behind restrictive NAT or firewall configurations. AirTransit instead uploads the file to Catbox and downloads it through the returned URL.

The CLI enforces a 200MB upload limit. It does not set a deletion time for hosted files. HTTPS access to the service can still be blocked by a network's rules.

---

## Installation

### macOS & Linux
1. Clone the repository:
   ```bash
   git clone https://github.com/kaahndemir/transfer.git ~/kaahn/dev/transfer
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

## Review and citation

See [review notes and offline checks](docs/review-notes.md) for a reproducible,
network-free walkthrough and the data-path limitations. Use GitHub's **Cite this
repository** menu, backed by [CITATION.cff](CITATION.cff), and include the commit
you reviewed when referencing the implementation.
