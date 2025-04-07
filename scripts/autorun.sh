#!/bin/bash

# Define the duration for running the script and the sleep interval
run_duration=$((30 * 60))   # 30 minutes in seconds
sleep_duration=$((60 * 60)) # 1 hour in seconds

# Loop to repeat the process 3 times
for i in {1..10}; do
    echo "Starting iteration $i: Running snapugc_hf.sh for 30 minutes..."
    
    # Start the snapugc_hf.sh script in the background
    ./scripts/snapugc_hf.sh &
    script_pid=$!

    # Allow the script to run for the specified duration
    sleep $run_duration

    # Terminate the snapugc_hf.sh script after 30 minutes
    kill $script_pid
    echo "snapugc_hf.sh terminated after 30 minutes."

    # Sleep for 1 hour before the next iteration, except after the last iteration
    if [ $i -lt 10 ]; then
        echo "Sleeping for 1 hour before the next iteration..."
        sleep $sleep_duration
    fi
done

echo "All iterations completed."
