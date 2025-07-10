from get_papers.pubmed import fetch_pubmed_ids, fetch_paper_details

def test_pubmed_id_fetching():
    ids = fetch_pubmed_ids("covid AND vaccine")
    assert isinstance(ids, list)
    assert len(ids) > 0

def test_pubmed_detail_fetching():
    ids = fetch_pubmed_ids("covid AND vaccine")
    details = fetch_paper_details(ids[0])
    assert "Title" in details
    assert "PubmedID" in details