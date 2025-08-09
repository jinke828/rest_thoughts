#!/bin/bash

for val in {1..200}
do
    sbatch --output=logs/outISC_${val}.txt run_null.sh $val
done