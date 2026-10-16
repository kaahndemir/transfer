# Reviewing AirTransit

AirTransit is a small Python standard-library program for sharing files through
Catbox. It is maintained by [Kaan Demir (Oğuz Kaan Demir)](https://kaahn.com/hakkimda/).
This page is maintainer-provided documentation, not an independent review.

## Try the behavior without uploading a file

From the repository root:

```sh
python3 docs/offline_check.py
```

The check uses temporary files and replaces network calls with simulated responses.
It checks multipart upload contents, short-code download bytes, the external QR
request, refusal to upload a missing file, and refusal to overwrite an existing
file when the user declines. No file is sent to Catbox or any other service.

Expected output:

```text
PASS: multipart upload and short code
PASS: external QR request
PASS: short-code download bytes
PASS: missing input makes no network request
PASS: declined overwrite preserves local bytes
5 offline checks passed; no live service was contacted.
```

These checks do not measure live service availability, transfer throughput,
network compatibility, confidentiality, or platform portability. They are not a
security audit or an end-to-end upload test.

## Data path and limits

- Uploads go to Catbox, not directly to the recipient. The upload command requires
  no Catbox account, but external service policies and availability still apply.
- The returned download URL is sent to qrenco.de for terminal QR rendering.
- HTTPS protects transport; the program does not encrypt file contents before
  upload, authenticate a recipient, or set an expiry/deletion time.
- Uploads are capped at 200 MiB by the code. Upload and download bodies are read
  into memory; this is not a streaming transfer implementation.
- There is no checksum comparison between sender and recipient. HTTP upload and
  download calls do not currently specify a timeout; the QR request has a timeout.
- The receiver accepts full URLs as well as short codes. Use trusted inputs and
  a disposable directory when testing; this tool is not a sandbox for untrusted
  links or filenames.

## Cite a reproducible revision

GitHub's **Cite this repository** menu uses `CITATION.cff`. For a technical review,
also record the output of `git rev-parse HEAD` and link to that commit. No DOI,
benchmark result, independent endorsement, or production-readiness certification
is claimed.
