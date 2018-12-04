<script src="http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.13.0/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>

function graph(url_result, makeChart) {
  var hco =  [
  { // 1
      backgroundColor: "#afb2f1",
      borderColor: "#9194d3",
      pointColor: "#9194d3",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // 2
      backgroundColor: "#fac496",
      borderColor: "#dca678",
      pointColor: "#dca678",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // 3
      backgroundColor: "#add0f3",
      borderColor: "#8fb2d5",
      pointColor: "#8fb2d5",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // 4
      backgroundColor: "#b9f4ad",
      borderColor: "#9bd68f",
      pointColor: "#9bd68f",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // yellow
      // backgroundColor: "#93C1CC",
      borderColor: "rgba(253,180,92,1)",
      pointColor: "rgba(253,180,92,1)",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // grey
      // backgroundColor: "rgba(148,159,177,0.2)",
      borderColor: "rgba(148,159,177,1)",
      pointColor: "rgba(148,159,177,1)",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  },
  { // dark grey
      // backgroundColor: "rgba(77,83,96,0.2)",
      borderColor: "rgba(77,83,96,1)",
      pointColor: "rgba(77,83,96,1)",
      pointHoverRadius: 8,
      pointBorderWidth: 2
  }
];
    var graph_data_x = [], graph_data_y = [];
    if(div_id == ""){
      $("canvas#myChart").remove();
      $("div#chart-CPU").append('<canvas id="myChart"></canvas>');
    }
    else{
      if( old_div == ""){
        $(div_id).html('<canvas id="'+makeChart+'"></canvas>')
      }
      else{
        $("canvas#"+makeChart).remove();
        $(div_id).append('<canvas id="'+makeChart+'"></canvas>');
      }
    }
    old_div = div_id;

    var chartData = {
      labels: graph_data_x,
      datasets: [ ]
    };

    var chartOptions = {
      title: {
        display: true,
        text : "title name"
      },
      tooltips: {
        mode: "index",
        intersect: true,
        position: 'nearest',
        bodySpacing: 4,
      },
      legend: {
        display: true,
        labels: {
        fontColor: 'grey',
        usePointStyle: true
      }
    },
      scales: {
        xAxes: [{
          display: true,
          beginAtZero: true,
          type: 'time',
          time: {
            unit: 'minute',
            unitStepSize: 60
          }
        }],
        yAxes: [{
          display: true,
          // stacked: true, // graph stacked
          ticks: {
            beginAtZero: true,
            type: 'linear',
            position: 'left',
            // setpSize: 5,
            // callback: function(v){
            //   return (v*100).toFixed(2) + '%';
            // }
          }
        }]
      },
    };

    if( div_id == '#chart-DISK' || div_id == '#chart-Memory' || div_id == '#chart-NIC' || div_id == '#chart-Swap'){
      // console.log('disk, memory, file, nic, swap');
      Chart.scaleService.updateScaleDefaults('linear', {
          ticks: {
            callback: function(v){
              return v;
            }
          }
      });
      if ( div_id == '#chart-Memory') Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel + ' KB'
      else if ( div_id == '#chart-DISK' ) Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel + ' bytes'
      else if ( div_id == '#chart-NIC' ) Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel + ' bps'
      else if ( div_id == '#chart-Swap' ) Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel + ' bytes'
      else Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel
    } else {
      // console.log('cpu, load, file, else');
      Chart.scaleService.updateScaleDefaults('linear', {
          ticks: {
            stepSize: 10,
            callback: function(v){
              return v + '%';
            }
          }
      });
      Chart.defaults.global.tooltips.callbacks.label = (idx, data) => data.datasets[idx.datasetIndex].label + ' : ' + idx.yLabel.toFixed(2) + '%'
    }

    var ctx = document.getElementById(makeChart).getContext('2d');

    Chart.defaults.global.defaultFontFamily = "Lato";
    Chart.defaults.global.defaultFontSize = 12;
    Chart.defaults.global.responsive = true;
    // Chart.defaults.global.time.stepSize = 60;
    // Chart.defaults.global.animation = false;
    Chart.defaults.global.maintainAspectRatio = false;

    $.ajax({
      url: url_result,
      async: false,
      type: 'get',
      dataType: 'json',
      success: function(data) {
        var jdata = data['result']['0']['rows'];
        chartOptions.title.text = data['result']['0']['nm'];
        for (var k = 0; k < data['result'].length; k++) {
          jdata = data['result'][k]['rows'];

          for (var i = 0; i < jdata.length; i++) {
            graph_data_x.push(new Date(jdata[i]['time'] * 1000));
            graph_data_y.push(parseFloat(jdata[i]['value']));
          }

          var newDataset = {
            label: data['result'][k]['type'],
            borderWidth: 1,
            fill: 'origin',
            data: graph_data_y,
          }

          var realNewData = Object.assign(newDataset,hco[k]);

          chartData.datasets.push(realNewData);
          graph_data_y = [];
        }
      }
    })

    var myChart = new Chart(ctx, {
      type: 'line',
      data: chartData,
      options: chartOptions
    });
    myChart.update();
}


$("canvas#myChart").remove();
$("div#box-body").append('<canvas id="myChart"></canvas>');

var chartData, chartOptions;

chartData = {
  labels: data_x,
  datasets: [{
    label: "Notification Count ",
    data: data_y,
    // backgroundColor: "rgba(54, 162, 235, 0.2)"
    borderColor: '#8cd7cb',
    backgroundColor: '#f5fffe'
  }]
};

chartOptions = {
  scales: {
    yAxes: [{
      display: true,
      ticks: {
        beginAtZero: true,
        type: 'linear',
        position: 'left'
      }
    }]
  },
};

var ctx = document.getElementById('myChart').getContext('2d');

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 12;
Chart.defaults.global.responsive = true;
// Chart.defaults.global.animation = false;
Chart.defaults.global.maintainAspectRatio = false;

var myChart = new Chart(ctx, {
  type: 'line',
  data: chartData,
  options: chartOptions
});
