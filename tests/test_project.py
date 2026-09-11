from pathlib import Path
def test_core():
    r=Path(__file__).parents[1]
    assert (r/'backend/ingestion/streaming.py').exists()
    assert (r/'backend/ingestion/validator.py').exists()
    assert (r/'data/results/v1_results.json').exists()
    assert (r/'frontend/index.html').exists()
