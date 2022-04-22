
## Data Modelling 

The semantic model of WeaKG knowledge graph is available in the ```ontology``` directory of this project.

Based on a network of existing ontologies (SOSA/SSN, GeoSPARQL, QUDT, OWL-Time ontology, RDF data Cube Vocabulary), we define a reusable and self-contained semantic model that describes the semantics of meteorological data. ```weo:MeterologicalObservation``` is the core class of our model; it supports the description of a single, atomic observation. A meteorological observation is related to a particular feature of interest, instance of class ```weo:MeteorologicalFeature```, and an observable property, instance of class ```weo:WeatherProperty```. These three classes specialize the following SOSA/SSN classes: [sosa:Observation](https://www.w3.org/TR/vocab-ssn/#SOSAObservation), [sosa:ObservableProperty](https://www.w3.org/TR/vocab-ssn/#SOSAObservableProperty) and [sosa:FeatureOfInterest](https://www.w3.org/TR/vocab-ssn/#SOSAFeatureOfInterest) classes. The `weatherdataset-model.ttl` provides the formal definitions in OWL of each class in our model. 

We also propose a SKOS vocabulary of weather observable properties and features of interest commonly used in weather reports. The current version of the SKOS vocabulary ```features-properties-vocabulaire.ttl``` includes 6 features of interest (air, wind, surface, gust, cloud, precipitations) and 21 observable properties (temperature, wind speed, diffrential pressure, ...). 

The model and vocabulary are intended to be adopted and extended by any meteorological data provider. 
