import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


REQUIRED_KEYS = ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")


def load_config(config_path: Path) -> dict[str, str]:
    if not config_path.exists():
        raise FileNotFoundError(f"telegram-notifier config not found: {config_path}")

    config: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        config_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid config line {line_number}: {line}")
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()

    missing = [key for key in REQUIRED_KEYS if not config.get(key)]
    if missing:
        raise ValueError(f"Missing required config: {', '.join(missing)}")

    return config


def send_message(config: dict[str, str], message_text: str) -> tuple[bool, str]:
    url = f"https://api.telegram.org/bot{config['TELEGRAM_BOT_TOKEN']}/sendMessage"
    payload = json.dumps(
        {"chat_id": config["TELEGRAM_CHAT_ID"], "text": message_text}
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
        reason = getattr(exc, "reason", None) or str(exc) or exc.__class__.__name__
        return False, str(reason)

    if body.get("ok"):
        return True, "sent"
    return False, str(body.get("description", "Telegram API error"))


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[0] != "--config" or not argv[1].strip():
        print("Error: must provide --config <path> and a message.", file=sys.stderr)
        return 1

    config_path = Path(argv[1])
    message_text = " ".join(argv[2:]).strip()
    if not message_text:
        print("Error: message is required.", file=sys.stderr)
        return 1

    try:
        config = load_config(config_path)
        ok, detail = send_message(config, message_text)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not ok:
        print(f"Error: {detail}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
