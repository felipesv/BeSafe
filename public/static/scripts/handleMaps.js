$(document).ready(function () {
  // script to use
  script1 = $.getScript('http://besafeapp.freevar.com/files/coordinatesPolygon.js');
  script2 = $.getScript('http://besafeapp.freevar.com/files/firebaseConfig.js')

  // when the script are loaded
  $.when(script1, script2).done(function() {
    /*
      script1:
        listPolygon: all the list of variable that containt the coordinates
    */

    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    // firebase variables
    const dbRefComuna = firebase.database().ref().child('comunas');
    const dbRefMapping = firebase.database().ref().child('mapping');
    const dbRefAlertType = firebase.database().ref().child('alert_type');

    // map variables
    var besafeMap = L.map('mapSafe').setView([3.4414560213815424, -76.52338027954102], 13);
    var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(besafeMap);

    // google charts
    google.charts.load('current', {'packages':['corechart']});

    // general variables
    let polygonsComunas = []; // each polygon is here
    let markerPoints = {}; // each marker is here

    let colorsComunas = []; // each color by comuna is here
    let nameComunas = []; // each comuna name is here
    let idComunas = []; // each comuna is is here
    let mappingPoints = []; // each points is here
    let alerttypes = {}; // each alert type is here

    let loadCount = 0; // para no cargar las comunas la primera vez
    const filters = {}; // ids type alert filters


    // function to load popup in polygon
    function popupPlygon() {
      polygonsComunas.forEach(polygon => {
        polygon.on('mouseover', function(e) {
          let popup = e.target.getPopup();
          popup.setLatLng(e.latlng).openOn(besafeMap)
        });
        polygon.on('mouseout', function(e) {
          e.target.closePopup();
        });
        polygon.on('mousemove', function(e){
          e.target.closePopup();
          var popup = e.target.getPopup();
          popup.setLatLng(e.latlng).openOn(besafeMap);
        });
        polygon.on('click', function() {
          //set data
          $("#chartNeighborhood").html("");
          $("#chartStages").html("");
          $("#chartCollective").html("");
          $("#titleModalPolygon").html(this.options.name);
          $("#totalCases").html("Total casos: 0");
          $("#totalComplaint").html("Total denuncias: 0");
          //create the charts
          getStadistics(this.options.idCom);

          $("#comunaDetails").modal("show");
        });
      });
    }

    // function to add polygon
    function polygonComunas() {
      let cntPos = 0;

      deletePolygon();
      polygonsComunas = [];

      listPolygon.forEach(comuna => {
        polygonsComunas.push(
          L.polygon(comuna, {
            color: colorsComunas[cntPos],
            weight: 1,
            name: nameComunas[cntPos], // this option doesnt exist
            idCom: idComunas[cntPos] // this option doesnt exist
          }).addTo(besafeMap)
          .bindPopup(nameComunas[cntPos])
        );
        cntPos++;
      });
      popupPlygon();
    }

    // function to add market on the map
    function markerMapping() {
      let iconClass = L.Icon.extend({
        options: {          
          iconSize:     [25, 41],
          shadowSize:   [50, 64],
          iconAnchor:   [12, 41],
          shadowAnchor: [4, 62],
          popupAnchor:  [-3, -76]
        }
      });

      deleteMarket();
      markerPoints = {};

      mappingPoints.forEach(point => {
        let idAlert = point.idAlerttype;
        let message, marker, icon;

        switch(alerttypes[idAlert].level) {
          case 0:
            icon = new iconClass({iconUrl: 'http://besafeapp.freevar.com/files/azulito.png'});
            message = "Otro";
            break;
          case 1:
            icon = new iconClass({iconUrl: 'http://besafeapp.freevar.com/files/rojito.png'});
            message = "Riesgo de vida";
            break;
          case 2:
            icon = new iconClass({iconUrl: 'http://besafeapp.freevar.com/files/naranjita.png'});
            message = "Riesgo físico o psicológico";
            break
        }

        if (Object.keys(filters).length != 0) {
          if (filters.hasOwnProperty(idAlert)) {
            marker = L.marker(
              [point.latitude, point.longitude],
              {icon: icon}
            ).addTo(besafeMap);
          }
        } else {
          marker = L.marker(
            [point.latitude, point.longitude],
            {icon: icon}
          ).addTo(besafeMap);
        }

        if (typeof marker !== 'undefined') {
          marker.bindTooltip(message);
          if (markerPoints.hasOwnProperty(idAlert)) {
            markerPoints[idAlert].push(marker);
          } else {
            markerPoints[idAlert] = [marker];
          }
        }
      });
    }

    // function to destroy each polygon
    function deletePolygon() {
      polygonsComunas.forEach(polygon => {
        polygon.remove();
      });
    }

    // function to destroy all markets
    function deleteMarket() {
      for (points in markerPoints) {
        markerPoints[points].forEach(market => {
          if (typeof market !== 'undefined')
            market.remove();
        });
      }
    }

    // read changes in database
    dbRefComuna.on('value', snap => {
      let comunasDict = snap.val();

      colorsComunas = [];
      nameComunas = [];

      for (comuna in comunasDict) {
        colorsComunas.push(comunasDict[comuna]['color']);
        nameComunas.push(comunasDict[comuna]['name']);
        idComunas.push(comunasDict[comuna]['idComuna'])
      }

      if (loadCount > 0)
        polygonComunas();
      loadCount++;
    });

    dbRefAlertType.on('value', snap => {
      let alerttypeDict = snap.val();

      alerttypes = {};

      for (type in alerttypeDict) {
        alerttypes[alerttypeDict[type]["idAlerttype"]] = alerttypeDict[type];
      }
    });

    dbRefMapping.on('value', snap => {
      let mappingDict = snap.val();

      mappingPoints = [];

      for (point in mappingDict) {
        mappingPoints.push(mappingDict[point]);
      }

      markerMapping();
    });

    $('.btnFiltro').on('click', function() {
      if($(this).attr('attr-ck') === "") {
        $(this).attr('attr-ck', 'checked');
        filters[$(this).attr('attr-id')] = $(this).text();
      } else {
        $(this).attr('attr-ck', '');
        delete filters[$(this).attr('attr-id')];
      }

      markerMapping();
    });

    $('.btnClearFilter').on('click', function() {
      const keysObj = Object.keys(filters);
      keysObj.forEach(key => {
        delete filters[key];
      })

      markerMapping();
    });

    $('.btnComuna').on('click', function() {
      if($(this).attr('attr-ck') === "") {
        $(this).attr('attr-ck', 'checked');
        polygonComunas();
      } else {
        $(this).attr('attr-ck', '');
        deletePolygon();
      }
    });

    function getStadistics(idComuna) {
      $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/stadistic",
        data: {
          idComuna: idComuna
        },
        success: function(out_msg) {
          $("#totalCases").html("Total casos: " + out_msg.total_cases);
          $("#totalComplaint").html("Total denuncias: " + out_msg.total_complaint);
          createCharts(out_msg);
        }
      });
    }

    function createCharts(data) {
      // neighborhood
      var dataNeighborhood = new google.visualization.DataTable();
      var optionsNeighborhood = {
        'title':'Casos por barrios',
        'width':467,
        'height':300
      };
      const dataChartNeighborhood = []
      for (item in data.neighborhood) {
        const subData = []
        subData.push(data.neighborhood[item].name);
        subData.push(data.neighborhood[item].cases);
        dataChartNeighborhood.push(subData);
      }
      dataNeighborhood.addColumn('string', 'Colectivo');
      dataNeighborhood.addColumn('number', 'Casos');
      dataNeighborhood.addRows(dataChartNeighborhood);
      var chartNeighborhood = new google.visualization.PieChart(document.getElementById("chartNeighborhood"));
      chartNeighborhood.draw(dataNeighborhood, optionsNeighborhood);

      // stages
      var dataStages = new google.visualization.DataTable();
      var optionsStages = {
        'title':'Casos por escenarios',
        'width':467,
        'height':300
      };
      const dataChartStage = []
      for (item in data.stages) {
        const subData = []
        subData.push(data.stages[item].name);
        subData.push(data.stages[item].cases);
        dataChartStage.push(subData);
      }
      dataStages.addColumn('string', 'Colectivo');
      dataStages.addColumn('number', 'Casos');
      dataStages.addRows(dataChartStage);
      var chartStages = new google.visualization.PieChart(document.getElementById("chartStages"));
      chartStages.draw(dataStages, optionsStages);

      // collective group
      var dataCollective = new google.visualization.DataTable();
      var optionsCollective = {
        'title':'Casos por grupos del collectivo',
        'width':467,
        'height':300
      };
      const dataChartCollective = []
      for (item in data.collective) {
        const subData = []
        subData.push(data.collective[item].name);
        subData.push(data.collective[item].cases);
        dataChartCollective.push(subData);
      }
      dataCollective.addColumn('string', 'Colectivo');
      dataCollective.addColumn('number', 'Casos');
      dataCollective.addRows(dataChartCollective);
      var chartCollective = new google.visualization.PieChart(document.getElementById("chartCollective"));
      chartCollective.draw(dataCollective, optionsCollective);
    }
  });
});