ITER_LIMIT="${1:-10000}"
ITER_COUNT=0

while [[ ${ITER_COUNT} -lt ${ITER_LIMIT} ]];
do
  curl -s http://${EXPRESS_HOST}:8080/metrics > /dev/null
  if [[ $? != 0 ]];
  then
    echo "Error during curl"
    curl http://${EXPRESS_HOST}:8080/metrics
    exit 1
  fi

  ITER_COUNT=$((ITER_COUNT + 1))

  if [[ $((ITER_COUNT % 100)) -eq 0 ]];
  then
    echo "Request: ${ITER_COUNT} of ${ITER_LIMIT}"
  fi
done