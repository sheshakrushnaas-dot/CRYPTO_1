from pathlib import Path
def test_v2():
    r=Path(__file__).parents[1]
    assert (r/'backend/api/app.py').exists()
    assert (r/'backend/ingestion/upload_pipeline.py').exists()
    assert (r/'frontend/index.html').exists()
    assert (r/'data/results/v1_results.json').exists()
