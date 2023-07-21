#!/bin/bash
#
# WARNING - Run the commands below from directory 'virtuoso'

# Environment variables
#. ../env.sh


# Directory where the ttl files are stored

graph="http://ns.inria.fr/meteo/ontology"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /ontology \
    weatherdataset-model.ttl
    
graph="http://ns.inria.fr/meteo/vocab"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /ontology \
    features-properties-vocabulaire.ttl WMO-thesaurus.ttl

graph="http://ns.inria.fr/meteo/weatherstation"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    meteofrance-station.ttl dump-wikidata3.ttl    

graph="http://ns.inria.fr/meteo/observation/2021"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    weather2021.ttl obsDec-2021.ttl

graph="http://ns.inria.fr/meteo/observation/2020"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    weather2020.ttl


graph="http://ns.inria.fr/meteo/observation/2019"
/database/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    weather2019.ttl

