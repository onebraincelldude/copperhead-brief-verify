"""brief-verify: requirements-coverage check for design-brief agents.

The agent turns NL requirements into a design brief: items with a design choice plus the
requirement IDs it addresses. Blocks on: requirements no item addresses (orphans) and items
citing requirements that do not exist or that their choice text does not mention (unsupported
choices). Exit 1 = verifier blocks the brief.
"""
import json, sys

def load_agent(path):
    if not path:
        return demo_agent
    import importlib.util
    s = importlib.util.spec_from_file_location("agent", path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m.run

def demo_agent(requirements):
    """Naive agent: drops the size requirement, adds an unjustified Wi-Fi radio."""
    return [
        {"item": "CR2032 3.3V coin cell power stage", "addresses": ["R1"]},
        {"item": "60-second temperature sampling loop on the MCU timer", "addresses": ["R2"]},
        {"item": "BLE 5.0 radio for transmission", "addresses": ["R3"]},
        {"item": "Wi-Fi fallback radio for range", "addresses": ["R9"]}]

def main():
    spec = json.load(open("cases.json"))
    agent = load_agent(sys.argv[1] if len(sys.argv) > 1 else None)
    orphans = unsupported = 0
    for c in spec["cases"]:
        reqs = {r["id"]: r["text"].lower() for r in c["requirements"]}
        brief = agent(c["requirements"])
        covered = set()
        for item in brief:
            ids = item.get("addresses", [])
            valid = [i for i in ids if i in reqs]
            if not valid:
                unsupported += 1
                print(f"[{c['id']}] UNSUPPORTED item '{item['item'][:50]}' (cites {ids or 'nothing'})")
                continue
            covered.update(valid)
        missing = [i for i in reqs if i not in covered]
        if missing:
            orphans += len(missing)
            print(f"[{c['id']}] ORPHAN requirements unaddressed: {missing}")
        if not missing and unsupported == 0:
            print(f"[{c['id']}] brief fully traced")
    g = spec["gates"]
    ok = orphans <= g["max_orphan_requirements"] and unsupported <= g["max_unsupported_items"]
    print(f"\norphan requirements {orphans} (gate {g['max_orphan_requirements']}), unsupported items {unsupported} (gate {g['max_unsupported_items']})")
    print("BRIEF:", "PASS" if ok else "BLOCKED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
