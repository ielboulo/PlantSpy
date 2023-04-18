<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Plantspy - Dashboard</title>

    <!-- Custom fonts for this template-->
    <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

    <!-- Custom styles for this template-->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body id="page-top">

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
    <!-- Page Wrapper -->
    <div id="wrapper">

       

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">


                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                    <div class="d-sm-flex align-items-center justify-content-between mb-4">
                        <h1 class="h3 mb-0 text-gray-800">Monitoring ML Planstpy</h1>
                        <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i
                                class="fas fa-download fa-sm text-white-50"></i> Télécharger l'historique</a>
                    </div>

                    <!-- Content Row -->
                    <div class="row">

                        <!-- Earnings (Monthly) Card Example -->
                        <div class="col-xl-3 col-md-6 mb-4">
                            <div class="card border-left-primary shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                                Nb Data testé</div>
                                            <?php
function count_files($dir) {
    $num_files = 0;
    if ($handle = opendir($dir)) {
        while (($file = readdir($handle)) !== false) {
            if (!in_array($file, array('.', '..'))) {
                if (is_dir($dir . '/' . $file)) {
                    $num_files += count_files($dir . '/' . $file);
                } else {
                    $num_files++;
                }
            }
        }
    }
    closedir($handle);
    return $num_files;
}


$file_count = count_files('data/test');

echo '<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' . $file_count . '</div>';
?>

                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-calendar fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Earnings (Monthly) Card Example -->
                        <div class="col-xl-3 col-md-6 mb-4">
                            <div class="card border-left-success shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                                Nb Data Train</div>
                                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php $file_count = count_files('data/train');

echo '<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' . $file_count . '</div>';
?></div>
                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Earnings (Monthly) Card Example -->
                        <div class="col-xl-3 col-md-6 mb-4">
                            <div class="card border-left-info shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Nb data Valide
                                            </div>
                                            <div class="row no-gutters align-items-center">
                                                <div class="col-auto">
                                                <?php $file_count = count_files('data/valid');

echo '<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' . $file_count . '</div>';
?>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pending Requests Card Example -->
                        <div class="col-xl-3 col-md-6 mb-4">
                            <div class="card border-left-warning shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                                Nb total Data</div>
                                                <?php $file_count = count_files('data');

echo '<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' . $file_count . '</div>';
?>
                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-comments fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Content Row -->


                    <div class="row">

                        <!-- Area Chart -->
                        <div class="col-xl-8 col-lg-7">
                            <div class="card shadow mb-4">
                                <!-- Card Header - Dropdown -->
                                <div
                                    class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
                                    
                                </div>
                                <!-- Card Body -->
                                <div class="card-body">
                                    <div class="chart-area">
                                        <canvas id="myChart"></canvas>
                                    </div>
                                </div>
                            </div>
                        </div>


                    </div>

                   
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

            <!-- Footer -->
            <footer class="sticky-footer bg-white">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>Copyright &copy; Your Website 2021</span>
                    </div>
                </div>
            </footer>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Logout Modal-->
    <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                    <a class="btn btn-primary" href="login.html">Logout</a>
                </div>
            </div>
        </div>
    </div>

    <script>

var ctx = document.getElementById('myChart').getContext('2d');
    var data1 = <?php echo $jsonData1; ?>;
    var data2 = <?php echo $jsonData2; ?>;
    console.log(data1);
    console.log(data2);
    let label_graph = [];
    for (let i = 0; i < data1.datasets[0].data.length; i++) {
        label_graph.push(i);
    }
    var data = {
        labels : label_graph,
        datasets:[
            {
                label: 'Model accuracy train',
                data: data1.datasets[0].data,
                backgroundColor: "#8e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
            },
            {
                label: 'Model accuracy',
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
    <!-- Bootstrap core JavaScript-->
    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom scripts for all pages-->
    <script src="js/sb-admin-2.min.js"></script>

    <!-- Page level plugins -->
    <script src="vendor/chart.js/Chart.min.js"></script>

    <!-- Page level custom scripts -->
    <script src="js/demo/chart-bar-demo.js"></script>
    <script src="js/demo/chart-pie-demo.js"></script>

</body>

</html>