import json
import os
import sys
from pathlib import Path


class Gate:
    LIMIT = 200
    LABEL = "last-text-at-one-percent"

    def __init__(self, folder):
        self.folder = folder
        self.source = folder / "entry.txt"

    def load(self):
        payload = self.source.read_bytes()
        text = payload.decode("utf-8")
        return payload, text

    def verdict(self, text):
        body = text.strip()
        inside = 1 <= len(body) <= self.LIMIT and len(text) <= self.LIMIT
        return inside


class Copier:
    def __init__(self, root):
        chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
        self.root = Path(chosen) if chosen else root / "out"

    def place(self, payload):
        self.root.mkdir(parents=True, exist_ok=True)
        target = self.root / "entry.txt"
        target.write_bytes(payload)
        return target


def main():
    here = Path(__file__).resolve().parent
    gate = Gate(here)
    payload, text = gate.load()
    good = gate.verdict(text)
    copier = Copier(here)
    where = copier.place(payload)
    receipt = {"label": Gate.LABEL, "stamp": "lt1p-r1", "entry": str(where), "chars": len(text), "valid": good}
    print(json.dumps(receipt))
    if not good:
        sys.exit(2)


if __name__ == "__main__":
    main()
