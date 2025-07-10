import requests
from xml.etree import ElementTree as ET

def fetch_pubmed_ids(query: str) -> list:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": 20, "retmode": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_paper_details(pmid: str) -> dict:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pmid, "retmode": "xml"}
    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)

    article = root.find(".//PubmedArticle")
    title = article.findtext(".//ArticleTitle", default="No title")
    pub_date = article.findtext(".//PubDate/Year", default="Unknown")
    affiliations = article.findall(".//AffiliationInfo")

    non_academic = []
    companies = []
    emails = []

    for aff in affiliations:
        aff_text = aff.findtext("Affiliation", default="")
        if any(word in aff_text.lower() for word in ["university", "college", "institute", "school", "center"]):
            non_academic.append(aff_text)
        if any(word in aff_text.lower() for word in ["pharma", "biotech", "therapeutics", "inc", "corp", "ltd"]):
            companies.append(aff_text)
        if "@" in aff_text:
            possible_email = [word for word in aff_text.split() if "@" in word]
            emails.extend(possible_email)

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": "; ".join(non_academic),
        "Company Affiliation(s)": "; ".join(companies),
        "Corresponding Author Email": "; ".join(emails),
    }