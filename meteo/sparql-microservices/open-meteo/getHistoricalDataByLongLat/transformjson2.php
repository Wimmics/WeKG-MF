<?php

//$url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2022-06-28&end_date=2022-07-12&daily=shortwave_radiation_sum,et0_fao_evapotranspiration&timezone=GMT";

$url = $_GET['url'];

//$url = str_replace(' ', '+', $url);

// Construct the API request URL
//$requestUrl = $url . '?' . http_build_query($queryParams);

$options = array(
    'http' => array(
        'method' => 'GET',
        'header' => 'Accept: application/json' // Spécifie le type de contenu attendu
    ), 
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
);

// Configuration des options de contexte
$context = stream_context_create($options);

// Make the API call
$response = file_get_contents($url, false, $context);


// Check if the request was successful
if ($response !== false) {
    $decoded_json = json_decode($response, true);
    if ($decoded_json === null) {
        echo 'Erreur JSON : ' . json_last_error_msg();
    } else {
        $latitude = $decoded_json['latitude'];
        $longitude = $decoded_json['longitude'];

        $time = $decoded_json['daily']['time'];
        $daily_params = array_keys($decoded_json['daily']);

        $daily_result = array();

        foreach ($time as $index => $date) {
            $daily_entry = array('time' => $date);

            foreach ($daily_params as $param) {
                if ($param !== 'time') {
                    $daily_entry[$param] = $decoded_json['daily'][$param][$index];
                }
            }

            $daily_result[] = $daily_entry;
        }

        $output = array(
            'latitude' => $latitude,
            'longitude' => $longitude,
            'daily_result' => $daily_result
        );

        $json = json_encode($output, JSON_PRETTY_PRINT);
        echo $json;
    }
} else {
    echo 'Erreur lors de la récupération des données.';
}
?>
