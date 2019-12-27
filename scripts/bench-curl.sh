ITER_LIMIT="${1:-10000}"
ITER_COUNT=0
ITER_ERROR=0

while [[ ${ITER_COUNT} -lt ${ITER_LIMIT} ]];
do
  CURL_RESULT="$(curl -s http://${EXPRESS_HOST}:8080/metrics)"
  CURL_STATUS="${?}"

  if [[ ${CURL_STATUS} != 0 ]];
  then
    echo "Error during curl (${ITER_ERROR}):"
    echo "${CURL_RESULT}"

    ITER_ERROR=$((ITER_ERROR + 1))
    if [[ ${ITER_ERROR} -gt 3 ]];
    then
      exit 1
    fi
  fi

  ITER_COUNT=$((ITER_COUNT + 1))
  ITER_ERROR=$((ITER_ERROR - 1))

  if [[ $((ITER_COUNT % 100)) -eq 0 ]];
  then
    echo "Request: ${ITER_COUNT} of ${ITER_LIMIT}"
  fi
done