#!/bin/bash

# Check for job IDs file argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <job_ids_file>"
    exit 1
fi

# Reading the file containing job IDs
JOB_IDS_FILE="$1"

# Check if the file exists
if [ ! -f "$JOB_IDS_FILE" ]; then
    echo "Error: Job IDs file does not exist - $JOB_IDS_FILE"
    exit 1
fi

# Convert job IDs from file to SLURM's format
JOB_IDS=$(cat "$JOB_IDS_FILE" | tr '\n' ' ' | sed 's/ $//' | tr ' ' ':' | sed 's/:$//')
echo "Job IDs: $JOB_IDS"

# Script content to check job statuses
check_script="for ID in \$(echo \$SLURM_JOB_DEPENDENCY | sed 's/.*afterany://; s/:/ /g'); do \
    STATE=\$(sacct -j \$ID --format=State --noheader | head -n 1 | tr -d ' '); \
    echo \"Job \$ID ended with state \$STATE\"; \
    if [[ \$STATE != COMPLETED ]]; then \
        echo \"Warning: Job \$ID did not complete successfully.\"; \
    fi; \
done"

# Submit a barrier job that checks the completion status of other jobs
if [ -n "$JOB_IDS" ]; then
    set -x
    BARRIER_JOB_ID=$(sbatch --dependency=afterany:$JOB_IDS --time=2:00 --wrap="$check_script" | cut -d ' ' -f 4)
    { set +x; } 2>/dev/null
    echo "Barrier job submitted with ID: $BARRIER_JOB_ID"
else
    echo "No job IDs provided. Exiting."
    exit 1
fi