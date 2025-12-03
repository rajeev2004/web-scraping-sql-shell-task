This project contains three components showcasing Python scripting, API data extraction, SQL querying, and shell scripting.

1. OLX Scraper (Python)

Uses OLX’s public JSON API:

https://www.olx.in/api/relevance/v4/search


Extracts:

Title

Price

Description

Item Link

Run
pip install -r requirements.txt
python olx_scraper.py "car cover" --limit 20


Sample output stored in:
examples/olx_output.txt

2. Rfam SQL Queries

Queries included in rfam_queries.sql:

Count tiger species + find Sumatran Tiger ncbi_id

Identify joinable columns across tables

Find rice species with longest DNA sequence

Pagination query (9th page, 15 results/page)

Run
mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro -D Rfam
SOURCE rfam_queries.sql;

3. AMFI NAV Extractor (Shell Script)

Extracts:

Scheme Name

Net Asset Value (NAV)

▶ Run
chmod +x amfi_extract.sh
./amfi_extract.sh examples/amfi_sample.tsv


Output saved in:
examples/amfi_sample.tsv