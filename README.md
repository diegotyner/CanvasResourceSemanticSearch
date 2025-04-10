

<br>

# Quick Summary

An end-to-end data pipeline that scrapes Canvas files and lecture transcripts, processes them, and enables semantic search using sentence embeddings.

Uses: 
- Scraping Tools: Selenium, Requests, Concurrency 
- Embeddings: Transformers, Pytorch, PostgreSQL
- (hopefully) Web App: Nextjs, Tailwind, Transformers.js 

<br>

# Pipeline Order

1. Canvas Scraper  
    - Uses Auth cookies and requests to scrape all Canvas files, and then uses Selenium to load the lecture hosting site and access transcripts
   - The lecture scraper runs slowly, takes me 30-40 minutes to run but a more powerful PC or more optimized code can definitely speed it up. 
2. Course Downloading 
    - Turns the scraped download URLs into local files.
3. Text Extractor
    - Wrangles resources into raw text files. A lot of work can be done here (Tesseract OCR, better chunking, etc.)
4. Embeddings Generation
    - Generates embeddings for text files. So far, I've only experimented with lectures, I will experiment with PDFs soon.

TODOs:

1. Data Exploration
    - Look into fun ways to cluster and visualize lectures
    - Cluster similar classes, similar lectures, semantic variation within lectures. etc 
2. UI and UX
    - Turn into a functional web app, pushing embeddings to Postgres and allowing easy semantic search
    - Think about useful interfaces
      - Find similar passages in lectures and suggest lecture slides afterwards?
      - Allow filtering for specific topics within classes (EG find where dynamic programming was introduced in an Algorithms class or a specific lecture)
    - More!
