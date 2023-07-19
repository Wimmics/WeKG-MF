## Transforming weather reports into RDF data is fully automatic. 


1. First, you have to update the variables in ```ÈNV.sh``` and precide where you want to store the csv/json file and the turtle file, the name of your docker container on which virtuoso runs and the name of the file containing the mapping rules for the raw-data of meteo france and the one with the mapping rule for the slices. Note that relative path for the mapping rules start from the folder ```xr2rml```
2. Once the variable updated, simply runs ```update.sh```. It will download the oldest weather report you did'nt add to your graph yet (The date of the last report lifted is stored in ```last_update.sh```), it will convert it into rdf and lift it to your graph. The turtle file generated is store in the ```backup``` folder in ```virtuoso```
