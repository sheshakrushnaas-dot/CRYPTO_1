
"""Explainable risk scoring for CRYPTO.SHIELD.
All explanations must be grounded in fields/features actually present in the dataset.
Missing fields are reported as unavailable; synthetic fields remain explicitly synthetic.
"""
def explain_transaction(features: dict):
    reasons=[]
    def add(name, evidence, source, weight):
        reasons.append({"reason":name,"evidence":evidence,"source":source,"weight":weight})

    fanout=features.get("output_count")
    if isinstance(fanout,(int,float)) and fanout>=10:
        add("High fan-out","Transaction has %d outputs."%fanout,"graph feature",0.24)

    reuse=features.get("address_reuse_count")
    if isinstance(reuse,(int,float)) and reuse>=1:
        add("Address reuse","%d input/output address relationship(s) are reused."%reuse,"graph feature",0.20)

    burst=features.get("burst_count")
    if isinstance(burst,(int,float)) and burst>=5:
        add("Burst timing","%d related transactions occur in a short time window."%burst,"temporal feature",0.18)

    fee_ratio=features.get("fee_ratio")
    if isinstance(fee_ratio,(int,float)) and fee_ratio>=0.05:
        add("Unusually high fee","Fee is %.2f%% of input value."%(fee_ratio*100),"financial feature",0.14)

    value=features.get("total_value")
    if isinstance(value,(int,float)) and value>=100:
        add("High transaction value","Synthetic/observed transaction value is %.4f BTC."%value,"amount feature",0.12)

    script=features.get("script_type")
    if script and str(script).lower() in {"p2sh-unusual","unusual"}:
        add("Unusual script type","Script type is %s."%script,"script feature",0.10)

    cluster=features.get("cluster_size")
    if isinstance(cluster,(int,float)) and cluster>=5:
        add("Coordinated cluster","Entity belongs to a connected cluster of %d+ nodes."%cluster,"graph feature",0.18)

    layering=features.get("layering_hops")
    if isinstance(layering,(int,float)) and layering>=2:
        add("Layering-chain pattern","Observed graph path contains %d sequential hops."%layering,"graph feature",0.18)

    net=features.get("network_anomaly")
    if net:
        add("Network anomaly",str(net),"network feature",0.15)

    model=features.get("model_anomaly")
    if isinstance(model,(int,float)) and model>0.7:
        add("ML anomaly score","Unsupervised anomaly score is %.2f."%model,"ML model",0.20)

    reasons.sort(key=lambda x:x["weight"],reverse=True)
    return {
        "reasons":reasons[:5],
        "why_flagged": "Flagged because " + "; ".join(r["reason"].lower() for r in reasons[:3]) + "." if reasons else
                       "No supported risk evidence was available for this transaction.",
        "evidence_count":len(reasons),
        "caveat":"Risk score is an investigative lead, not proof of illicit activity."
    }
