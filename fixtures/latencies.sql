-- Get the latency table from the database. 
SELECT s.hostname as src_hostname, s.location as src_location, s.latitude as src_latitude, s.longitude as src_longitude, 
       d.hostname as dst_hostname, d.location as dst_location, d.latitude as dst_latitude, d.longitude as dst_longitude,
       l.messages, l.timeouts, l.mean, l.stddev, l.fastest, l.slowest 
FROM latencies l 
    JOIN machines s on l.source_id = s.id 
    JOIN machines d on l.target_id = d.id 
WHERE s.active = 't' AND d.active = 't'
