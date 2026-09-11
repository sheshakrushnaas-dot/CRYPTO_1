
from pathlib import Path
import pandas as pd, json, xml.etree.ElementTree as ET

ALIASES={
"txid":{"txid","tx_id","transaction_id","transaction"},
"timestamp":{"timestamp","time","datetime","date"},
"src_ip":{"src_ip","source_ip","srcip"},"dst_ip":{"dst_ip","destination_ip","dstip"},
"src_port":{"src_port","source_port","srcport"},"dst_port":{"dst_port","destination_port","dstport"},
"input_addresses":{"input_addresses","inputs","input_address"},
"output_addresses":{"output_addresses","outputs","output_address"},
"input_amounts":{"input_amounts","input_amount"},"output_amounts":{"output_amounts","output_amount"},
"fee":{"fee","transaction_fee"},"script_type":{"script_type","script"},
"geo_country":{"geo_country","country","country_code"},"asn":{"asn","autonomous_system","autonomous_system_number"}}

def map_schema(columns):
    norm={str(c).strip().lower().replace(" ","_"):c for c in columns}
    return {k:next((norm[a] for a in v if a in norm),None) for k,v in ALIASES.items()}

def inspect_csv(path, chunk=100_000):
    rows=0; cols=[]
    for df in pd.read_csv(path,chunksize=chunk,low_memory=False):
        rows += len(df)
        if not cols: cols=list(df.columns)
    return rows, map_schema(cols)

def inspect_json(path):
    with open(path,encoding="utf-8") as f:
        first=f.read(1); f.seek(0)
        if first=="[":
            d=json.load(f); cols=list(d[0]) if d else []; return len(d),map_schema(cols)
        rows=0; cols=[]
        for line in f:
            if line.strip():
                o=json.loads(line); rows+=1
                if not cols: cols=list(o)
        return rows,map_schema(cols)

def inspect_xml(path, record_tag="record"):
    rows=0; cols=set()
    for _,e in ET.iterparse(path,events=("end",)):
        if e.tag==record_tag:
            rows+=1; cols.update(c.tag for c in e); e.clear()
    return rows,map_schema(cols)
