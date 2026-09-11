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
def coverage(columns):
    norm={str(c).strip().lower().replace(" ","_"):c for c in columns}
    return {k:next((norm[a] for a in aliases if a in norm),None) for k,aliases in ALIASES.items()}
def validate(columns):
    c=coverage(columns); return {"coverage_percent":round(100*sum(v is not None for v in c.values())/len(c),2),
                                 "fields":{k:{"available":v is not None,"source_column":v} for k,v in c.items()}}
