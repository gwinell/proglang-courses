import json
from pathlib import Path


profiles_path = Path(__file__).with_name("profiles.json")
with profiles_path.open(encoding="utf-8") as file:
    profiles = json.load(file)

print("Всего профилей:", len(profiles))
for profile in profiles:
    print(profile["name"], "—", profile["profession"])
