#!/bin/bash

##############################
#hdfs namenode -format
#hdfs dfs -rm -r /cloud

echo "******************** Descargar dataset ********************"

python3 fetch_pages.py

echo "******************** Creando folders y subiendo los archivos ********************"
hdfs dfs -mkdir /invertedIndex/
hdfs dfs -mkdir /invertedIndex/inputDocuments
hdfs dfs -mkdir /invertedIndex/outputInvertedIndex

hdfs dfs -put data/* /invertedIndex/inputDocuments

echo "******************** ejecutar jar con indice invertido ********************"
#Cambiar ruta de jar segun corresponda

hadoop jar '/home/efra/Documentos/github/implemntations/JAR_Files/inverted-index.jar' invertedindex.InvertedIndex

echo "******************** Descargar archivo de salida ********************"
hdfs dfs -get /invertedIndex/outputInvertedIndex/part-r-00000



