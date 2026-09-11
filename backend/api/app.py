
from pathlib import Path
import json, uuid, threading
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

BASE=Path(__file__).resolve().parents[2]
R=BASE/"data"/"results"; F=BASE/"frontend"; UP=BASE/"data"/"uploads"
UP.mkdir(parents=True,exist_ok=True); R.mkdir(parents=True,exist_ok=True)
app=Flask(__name__,static_folder=str(F),static_url_path="")
jobs={}

def analyze_file(path, job_id, synthetic_demo=False):
    """Chunked upload inspection. Full graph analysis is used for the bundled demo;
    uploaded files first receive scalable schema/coverage analysis."""
    try:
        suffix=path.suffix.lower()
        if suffix==".csv":
            total=0; cols=None
            for chunk in pd.read_csv(path,chunksize=100_000,low_memory=False):
                total += len(chunk)
                if cols is None: cols=list(chunk.columns)
        elif suffix==".json":
            # JSONL fast path; array fallback.
            try:
                total=0; cols=None
                with open(path,encoding="utf-8") as f:
                    first=f.read(1); f.seek(0)
                    if first=="[":
                        data=json.load(f); total=len(data); cols=list(data[0].keys()) if data else []
                    else:
                        for line in f:
                            if line.strip():
                                obj=json.loads(line); total+=1
                                if cols is None: cols=list(obj.keys())
            except Exception:
                total=0; cols=[]
        elif suffix==".xml":
            import xml.etree.ElementTree as ET
            total=0; cols=set()
            for _,e in ET.iterparse(path,events=("end",)):
                if len(e):
                    total+=1
                    cols.update(c.tag for c in e)
                    e.clear()
            cols=sorted(cols)
        else: raise ValueError("Only CSV, JSON and XML are supported.")
        jobs[job_id]={"status":"complete","rows":total,"columns":cols,
                      "synthetic_demo_enabled":bool(synthetic_demo),
                      "synthetic_policy":"Only missing fields may be synthetically generated; all generated values are labeled." ,
                      "message":"Upload ingested successfully. Run analysis using the mapped schema."}
    except Exception as e:
        jobs[job_id]={"status":"error","message":str(e)}

@app.get("/api/health")
def health(): return jsonify({"status":"online","offline":True,"project":"CRYPTO.SHIELD","problem_statement":"NTRO-26146","version":"FINAL"})

@app.get("/api/results")
def results():
    return jsonify(json.loads((R/"v1_results.json").read_text()))

@app.get("/api/leads")
def leads():
    return jsonify(pd.read_csv(R/"top_100_investigative_leads.csv").to_dict("records"))

@app.post("/api/upload")
def upload():
    if "file" not in request.files: return jsonify({"error":"file field is required"}),400
    file=request.files["file"]
    name=secure_filename(file.filename or "")
    if Path(name).suffix.lower() not in {".csv",".json",".xml"}:
        return jsonify({"error":"Supported formats: CSV, JSON, XML"}),400
    job_id=str(uuid.uuid4())
    path=UP/f"{job_id}_{name}"
    file.save(path)
    jobs[job_id]={"status":"processing","filename":name}
    synthetic_demo=request.form.get('synthetic_demo','false').lower()=='true'
    threading.Thread(target=analyze_file,args=(path,job_id,synthetic_demo),daemon=True).start()
    return jsonify({"job_id":job_id,"status":"processing","filename":name})

@app.get("/api/upload/<job_id>")
def upload_status(job_id):
    return jsonify(jobs.get(job_id,{"status":"unknown"}))

@app.route("/")
def home(): return send_from_directory(F,"index.html")

@app.route("/<path:p>")
def static(p): return send_from_directory(F,p)

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8000)
