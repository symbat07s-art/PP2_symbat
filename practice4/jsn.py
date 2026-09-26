import json
import os

file_path = os.path.join(os.path.dirname(__file__), "sample-data.json")

with open(file_path, "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50}{'Description':<20}{'Speed':<8}{'MTU':<5}")
print("-" * 50 + " " + "-" * 20 + " " + "-" * 6 + " " + "-" * 6)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes["dn"]
    description = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")

    print(f"{dn:<50}{description:<20}{speed:<8}{mtu:<5}")