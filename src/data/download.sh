#!/bin/bash
echo 'Downloading data ...'
output='data/raw'
mkdir -p $output
base_url='https://opendata.stif.info/explore/dataset'
profil_validation1='/validations-sur-le-reseau-ferre-profils-horaires-par-jour-type-1er-sem/'
profil_validation2='/validations-sur-le-reseau-ferre-profils-horaires-par-jour-type-2e-sem/'
profil_nb1='/validations-sur-le-reseau-ferre-nombre-de-validations-par-jour-1er-sem/'
profil_nb2='/validations-sur-le-reseau-ferre-nombre-de-validations-par-jour-2e-sem/'
lignes='/liste-arrets-lignes-tc-idf/download/?format=json&refine.agency_name=METRO&timezone=Europe/Berlin'
schedule='/offre-horaires-tc-gtfs-idf/files/f24cf9dbf6f80c28b8edfdd99ea16aad/download/'
calendrier="https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"
#download only data regarding metro network (res = 110)
option='download/?format=json&refine.code_stif_res=110&timezone=Europe/Berlin'
wget -O "$output"/nb-validation_S1-2017.json "$base_url""$profil_nb1""$option" -
wget -O "$output"/nb-validation_S2-2017.json "$base_url""$profil_nb2""$option" -
wget -O "$output"/profil-validation_S1-2017.json "$base_url""$profil_validation1""$option" 
wget -O "$output"/profil-validation_S2-2017.json "$base_url""$profil_validation2""$option"
wget -O "$output"/lignes.json "$base_url""$lignes"
wget -O "$output"/gtfs.zip "$base_url""$schedule"
unzip "$output"/gtfs.zip -d $output
wget  -O "$output""/vacances.csv" "$calendrier"
