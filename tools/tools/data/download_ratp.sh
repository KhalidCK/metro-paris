#!/bin/bash
output='data/raw'
mkdir -p $output
echo 'Download data from ratp website'
wget -O $output/ratp-trafic-2016.json 'https://data.ratp.fr/explore/dataset/trafic-annuel-entrant-par-station-du-reseau-ferre-2016/download/?format=json&refine.reseau=M%C3%A9tro&timezone=Europe/Berlin'
