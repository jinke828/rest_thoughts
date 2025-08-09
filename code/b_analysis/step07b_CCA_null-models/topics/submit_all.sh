#!/bin/bash

for val in {1..40}
do
    sbatch --output=logs/outISC_${val}.txt run_topics_null.sh $val
done