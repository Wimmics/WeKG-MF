### Meteo-France Weather Dataset

The Meteo-France Weather dataset is an RDF dataset that provides access to meteorological measurments provided by 62 weather stations located in different regions in metropolitan France and overseas departments. 
The dataset incorporates measurements of several weather parameters such as wind direction and speed, air pressure, precipitations, humidity and temperature. 
In total, observations  

The weather dataset namespace is ```http://ns.inria.fr/meteo/```. 

## RDF data modelling 

Based on a network of existing ontologies (SOSA/SSN, GeoSPARQL, Time Ontology), we define a minimal self-contained semantic model for meteorological data. 
Thus, we extend the SOSA observation, feature of interest and observable property classes and we provide an formal OWL definition of the new classes. 

We define also a SKOS vocabulary of weather observable properties and features of interest commonly used in weather reports.  

The semantic model and SKOS vocabulary are provided in the ```weather-dataset-metadata``` directory. 

The model and vocabulary are intended to be adopted and extended by any meteorological data provider. 

## Pipeline generation 

The pipeline generation of the Meteo-France weather RDF dataset involves several steps including the preprocessing and loading data in MongoDB database as JSON collections.
Then, the step of translation is carried out using Morph-xr2RML tool, an implementation of the xR2RML mapping language for MongoDB databases. 

Note that all the pipeline generation can be automatically executed with ```run_pipeline.sh``` script available in ```Lifting-dataset``` directory.

The script ```run_pipeline.sh``` needs 4 arguments: 
 
* JSON collection (if a collection with the same name already exist in MongoDB, it will be dropped and created again with the new data),

* Path directory to the csv files, e.g., raw-weather-data/yyyy/csv

* Mapping file : e.g., mapping_observation_tpl.ttl

* Output file name (e.g, ```rdf-dataset-yyyy.ttl```)

Example : 

./run_pipeline.sh collection022021 raw-weather-data/2021/csv mapping_observation_tpl.ttl rdf-dataset-02-2021.ttl

RDF data files generated can be loaded in Virtuoso as separate named graphs. Scripts are provided in directory ```virtuoso```.

## Downloading and SPARQL querying 

The dataset is downloadable as a set of RDF dumps (in Turtle syntax) from Zenodo : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5593216.svg)](https://doi.org/10.5281/zenodo.5593216)

| Named Graph  | No. of RDF triples |
| ------------- | ------------- |
| http://ns.inria.fr/meteo/ontology  | 193  |
| http://ns.inria.fr/meteo/vocab | 346 |
| http://ns.inria.fr/meteo/weatherstation | 794 |
| http://ns.inria.fr/meteo/observation/2021 |  |
| http://ns.inria.fr/meteo/observation/2020 |  |
| http://ns.inria.fr/meteo/observation/2019 |  |
