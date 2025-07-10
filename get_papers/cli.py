import argparse
import csv
from get_papers.pubmed import fetch_pubmed_ids, fetch_paper_details

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma affiliations.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-f", "--file", help="CSV output filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Searching PubMed with query: {args.query}")

    pmids = fetch_pubmed_ids(args.query)

    if args.debug:
        print(f"[DEBUG] Found {len(pmids)} papers")

    results = [fetch_paper_details(pmid) for pmid in pmids]

    if args.file:
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Results saved to {args.file}")
    else:
        for row in results:
            print(row)