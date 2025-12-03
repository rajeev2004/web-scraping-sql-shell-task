-- 2a. Count tiger types
SELECT COUNT(DISTINCT scientific_name) AS tiger_types
FROM taxonomy
WHERE scientific_name LIKE '%tigris%';

-- Find the ncbi_id for Sumatran Tiger
SELECT ncbi_id, scientific_name
FROM taxonomy
WHERE scientific_name LIKE '%Panthera tigris%' AND scientific_name LIKE '%sumatr%';

-------------------------------------------------

-- 2b. Columns that connect tables (shared column names)
SELECT column_name,
       COUNT(*) AS occurrences,
       GROUP_CONCAT(table_name) AS tables
FROM information_schema.columns
WHERE table_schema = 'Rfam'
GROUP BY column_name
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

-------------------------------------------------

-- 2c. Rice with longest DNA sequence
SELECT t.scientific_name,
       r.accession,
       r.length
FROM rfamseq r
JOIN taxonomy t ON r.ncbi_id = t.ncbi_id
WHERE t.scientific_name LIKE 'Oryza%'
ORDER BY r.length DESC
LIMIT 1;

-------------------------------------------------

-- 2d. Pagination — families where max DNA length > 1,000,000
-- 9th page, 15 results per page → OFFSET = (9-1)*15 = 120
SELECT f.rfam_acc,
       f.rfam_id,
       MAX(s.length) AS max_length
FROM family f
JOIN full_region fr ON f.rfam_id = fr.rfam_id
JOIN rfamseq s ON fr.seq_acc = s.accession
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(s.length) > 1000000
ORDER BY max_length DESC
LIMIT 15 OFFSET 120;
