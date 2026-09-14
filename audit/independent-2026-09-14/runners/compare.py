"""Compares browser and python outputs field by field with the normalization the
second-pass parity test documents (ISO timestamps masked, json and queue parsed).
usage: python compare.py <browser.json> <python.json> <out.json>"""
import json, re, sys
ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z")
FIELDS = ("status", "role", "stats", "queueKinds", "finding", "survivors", "queue", "csv", "tsv", "json", "prompt")
def norm(field, v):
    if v is None:
        v = {} if field in ("status", "role", "stats", "finding") else ""
    if field in ("json", "queue"):
        t = ISO.sub("<timestamp>", v) if isinstance(v, str) else v
        try:
            return json.loads(t) if isinstance(t, str) and t else t
        except Exception:
            return t
    if isinstance(v, str):
        return ISO.sub("<timestamp>", v)
    return v
b = {x["id"]: x for x in json.load(open(sys.argv[1], encoding="utf-8"))}
p = {x["id"]: x for x in json.load(open(sys.argv[2], encoding="utf-8"))}
res = []
for k in b:
    x, y = b[k], p.get(k, {})
    if "error" in x or "error" in y:
        res.append({"id": k, "browserError": x.get("error"), "pythonError": y.get("error"),
                    "differingFields": ["error"], "browserStatus": x.get("status"), "pythonStatus": y.get("status")})
        continue
    diff = [f for f in FIELDS if norm(f, x.get(f)) != norm(f, y.get(f))]
    res.append({"id": k, "differingFields": diff, "sameStatus": x.get("status") == y.get("status"),
                "browserStatus": x.get("status"), "pythonStatus": y.get("status")})
json.dump(res, open(sys.argv[3], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("compared", len(res), "| same status:", sum(1 for r in res if r.get("sameStatus")),
      "| all fields equal:", sum(1 for r in res if not r["differingFields"]),
      "| differing:", [(r["id"], r["differingFields"]) for r in res if r["differingFields"]][:40])
