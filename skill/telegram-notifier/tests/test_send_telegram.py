import importlib.util
import ssl
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "send_telegram.py"
SPEC = importlib.util.spec_from_file_location("send_telegram", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BuildSslContextTests(unittest.TestCase):
    def test_prefers_system_cert_bundle_on_macos(self) -> None:
        sentinel = ssl.create_default_context()

        with mock.patch.object(MODULE.sys, "platform", "darwin"):
            with mock.patch.object(MODULE.Path, "exists", return_value=True):
                with mock.patch.object(
                    MODULE.ssl, "create_default_context", return_value=sentinel
                ) as create_default_context:
                    context = MODULE.build_ssl_context()

        self.assertIs(context, sentinel)
        create_default_context.assert_called_once_with(cafile="/etc/ssl/cert.pem")


if __name__ == "__main__":
    unittest.main()
