
. ../Lifting-dataset/env.sh

#collection=postesSynop
#mongoimport --type=json -d $DB -c ${collection} postesSynop.json


log "Importing graph in Virtuoso..."; echo
graph="http://ns.meteo.inria.fr/graph/weather2019"
. $PROJECT/src/virtuoso/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path /xr2rml \
   observations2019.ttl