
. ../Lifting-dataset/env.sh

#collection=postesSynop
#mongoimport --type=json -d $DB -c ${collection} postesSynop.json

cd virtuoso
graph="http://ns.meteo.inria.fr/graph/weather2019"
. ./virtuoso-import.sh  --cleargraph --graph $graph --path ./xr2rml/observations2019.ttl

