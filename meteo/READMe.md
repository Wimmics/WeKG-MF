# Météo-France RDF Weather Dataset

The Météo-France RDF Weather dataset is an RDF dataset that provides access to meteorological measurments provided by 62 Météo-France weather stations located in different regions in metropolitan France and overseas departments. 
The dataset incorporates measurements of several weather parameters such as wind direction and speed, air pressure, precipitations, humidity and temperature. 

The RDF dataset is organised in different named graphs queryable through a SPARQL endpoint. 

The weather dataset namespace is ```http://ns.inria.fr/meteo/```. 

## RDF data modelling 

Based on a network of existing ontologies (SOSA/SSN, GeoSPARQL, Time Ontology), we define a minimal self-contained semantic model to capture the spatio-temporal aspects of meteorological data. 
For this purpose, we extend the SOSA observation, feature of interest and observable property classes and we provide the OWL definitions of these new classes. 

Also, we propose a SKOS vocabulary of weather observable properties and features of interest commonly used in weather reports.  

The semantic model and SKOS vocabulary are provided in the ```weather-dataset-metadata``` directory of the project. 

The model and vocabulary are intended to be adopted and extended by any meteorological data provider. 

## Pipeline generation 

The pipeline generation of the weather RDF dataset involves several steps including the preprocessing and loading data in MongoDB database as JSON collections.
Then the translation into RDF is carried out using the Morph-xr2RML tool, an implementation of the xR2RML mapping language for MongoDB databases. 

Note that the pipeline generation including all steps is fully executed thanks to the ```run_pipeline.sh``` script available in ```Lifting-dataset``` directory.

The script ```run_pipeline.sh``` needs 4 arguments: 
 
* JSON collection name (if a collection with the same name already exists in MongoDB, it will be dropped),

* Path directory to the csv files, e.g., raw-weather-data/yyyy/csv

* Mapping rules file : e.g., mapping_observation_tpl.ttl

* Output file name (e.g, ```rdf-dataset-yyyy.ttl```)

Example : 

./run_pipeline.sh collection022021 raw-weather-data/2021/csv mapping_observation_tpl.ttl rdf-dataset-02-2021.ttl

Generated RDF data files can be loaded in Virtuoso as separate named graphs. Scripts are provided in directory ```virtuoso```.

## Prefixes of Ontologies and Vocabularies used in Météo-France RDF Dataset

| Prefix  | URI |
| ------------- | ------------- |
| geo  | http://www.w3.org/2003/01/geo/wgs84_pos#  |
| geosparql | http://www.opengis.net/ont/geosparql# |
| nerc | http://vocab.nerc.ac.uk/collection/P07/current/ |
| qudt | http://qudt.org/2.0/schema/qudt |
| qudt-unit | http://qudt.org/2.1/vocab/unit  |
| qudtkind | http://qudt.org/vocab/quantitykind/ |
| skos | http://www.w3.org/2004/02/skos/core#  |
| qb | http://purl.org/linked-data/cube# |
| sosa |http://www.w3.org/ns/sosa/  |
| ssn | http://www.w3.org/ns/ssn/ |
| time | http://www.w3.org/2006/time# |
| weo | http://ns.inria.fr/meteo/ontology/ |
| wep | http://ns.inria.fr/meteo/ontology/property/ |
| wevp | http://ns.inria.fr/meteo/vocab/weatherproperty/ |
| wevf | http://ns.inria.fr/meteo/vocab/meteorologicalfeature/ |
| wes | http://ns.inria.fr/meteo/observationslice/ |
## Downloading and SPARQL querying 

The dataset is downloadable as a set of RDF dumps (in Turtle syntax) from Zenodo : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5593216.svg)](https://doi.org/10.5281/zenodo.5593216)

Several SPARQL queries are provided in ```sparql-examples``` directory and serves as examples of exploitation of the dataset. A jupyter notebook '''WeKG-MFQuerying.ipynb''' is available to demonstrate how the results of some SPARQL queries can be used to generate visualizations. 

The number of triples for each named graph is provided as follows :

| Named Graph  | No. of RDF triples |
| ------------- | ------------- |
| http://ns.inria.fr/meteo/ontology  | 193  |
| http://ns.inria.fr/meteo/vocab | 346 |
| http://ns.inria.fr/meteo/weatherstation | 794 |
| http://ns.inria.fr/meteo/observation/2021 | 18.899.921 |
| http://ns.inria.fr/meteo/observation/2020 | 20.868.650  |
| http://ns.inria.fr/meteo/observation/2019 | 20.832.677 |
