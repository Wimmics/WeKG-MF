
In order to generate spatio-temporal slices corresponding to a specific weather station, you should perform a CURL using a sparql query in a file: 

```curl -H "Accept: text/turtle" --output ./RDFslices.ttl --data-urlencode "query@ConstructQuery.rq"  https://weakg.i3s.unice.fr/sparql```

The CONSTRUCT query ```ConstructQuery.rq``` provides the transformation of a historical weather atomic observation stored initially in WeKG-MF and generates RDF data conforming the ```wes:annualTimeSeries``` data structure described in ```DSDAnnualTimesSeriesAirTemperatures```.