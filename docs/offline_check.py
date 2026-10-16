"""Exercise documented behavior with synthetic data and no live network calls."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("airtransit", ROOT / "transfer.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def run_checks():
    original_directory = Path.cwd()
    with tempfile.TemporaryDirectory() as directory:
        try:
            os.chdir(directory)
            Path("sample.txt").write_bytes(b"Synthetic review fixture\n")
            output = io.StringIO()
            with patch.object(app.urllib.request, "urlopen", return_value=io.BytesIO(
                b"https://files.catbox.moe/example.txt\n"
            )) as network, patch.object(app, "print_qr_code") as qr, contextlib.redirect_stdout(output):
                app.upload_file("sample.txt")
                request = network.call_args.args[0]
                assert request.full_url == "https://catbox.moe/user/api.php"
                assert b'Synthetic review fixture\n' in request.data
                assert b'name="fileToUpload"; filename="sample.txt"' in request.data
                assert "example.txt" in output.getvalue()
                qr.assert_called_once_with("https://files.catbox.moe/example.txt")
            print("PASS: multipart upload and short code")

            with patch.object(app.urllib.request, "urlopen", return_value=io.BytesIO(b"SIMULATED QR")) as network, contextlib.redirect_stdout(io.StringIO()):
                app.print_qr_code("https://files.catbox.moe/example.txt")
                assert network.call_args.args[0].full_url == "https://qrenco.de/https%3A%2F%2Ffiles.catbox.moe%2Fexample.txt"
                assert network.call_args.kwargs["timeout"] == 5
            print("PASS: external QR request")

            with patch.object(app.urllib.request, "urlopen", return_value=io.BytesIO(b"download fixture")) as network, contextlib.redirect_stdout(io.StringIO()):
                app.download_file("example.txt")
                assert network.call_args.args[0].full_url == "https://files.catbox.moe/example.txt"
                assert Path("example.txt").read_bytes() == b"download fixture"
            print("PASS: short-code download bytes")

            with patch.object(app.urllib.request, "urlopen", side_effect=AssertionError("Unexpected network call")) as network, contextlib.redirect_stdout(io.StringIO()):
                app.upload_file("missing.txt")
                network.assert_not_called()
            print("PASS: missing input makes no network request")

            with patch.object(app.urllib.request, "urlopen", side_effect=AssertionError("Unexpected network call")) as network, patch("builtins.input", return_value="n"), contextlib.redirect_stdout(io.StringIO()):
                app.download_file("example.txt")
                network.assert_not_called()
                assert Path("example.txt").read_bytes() == b"download fixture"
            print("PASS: declined overwrite preserves local bytes")
        finally:
            os.chdir(original_directory)
    print("5 offline checks passed; no live service was contacted.")


if __name__ == "__main__":
    run_checks()
