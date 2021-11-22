
. ../Lifting-dataset/env.sh

#collection=postesSynop
#mongoimport --type=json -d $DB -c ${collection} postesSynop.json

collection=$1
if [[ -z "$collection" ]] ; then help; fi

dirpath=$2
if [[ -z "$dirpath" ]] ; then help; fi
 

python uploadMongoDB.py $collection $dirpath

