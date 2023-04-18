fetch('https://monsite.com/donnees.txt')
  .then(response => response.text())
  .then(data => {
    const values = data.trim().split('\n').map(line => {
      const value = parseFloat(line.split(': ')[1]);
      return value;
    });

    const chartData = {
      labels: ["January", "February", "March", "April", "May", "June"],
      datasets: [{
        label: "Revenue",
        backgroundColor: "#8e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: values,
      }],
    };

    const ctx = document.getElementById('myChart');
    const myBarChart = new Chart(ctx, {
      type: 'bar',
      data: chartData,
    });
  })
  .catch(error => console.error(error));