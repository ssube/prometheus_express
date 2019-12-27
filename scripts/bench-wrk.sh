wrk -c 1 -t 1 -d 60s \
  --timeout 1s \
  --script <(echo <<<EOF
function delay()
 return math.random(10, 20)
end
EOF
  ) \
  http://${EXPRESS_HOST}:8080/metrics