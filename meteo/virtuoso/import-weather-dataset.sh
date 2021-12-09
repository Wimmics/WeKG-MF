#!/bin/bash
#
# WARNING - Run the commands below from directory 'virtuoso'

# Environment variables
#. ../env.sh


# Directory where the ttl files are stored

../ 

graph="http://ns.inria.fr/meteo/ontology"
/data/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /metadata \
    weatherdataset-model.ttl
    
graph="http://ns.inria.fr/meteo/vocab"
/data/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /metadata \
    features-properties-vocabulaire.ttl WMO-thesaurus.ttl

graph="http://ns.inria.fr/meteo/weatherstation/"
/data/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    meteofrance-stations.ttl

graph="http://ns.inria.fr/meteo/observation/"
/data/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /dataset \
    weather2021.ttl

