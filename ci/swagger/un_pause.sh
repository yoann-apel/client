curl -X 'POST' \
  'http://lhd-dev-gpao.ign.fr:8080/api/jobs/setTags?tags=docker' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "ids": [
    84114
  ]
}'