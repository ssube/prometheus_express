wrk -c 1 -t 1 -d 60s \
  http://${EXPRESS_HOST}:8080/metrics \
  --timeout 1s \
  --script <(cat << EOF
function delay()
 return math.random(10, 20)
end
EOF
)
