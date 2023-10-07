#!/bin/bash
PFC_DIR=/home/utilizador/pfc-2023-agitec
$PFC_DIR/run-dotnet.sh

source $PFC_DIR/venv/bin/activate

cd $PFC_DIR/candidates/
./run.sh
cd $PFC_DIR/lattes-core/
./run.sh
cd $PFC_DIR/nce/
./run.sh
cd $PFC_DIR/scores/
./run.sh
