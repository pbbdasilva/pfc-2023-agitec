#!/bin/bash
PFC_DIR=/home/utilizador/pfc-2023-agitec
$PFC_DIR/run-dotnet.sh

# fetch and filter candidates step
cd $PFC_DIR/candidates
source $PFC_DIR/venv/bin/activate
python3 fetch_candidates.py --month 01 --year 2023
python3 fetch_ids.py

# store candidates step
cd $PFC_DIR/lattes-core
python3 store_cvs.py

cd $PFC_DIR/nce
python3 parse_nces.py
python3 store_nces.py

cd $PFC_DIR/scores
python3 main.py
