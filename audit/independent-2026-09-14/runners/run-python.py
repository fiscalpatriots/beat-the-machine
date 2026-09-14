"""Runs checker inputs through second_pass.checker at a given tree, using that tree's
own probe builder (tests/test_checker_contract.probe). Independent audit A1.
usage: python run-python.py <trainer-root> <inputs.json> <out.json>"""
import json, sys, os, traceback
trainer, in_file, out_file = sys.argv[1:4]
sys.path.insert(0, trainer)
os.chdir(trainer)
from tests.test_checker_contract import probe
items = json.load(open(in_file, encoding="utf-8"))
out = []
for it in items:
    try:
        p = probe(it)
        keep = {k: p.get(k) for k in ("ran", "status", "role", "stats", "queueKinds", "finding", "survivors",
                                      "queue", "csv", "tsv", "json", "prompt", "pageText", "accounts", "flags")}
        keep["id"] = it["id"]
        out.append(keep)
    except Exception as exc:
        out.append({"id": it["id"], "error": "%s: %s" % (type(exc).__name__, exc),
                    "trace": traceback.format_exc()[-600:]})
json.dump(out, open(out_file, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("python ran", len(out), "inputs,", sum(1 for o in out if "error" in o), "threw")
