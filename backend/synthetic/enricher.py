
"""Synthetic demo enrichment.
IMPORTANT: generated values are simulation only and must never be treated as real observations."""
from __future__ import annotations
import hashlib
from datetime import datetime, timedelta

COUNTRIES=["IN","US","DE","NL","SG","GB","CA","FR","JP","AU"]
SCRIPTS=["P2PKH","P2SH","P2WPKH","P2WSH","P2TR"]

def _u(seed, salt):
    return int(hashlib.sha256(f"{seed}:{salt}".encode()).hexdigest()[:12],16)

def synthetic_for_tx(txid, index=0):
    seed=str(txid)
    a=_u(seed,"a")
    b=_u(seed,"b")
    ts=datetime(2024,1,1)+timedelta(seconds=a%(366*24*3600))
    src=f"10.{(a>>8)%256}.{(a>>16)%256}.{max(1,(a>>24)%254)}"
    dst=f"10.{(b>>8)%256}.{(b>>16)%256}.{max(1,(b>>24)%254)}"
    in_amount=round(0.001+(a%500000000)/1e8,8)
    fee=round(0.000001+(b%500000)/1e8,8)
    out_amount=max(0.00000001,round(in_amount-fee,8))
    return {
      "timestamp":ts.isoformat()+"Z",
      "src_ip":src,"dst_ip":dst,
      "src_port":8333 if a%3 else 18333,
      "dst_port":8333,
      "geo_country":COUNTRIES[a%len(COUNTRIES)],
      "asn":f"AS{1000+(b%64500)}",
      "input_addresses":[f"syn-in-{hashlib.sha256((seed+'in').encode()).hexdigest()[:16]}"],
      "input_amounts":[in_amount],
      "output_amounts":[out_amount],
      "fee":fee,
      "script_type":SCRIPTS[b%len(SCRIPTS)],
      "synthetic":True,
      "synthetic_source":"NTRO-26146 demo enrichment",
      "synthetic_seed":hashlib.sha256(seed.encode()).hexdigest()[:12]
    }

def enrich(txid, row=None):
    """Return only missing fields; never overwrite supplied real fields."""
    row=dict(row or {})
    syn=synthetic_for_tx(txid)
    generated=[]
    for k,v in syn.items():
        if k in {"synthetic","synthetic_source","synthetic_seed"}:
            continue
        if k not in row or row[k] in (None,"","[]","{}"):
            row[k]=v; generated.append(k)
    row["_synthetic_fields"]=generated
    row["_has_synthetic_enrichment"]=bool(generated)
    return row
