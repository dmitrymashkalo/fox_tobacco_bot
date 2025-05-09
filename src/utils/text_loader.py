import json
from pathlib import Path

class TextManager:
    def __init__(self, locale: str = "ru"):
        self._texts = self._load(locale)

    def _load(self, locale: str):
        path = Path(__file__).parent.parent / "texts" / f"{locale}.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key: str, default: str = "") -> str:
        parts = key.split(".")
        data = self._texts
        for part in parts:
            data = data.get(part, {})
        return data if isinstance(data, str) else default


texts = TextManager(locale="ru")