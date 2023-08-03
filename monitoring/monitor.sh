#!/bin/bash

while true
do
    BASE_URL="http://localhost:5000/api"
    DISPENSERS=$(curl -s "${BASE_URL}/dispenser")

    clear

    heading="Dispenser Monitoring"
    terminal_width=$(tput cols)

    heading_center=$(( (terminal_width - ${#heading}) / 2 ))

    printf "%*s\n" $heading_center "$heading"
    echo "=============================================================================================="

    DISPENSER_COUNT=$(echo "${DISPENSERS}" | jq length)
    COLUMNS=1

    for ((i = 0; i < DISPENSER_COUNT; i += COLUMNS))
    do
        for ((j = 0; j < COLUMNS && (i + j) < DISPENSER_COUNT; j++))
        do
            INDEX=$((i + j))
            DISPENSER=$(echo "${DISPENSERS}" | jq -r ".[${INDEX}]")

            id=$(echo "${DISPENSER}" | jq -r '.id')
            flow_volume=$(echo "${DISPENSER}" | jq -r '.flow_volume')
            price=$(echo "${DISPENSER}" | jq -r '.price')
            is_open=$(echo "${DISPENSER}" | jq -r '.is_open')

            printf "Dispenser ID: %-8s | Flow Volume: %-8sL/s | Price: \$%-6s | Status: %s\n" "${id}" "${flow_volume}" "${price}" "$(if [ "$is_open" = "true" ]; then echo "Open"; else echo "Closed"; fi)"
        done
        echo "----------------------------------------------------------------------------------------------"
    done

    sleep 5
done