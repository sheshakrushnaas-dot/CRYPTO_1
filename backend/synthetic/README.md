# Synthetic Demo Enrichment

This module generates deterministic, clearly synthetic values for fields absent
from the supplied development data. It never overwrites a field supplied by a
user dataset.

Synthetic fields include timestamp, IPs, ports, country, ASN, amounts, fee,
script type and a synthetic input address.

All generated records carry:
- `synthetic: true`
- `synthetic_source: NTRO-26146 demo enrichment`
- `_synthetic_fields`

These values are for UI/model demonstration only and are not evidence.
