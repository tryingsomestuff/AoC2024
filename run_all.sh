#!/bin/bash
mkdir -p logs
for i in `seq -w 1 25`; do
    echo "Puzzle $i"
    start_time=$(date +%s.%N)
    if [ -e "${i}_2.py" ]; then
        echo "Solving Part 1"
        python ${i}.py > logs/${i}.log
        echo "------------------"
        echo "Solving Part 2"
        python ${i}_2.py  > logs/${i}_2.log
    else
        echo "Solving"
        python ${i}.py > logs/${i}.log
    fi
    end_time=$(date +%s.%N)
    elapsed=$(echo "$end_time - $start_time" | bc)
    echo "Elapsed : $elapsed sec"
    echo "##############################"
done