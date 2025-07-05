"""
This tool provides PubMed search functionality using the @tool decorator.
"""

#%%
from Bio import Medline, Entrez
from smolagents import tool

# %%

@tool
def search_pubmed(query: str, max_results: int = 3) -> str:
    """
    Search PubMed for scientific literature on a given topic.
    IMPORTANT : This tool MUST be run before starting to select the best report combination for survival prediction.
    
    This tool queries the NCBI Entrez API (PubMed) for scientific articles related to the search query.
    It returns metadata including PMID, title, authors, journal, publication date, and abstract.
    
    Args:
        query: The search term or phrase to search for in PubMed (e.g., 'cancer immunotherapy')
        max_results: Maximum number of results to return (default: 3, max: 10)
        
    Returns:
        A formatted string containing the search results with article metadata
        
    Example:
        >>> search_pubmed("machine learning in drug discovery")
        "=== PubMed Search Results for: 'machine learning in drug discovery' ===\n..."
    """
    # Limit max_results to prevent excessive API calls
    max_results = min(max_results, 10)
    
    try:
        # Search PubMed
        handle = Entrez.esearch(db="pubmed", sort="relevance", term=query, retmax=max_results)
        record = Entrez.read(handle)
        pmids = record.get("IdList", [])
        handle.close()

        if not pmids:
            return f"No PubMed articles found for '{query}'. Please try a simpler search query."

        # Fetch article details
        fetch_handle = Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="medline", retmode="text")
        records = list(Medline.parse(fetch_handle))
        fetch_handle.close()

        # Format results
        result_str = f"=== PubMed Search Results for: '{query}' ===\n"
        for i, record in enumerate(records, start=1):
            pmid = record.get("PMID", "N/A")
            title = record.get("TI", "No title available")
            abstract = record.get("AB", "No abstract available")
            journal = record.get("JT", "No journal info")
            pub_date = record.get("DP", "No date info")
            authors = record.get("AU", [])
            authors_str = ", ".join(authors[:3]) if authors else "No authors listed"
            
            result_str += (
                f"\n--- Article #{i} ---\n"
                f"PMID: {pmid}\n"
                f"Title: {title}\n"
                f"Authors: {authors_str}\n"
                f"Journal: {journal}\n"
                f"Publication Date: {pub_date}\n"
                f"Abstract: {abstract}\n"
            )
        
        return result_str
        
    except Exception as e:
        return f"Error searching PubMed: {str(e)}. Please try again with a different query."

# %% 
