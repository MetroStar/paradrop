#!/bin/sh

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a'  -H 'Content-Type: application/json' -XPOST 'https://127.0.0.1:9200/paradrop_hosts/_delete_by_query?conflicts=proceed' -d '{"query":{"match_all": {}}}'
