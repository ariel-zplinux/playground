SELECT A.cid,A.name
FROM customers A
    LEFT JOIN invoices B ON A.cid = B.cid
WHERE B.cid IS NULL