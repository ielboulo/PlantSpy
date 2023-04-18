<?php
// Lire les données du fichier accuracy_train.txt
$data1 = file('results/accuracy_train.txt');

// Extraire les valeurs numériques
$values1 = array();
foreach ($data1 as $line) {
  preg_match('/\d+\.\d+/', $line, $matches);
  $value = floatval($matches[0]);
  $values1[] = $value;
}

// Créer un tableau de données pour le graphique
$chartData1 = array(
  'labels' => array('January', 'February', 'March', 'April', 'May', 'June'),
  'datasets' => array(
    array(
      'label' => 'Model accuracy train',
      'backgroundColor' => '#8e73df',
      'hoverBackgroundColor' => '#2e59d9',
      'borderColor' => '#4e73df',
      'data' => $values1,
    ),
  ),
);

// Convertir le tableau de données en JSON
$jsonData1 = json_encode($chartData1);


// Lire les données du fichier accuracy_test.txt
$data2 = file('results/accuracy.txt');

// Extraire les valeurs numériques
$values2 = array();
foreach ($data2 as $line) {
  preg_match('/\d+\.\d+/', $line, $matches);
  $value = floatval($matches[0]);
  $values2[] = $value;
}

// Créer un tableau de données pour le graphique
$chartData2 = array(
  'labels' => array('January', 'February', 'March', 'April', 'May', 'June'),
  'datasets' => array(
    array(
      'label' => 'Model accuracy test',
      'backgroundColor' => '#e74a3b',
      'hoverBackgroundColor' => '#c0392b',
      'borderColor' => '#e74a3b',
      'data' => $values2,
    ),
  ),
);

// Convertir le tableau de données en JSON
$jsonData2 = json_encode($chartData2);
?>

<!-- Afficher le graphique en utilisant Chart.js dans une page HTML -->
<!DOCTYPE html>
<html>
<head>
  <title>Mon graphique</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <canvas id="myChart"></canvas>
  <script>
    var ctx = document.getElementById('myChart').getContext('2d');
    var data1 = <?php echo $jsonData1; ?>;
    var data2 = <?php echo $jsonData2; ?>;
    
    var data = {
        labels :["January", "February", "March", "April", "May", "June"],
        datasets:[
            {
                label: 'Model accuracy train',
                data: data1.datasets[0].data,
                backgroundColor: "#8e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
            },
            {
                label: 'Model accuracy test',
                data: data2.datasets[0].data,
                backgroundColor: "#e74a3b",
                hoverBackgroundColor: "#c0392b",
                borderColor: "#e74a3b",
            }
        ]
    }
    
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      
    });
  </script>
</body>
</html>
