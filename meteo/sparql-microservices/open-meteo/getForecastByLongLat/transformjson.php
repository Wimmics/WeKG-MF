<?php

//$url = "https://api.open-meteo.com/v1/forecast?latitude=49.383&longitude=13.41&timezone=GMT&daily=temperature_2m_max,temperature_2m_min,precipitation_sum";

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
    //var_dump($http_response_header);

    // Tentative de décodage JSON
    //$data = json_decode($response, true);
    $decoded_json = json_decode($response, true);
    if ($decoded_json === null) {
        echo 'Erreur JSON : ' . json_last_error_msg();
    } 
}

$latitude = $decoded_json['latitude'];
$longitude = $decoded_json['longitude'];

$time = $decoded_json['daily']['time'];
$temp_max_2m = $decoded_json['daily']['temperature_2m_max'];
$temp_min_2m = $decoded_json['daily']['temperature_2m_min'];
$precipitation_sum = $decoded_json['daily']['precipitation_sum'];
// Tableau résultant
$result = [];

// Boucle pour créer les objets JSON
for ($i = 0; $i < count($time); $i++) {
    $obj = [
        "time" => $time[$i],
        "temp_min_2m" => $temp_min_2m[$i],
        "temp_max_2m" => $temp_max_2m[$i],
        "precipitation_sum" => $precipitation_sum[$i]
    ];
    $result[] = $obj;
}

$obj = [
    "longitude" => $longitude,
    "latitude" => $latitude,
    "forecast" => $result
];

// Conversion en JSON
$json = json_encode($obj);

// Affichage du résultat
echo $json;
