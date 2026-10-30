import json
import sys
from pathlib import Path


profiles_path = Path(__file__).with_name("profiles.json")
with profiles_path.open(encoding="utf-8") as file:
    profiles = json.load(file)

first, second = profiles[0], profiles[1]
choice = sys.argv[1].upper() if len(sys.argv) > 1 else "A"
if choice not in ("A", "B"):
    raise SystemExit("Укажи A или B: python stage_2_compare.py A")

selected = first if choice == "A" else second
winner = max((first, second), key=lambda profile: profile["readers"])
print("Выбран:", selected["name"])
print("Правильный ответ:", "A" if winner is first else "B")
