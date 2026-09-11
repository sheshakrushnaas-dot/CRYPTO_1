# CRYPTO.SHIELD — FINAL PROTOTYPE
Problem Statement 26146 • Offline Linux • Blockchain & Cybersecurity

## What this final package contains
1. Scalable CSV/JSON/XML ingestion.
2. Dataset upload endpoint with asynchronous inspection.
3. NTRO-oriented schema mapping and coverage reporting.
4. Blockchain transaction/address graph features.
5. Supervised illicit-vs-licit ML baseline when labels are available.
6. Isolation Forest anomaly detection.
7. Combined explainable investigation risk score.
8. Ranked investigative leads with evidence reasons.
9. Interactive intelligence dashboard with Command Center, Upload,
   Investigation, Transactions, Entities, Network, 3D Graph, AI,
   Alerts, Analytics and Methodology sections.
10. REST endpoints for health, results, leads, upload and upload status.
11. Tests, configuration and documentation.

## Run locally on Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 backend/api/app.py
```
Then open:
http://127.0.0.1:8000

## Demo dataset
The bundled development results were generated from the three supplied files:
- txs_classes.csv
- txs_edgelist.csv
- TxAddr_edgelist.csv

The source files are intentionally not copied into this package, so the
application remains lightweight. The generated results are included.

## Important data truthfulness rule
The current supplied files do NOT provide network IP/port/timing, transaction
amounts/fees, script type, country or ASN. The UI marks those fields as
unavailable. The final architecture accepts them when a future uploaded
dataset contains them. It never invents missing evidence.

## Large-data behavior
CSV ingestion uses pandas chunking (default 100,000 rows). JSONL is processed
incrementally and XML uses iterparse. For very large deployments, the same
interfaces can be connected to a columnar local store without changing the
frontend/API contract.

## Demo ML result
Known class 1 (illicit) vs class 2 (licit), with class 3 excluded:
- ROC-AUC: 0.8707
- Average Precision: 0.5358
- Illicit precision: 0.6129
- Illicit recall: 0.6259
- Illicit F1: 0.6193

These are dataset-benchmark results, not real-world attribution.


## Synthetic Demo Mode
The final package includes an optional synthetic enrichment layer for demonstrations.
It can generate missing timestamp, IP/port, country/ASN, amount/fee, script type and
synthetic address fields. Generated values are marked as synthetic and are never
presented as real network observations or financial evidence. Real user-supplied fields
always take precedence.
