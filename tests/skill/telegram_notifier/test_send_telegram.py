import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = PROJECT_ROOT / "skill/telegram-notifier/scripts/send_telegram.py"


def load_send_telegram_module():
    if not SCRIPT_PATH.exists():
        raise AssertionError(
            f"Missing implementation module: {SCRIPT_PATH}. "
            "Create send_telegram.py to make these tests pass."
        )

    spec = importlib.util.spec_from_file_location("send_telegram", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module spec from {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload):
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class SendTelegramTests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = load_send_telegram_module()
        except AssertionError as exc:
            self.fail(str(exc))

    def write_config(self, contents):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "notifier.env"
        path.write_text(contents, encoding="utf-8")
        return path

    def test_load_config_raises_file_not_found_for_missing_file(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        missing_path = Path(temp_dir.name) / "telegram-notifier-missing.env"

        with self.assertRaisesRegex(FileNotFoundError, "telegram-notifier"):
            self.module.load_config(missing_path)

    def test_load_config_reads_required_values(self):
        config_path = self.write_config(
            "\n".join(
                [
                    "# comment",
                    "",
                    "TELEGRAM_BOT_TOKEN=test-token",
                    "TELEGRAM_CHAT_ID=12345",
                ]
            )
        )

        config = self.module.load_config(config_path)

        self.assertIsInstance(config, dict)
        self.assertEqual(config["TELEGRAM_BOT_TOKEN"], "test-token")
        self.assertEqual(config["TELEGRAM_CHAT_ID"], "12345")

    def test_load_config_rejects_empty_required_value(self):
        config_path = self.write_config(
            "\n".join(
                [
                    "TELEGRAM_BOT_TOKEN=",
                    "TELEGRAM_CHAT_ID=12345",
                ]
            )
        )

        with self.assertRaisesRegex(ValueError, "TELEGRAM_BOT_TOKEN"):
            self.module.load_config(config_path)

    def test_load_config_rejects_invalid_line_without_equals(self):
        config_path = self.write_config(
            "\n".join(
                [
                    "TELEGRAM_BOT_TOKEN=test-token",
                    "BROKEN_LINE",
                    "TELEGRAM_CHAT_ID=12345",
                ]
            )
        )

        with self.assertRaisesRegex(ValueError, "BROKEN_LINE"):
            self.module.load_config(config_path)

    def test_send_message_posts_json_with_chat_id_and_text(self):
        config = {
            "TELEGRAM_BOT_TOKEN": "bot-token",
            "TELEGRAM_CHAT_ID": "chat-123",
        }

        with mock.patch(
            "urllib.request.urlopen",
            return_value=FakeResponse({"ok": True, "result": {"message_id": 1}}),
        ) as mock_urlopen:
            self.module.send_message(config, "done")

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://api.telegram.org/botbot-token/sendMessage",
        )
        self.assertEqual(request.get_header("Content-type"), "application/json")

        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["chat_id"], "chat-123")
        self.assertIn("text", payload)
        self.assertEqual(payload["text"], "done")

    def test_send_message_returns_failure_status_for_telegram_api_error(self):
        config = {
            "TELEGRAM_BOT_TOKEN": "bot-token",
            "TELEGRAM_CHAT_ID": "chat-123",
        }

        with mock.patch(
            "urllib.request.urlopen",
            return_value=FakeResponse({"ok": False, "description": "Bad Request"}),
        ):
            result = self.module.send_message(config, "done")

        self.assertEqual(result, (False, "Bad Request"))

    def test_send_message_returns_failure_status_for_network_error(self):
        config = {
            "TELEGRAM_BOT_TOKEN": "bot-token",
            "TELEGRAM_CHAT_ID": "chat-123",
        }

        with mock.patch(
            "urllib.request.urlopen",
            side_effect=OSError("network down"),
        ):
            result = self.module.send_message(config, "done")

        self.assertEqual(result, (False, "network down"))

    def test_main_returns_1_when_config_argument_is_omitted(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = self.module.main(["done"])

        self.assertEqual(exit_code, 1)
        combined_output = f"{stdout.getvalue()}\n{stderr.getvalue()}".lower()
        self.assertIn("config", combined_output)
        self.assertRegex(combined_output, r"must|required|provide")

    def test_main_returns_1_when_config_loading_fails(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with mock.patch.object(
            self.module, "load_config", side_effect=OSError("permission denied")
        ):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = self.module.main(["--config", "repo.env", "done"])

        self.assertEqual(exit_code, 1)
        combined_output = f"{stdout.getvalue()}\n{stderr.getvalue()}".lower()
        self.assertIn("permission denied", combined_output)


if __name__ == "__main__":
    unittest.main()
