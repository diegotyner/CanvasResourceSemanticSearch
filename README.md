

# Quick Summary

An end-to-end data pipeline that scrapes Canvas files and lecture transcripts, processes them, and enables semantic search using sentence embeddings.

Uses: Selenium, Requests, Concurrency, transformers, torch, sklearn

# Pipeline Order

1. Canvas Scraper 
  - Uses Auth cookies and requests to scrape all Canvas files, and then uses Selenium to load the lecture hosting site and access transcripts
  - The lecture scraper runs slowly, takes me 30-40 minutes to run but a more powerful PC or more optimized code can definitely speed it up. 
2. Course Downloading 
- Turns the scraped download URLs into local files.
3. Text-Extractor
- Wrangles resources into raw text files. A lot of work can be done here (Tesseract OCR, better chunking, etc.)
4. Embeddings 
- Generates 
5. ?
- Turn into a functional web app, pushing embeddings to Postgres and allowing easy semantic search