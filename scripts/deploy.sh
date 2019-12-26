DEVICE_PATH="${1}"
DEVICE_LIB="${DEVICE_PATH}/lib"

LIBRARY_PATH="${2}"

PROGRAM_FILE="${3}"

mkdir "${DEVICE_LIB}"
rsync -avh "${LIBRARY_PATH}/neopixel.mpy" "${DEVICE_LIB}"
rsync -avh --exclude-from="scripts/deploy-exclude" "./prometheus_express" "${DEVICE_PATH}"
cp -v "./examples/${PROGRAM_FILE}.py" "${DEVICE_PATH}/code.py"
