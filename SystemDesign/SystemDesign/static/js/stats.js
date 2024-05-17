function drawChart(type, data, labels, id="myChart", title='# Số lượng') {
  const ctx = document.getElementById(id);

  new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: [{
        label: title,
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}


function drawChartMD(type, data, labels, id="myChart", title='# Số lượng') {
  const ctx = document.getElementById(id);

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: title,
        data: data,
        borderWidth: 1

      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
