# WeKG-MF: Weather Knowlege Graph Météo-France

The Météo-France RDF Weather dataset is an RDF knowledge graph that provides access to meteorological measurments provided by 62 Météo-France weather stations located in different regions in metropolitan France and overseas departments. The dataset incorporates measurements of several weather parameters such as wind direction and speed, air pressure, precipitations, humidity and air temperature. These measurements are provided every three hours per day.

The WeKG-MF namespace is ```http://ns.inria.fr/meteo/```. 

## RDF data modelling 

Based on a network of existing ontologies (SOSA/SSN, GeoSPARQL, QUDT, OWL-Time ontology, RDF data Cube Vocabulary), we define a reusable and self-contained semantic model that semantically describes the multiple dimensions behind meteorological data. For this purpose, we extend the SOSA observation, feature of interest and observable property classes and we provide the OWL definitions of these new classes. Also, we propose a SKOS vocabulary of weather observable properties and features of interest commonly used in weather reports.  

The semantic model and SKOS vocabulary are provided in the ```ontology``` directory of the project. The `weatherdataset-model.ttl` defines the semantic model of the metereological dataset. In the SKOS vocabulary, we defined 6 features of interest (air, wind, surface, gust, cloud, precipitations) and 21 observable properties (temperature, wind speed, diffrential pressure, ...). The model and vocabulary are intended to be adopted and extended by any meteorological data provider. 


## Downloading and SPARQL querying 

**A new version of WeKG is now available ! Please go and download RDF dumps (in Turtle syntax) from Zenodo :** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5925413.svg)](https://doi.org/10.5281/zenodo.5925413)

In order to use the WeKG dataset and create a local SPARQL endpoint, we recommend you to use the [openLink Virtuoso Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8). We provide scripts availabe in ```Lifting-dataset/virtuoso``` repository to upload the downloaded WeKG dataset in different named graphs. Use the script ```import-weather-dataset``` as main entry point. 

Several SPARQL queries are provided in ```sparql-examples``` directory and serves as illustrative examples showing how data may be retreived from the WeKG graph. A Jupyter Notebook ```WeKG-MFQuerying.ipynb``` demonstrates how the results of some SPARQL queries can be used to generate visualizations very useful for experts in different domains. 

The number of triples for each named graph is provided as follows :

| Named Graph  | No. of RDF triples |
| ------------- | ------------- |
| http://ns.inria.fr/meteo/ontology  | 193  |
| http://ns.inria.fr/meteo/vocab | 346 |
| http://ns.inria.fr/meteo/weatherstation | 794 |
| http://ns.inria.fr/meteo/observation/2021 | 18.899.921 |
| http://ns.inria.fr/meteo/observation/2020 | 20.868.650  |
| http://ns.inria.fr/meteo/observation/2019 | 20.832.677 |


## Prefixes of ontologies and vocabularies used in WeKG-MF

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
| wes-dimension| <http://ns.inria.fr/meteo/observationslice/dimension#> |
| wes-measure| <http://ns.inria.fr/meteo/observationslice/measure#> |
| wes-attribute| <http://ns.inria.fr/meteo/observationslice/attribute#> |


## Pipeline Generation

We provide a fully automatic pipeline that enables us the maintenance and update of the WeKG graph with new weather data from the Météo-France Organism. This pipeline allowed us to generate the WeKG dataset and then it is reused to update it along time. The pipeline involves several steps including the preprocessing and loading data in MongoDB database as JSON collections and their transformation in RDF data. The [Morph-xR2RML tool](https://github.com/frmichel/morph-xr2rml/) allows the generation of RDF data. 
 
 The script ```run_pipeline.sh``` available in ```Lifting-dataset``` directory is the main entry point of the pipeline.

The script ```run_pipeline.sh``` needs 3 arguments: 
 
* JSON collection name: the CSV files of weather report downloaded from the Meteo-France Website are loaded as JSON collection in MongoDB.

* Mapping rules file : mappings files are available in ```Lifting-dataset/xr2rml```, e.g., mapping_observation_tpl.ttl

* Output file name : e.g, ```rdf-dataset-yyyy.ttl```

Example : 

```bash
./run_pipeline.sh collection022021 mapping_observation_tpl.ttl rdf-dataset-02-2021.ttl
```
More informations are available in ```Lifting-dataset```repository !
