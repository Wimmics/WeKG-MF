This folder provides the scripts, configuration and mappings files needed to translate the dataset into RDF using Morph-xR2RML.

Script `run_xr2rml_all.sh` is the main entry point.
Comment or uncomment the lines as needed.


- The 'WeatherDatasetModel.ttl' defines the semantic model of the metereological dataset. According to SOSA ontology, we defined 6 features of interest (air, wind, surface, gust, cloud, precipitations) and 21 observable properties (temperature, wind speed, diffrential pressure, ...). We have reused several ontologies : SOSA/SSN ontologies, QUDT, Time Ontology. The semantic model is still under development. 

