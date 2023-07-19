 #!/bin/bash


. ./ENV.sh



./download.sh

. ./last_update.sh

NEWDATE=$LASTupdateY$LASTupdateM

output=observation${NEWDATE}.ttl

./run_pipeline.sh obs$NEWDATE $MAPPING_OBS $output

mv ${DATASET_DIR}$output ${BACKUP_DIR}$output


rm ${DIR}csv/*

rm ${DIR}json/*

python SliceGenerator.py $LASTupdateY $LASTupdateM

outputSlice=slice${NEWDATE}.ttl

./run_pipeline.sh obs$NEWDATE $MAPPING_SLICES $outputSlice

mv ${DATASET_DIR}$outputSlice ${BACKUP_DIR}$outputSlice

rm ${DIR}csv/*

rm ${DIR}json/*