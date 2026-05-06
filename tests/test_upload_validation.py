
import io
import unittest

import app as app_module
from app import app


class TestUploadValidation(unittest.TestCase):
    def setUp(self):
        # Isolate every test by clearing the in-memory scan store.
        app_module._scan_store.clear()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        app_module._scan_store.clear()

    def test_rejects_non_python_extension(self):
        """
        NFR-01 (Security Detection Accuracy) / FR-1 (Allow users to submit
        source code files). The /upload endpoint must reject any file whose
        extension is not .py. Reject = the file is not added to _scan_store.

        Note: the payload is syntactically valid Python so the SyntaxError
        guard in app.py cannot mask the missing extension check. The only
        thing that should keep this file out of _scan_store is server-side
        extension validation - which is currently absent.
        """
        evil_bytes = b"x = 1\n"  # valid Python, but extension is .exe
        data = {
            "files": (io.BytesIO(evil_bytes), "evil.exe"),
        }
        self.client.post(
            "/upload",
            data=data,
            content_type="multipart/form-data",
        )
        self.assertEqual(
            len(app_module._scan_store),
            0,
            "Non-.py upload was accepted into _scan_store; "
            "server-side extension validation is missing.",
        )

    def test_rejects_oversize_upload(self):
        """
        NFR-04 (Code Maintainability / resource safety) and the Known
        Limitations gap. Uploads larger than 1 MB must be rejected, and
        the file must NOT be added to _scan_store. The rejection may be
        signalled either by Flask's native 413 Request Entity Too Large,
        or by the application's own 413 errorhandler (which redirects to
        the dashboard with a flash message). Both are valid rejections
        as long as the resource-safety guarantee holds: the oversize
        payload never reaches _scan_store.
        """
        big_bytes = b"x = 1\n" * 200_000  # ~1.2 MB of valid Python
        data = {
            "files": (io.BytesIO(big_bytes), "big.py"),
        }
        response = self.client.post(
            "/upload",
            data=data,
            content_type="multipart/form-data",
        )
        # Either Flask's native 413, or a redirect from the app's 413 handler.
        self.assertIn(
            response.status_code,
            (302, 413),
            f"Oversize upload returned unexpected status {response.status_code}; "
            "expected 413 (Flask native) or 302 (redirect from 413 errorhandler).",
        )
        # The critical resource-safety assertion: oversize file must not be stored.
        self.assertEqual(
            len(app_module._scan_store),
            0,
            "Oversize upload was added to _scan_store; "
            "MAX_CONTENT_LENGTH is not enforced.",
        )


if __name__ == "__main__":
    unittest.main()
