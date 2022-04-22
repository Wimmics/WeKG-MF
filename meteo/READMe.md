# WeaKG-MF: Weather Knowlege Graph of Météo-France Archives

The Météo-France RDF Weather dataset (WeaKG-MF) is an RDF knowledge graph that provides access to meteorological measurements provided by 62 Météo-France weather stations located in different regions in metropolitan France and overseas departments. The dataset incorporates measurements of several weather parameters such as wind direction and speed, air pressure, precipitations, humidity and air temperature. These measurements are provided every three hours per day.

The WeaKG-MF namespace is ```http://ns.inria.fr/meteo/```. 

## RDF data modelling 

- The semantic model of WeaKG knowledge graph is available in the ```ontology``` directory of this project.

- Based on a network of existing ontologies (SOSA/SSN, GeoSPARQL, QUDT, OWL-Time ontology, RDF data Cube Vocabulary), we define a reusable and self-contained semantic model that describes the semantics of meteorological data. ```weo:MeterologicalObservation``` is the core class of our model; it supports the description of a single, atomic observation. A meteorological observation is related to a particular feature of interest, instance of class ```weo:MeteorologicalFeature```, and an observable property, instance of class ```weo:WeatherProperty```. These three classes specialize the following SOSA/SSN classes: [sosa:Observation](https://www.w3.org/TR/vocab-ssn/#SOSAObservation), [sosa:ObservableProperty](https://www.w3.org/TR/vocab-ssn/#SOSAObservableProperty) and [sosa:FeatureOfInterest](https://www.w3.org/TR/vocab-ssn/#SOSAFeatureOfInterest) classes. The `weatherdataset-model.ttl` provides the formal definitions in OWL of each class in our model. 

- We also propose a SKOS vocabulary of weather observable properties and features of interest commonly used in weather reports. The current version of the SKOS vocabulary ```features-properties-vocabulaire.ttl``` includes 6 features of interest (air, wind, surface, gust, cloud, precipitations) and 21 observable properties (temperature, wind speed, diffrential pressure, ...). 

- The model and vocabulary are intended to be adopted and extended by any meteorological data provider. 

## Prefixes of ontologies and vocabularies used in WeaKG-MF

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

## Downloading and SPARQL querying 

**A new version of WeaKG is now available ! Please download RDF dumps (in Turtle syntax) from Zenodo :** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5925413.svg)](https://doi.org/10.5281/zenodo.5925413)

It can also be queried through our Virtuoso SPARQL endpoint [http://weakg.i3s.unice.fr/sparql](http://weakg.i3s.unice.fr/sparql)

In order to re-use the WeaKG dataset and create your local SPARQL endpoint, we recommend to use the [openLink Virtuoso Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8). We provide scripts availabe in ```Lifting-dataset/virtuoso``` repository to upload the downloaded WeaKG  RDF dataset in different named graphs. Use the script ```import-weather-dataset``` as main entry point. 

Several SPARQL queries are provided in ```sparql-examples``` directory and serves as illustrative examples showing how data may be retreived from the WeaKG graph. A Jupyter Notebook ```WeaKG-MFQuerying.ipynb``` demonstrates how the results of some SPARQL queries can be used to generate visualizations very useful for experts in different domains. 

Statistics about WeaKG-MF is provided as follows :

| Named Graph  | No. of RDF triples |
| ------------- | ------------- |
| http://ns.inria.fr/meteo/ontology  | 193  |
| http://ns.inria.fr/meteo/vocab | 346 |
| http://ns.inria.fr/meteo/weatherstation | 794 |
| http://ns.inria.fr/meteo/observation/2021 | 20.604.775 |
| http://ns.inria.fr/meteo/observation/2020 | 20.868.650  |
| http://ns.inria.fr/meteo/observation/2019 | 20.832.677 |
| http://ns.inria.fr/meteo/observation/2018 | 19.684.672 |
| http://ns.inria.fr/meteo/observation/2017 | 20.539.699 |

## WeaKG-MF Pipeline Generation

We provide a fully automatic pipeline that enables us the maintenance and update of the WeaKG graph with new weather data from the Météo-France organism. This pipeline allowed us to generate the WeaKG dataset and then we reuse it to update the WeaKG knowledge graph over time. The pipeline involves several steps including the preprocessing and loading data in MongoDB database as JSON collections and their transformation in RDF data. The [Morph-xR2RML tool](https://github.com/frmichel/morph-xr2rml/) allows the generation of RDF data. 
 
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
