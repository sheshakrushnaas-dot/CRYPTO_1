from pathlib import Path
import json, xml.etree.ElementTree as ET
import pandas as pd
SUPPORTED={".csv",".json",".xml"}
def detect_format(path):
    s=Path(path).suffix.lower()
    if s not in SUPPORTED: raise ValueError(f"Unsupported format: {s}")
    return s[1:]
def iter_csv(path,chunksize=100_000):
    yield from pd.read_csv(path,chunksize=chunksize,low_memory=False)
def iter_json(path,chunksize=100_000):
    with open(path,encoding="utf-8") as f:
        first=f.read(1); f.seek(0)
        if first=="[":
            data=json.load(f)
            for i in range(0,len(data),chunksize): yield pd.DataFrame(data[i:i+chunksize])
        else:
            batch=[]
            for line in f:
                if line.strip(): batch.append(json.loads(line))
                if len(batch)>=chunksize: yield pd.DataFrame(batch); batch=[]
            if batch: yield pd.DataFrame(batch)
def iter_xml(path,record_tag="record",chunksize=100_000):
    batch=[]
    for _,elem in ET.iterparse(path,events=("end",)):
        if elem.tag==record_tag:
            batch.append({c.tag:c.text for c in elem}); elem.clear()
            if len(batch)>=chunksize: yield pd.DataFrame(batch); batch=[]
    if batch: yield pd.DataFrame(batch)
def iter_records(path,chunksize=100_000,xml_record_tag="record"):
    fmt=detect_format(path)
    if fmt=="csv": yield from iter_csv(path,chunksize)
    elif fmt=="json": yield from iter_json(path,chunksize)
    else: yield from iter_xml(path,xml_record_tag,chunksize)
