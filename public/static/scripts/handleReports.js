$(document).ready(function() {
  // script to use
  script1 = $.getScript('http://besafeapp.freevar.com/files/firebaseConfig.js');

  // when the script are loaded
  $.when(script1).done(function() {
    // map variables
    var reportMap = L.map('mapRpt').setView([3.4414560213815424, -76.52338027954102], 13);
    var OpenStreetMap_Mapnik = OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(reportMap);
    let markerRpt = 0;


    function validCampus() {
      let cont = 0;
      if ($('#typeAlertRpt').val().length > 0)
        cont++;
      if ($('#typeAggressorRpt').val().length > 0)
        cont++;
      if ($('#collectiveGroupRpt').val().length > 0)
        cont++;
      if ($('#stagesRpt').val().length > 0)
        cont++;
      if ($('#complaintRpt').val().length > 0)
        cont++;
      if ($('#descriptionRpt').val().length > 0)
        cont++;
      if ($('#neighborhoodRpt').val().length > 0)
        cont++;
      if ($('#latitudeRpt').val().length > 0 && $('#longitudeRpt').val().length > 0)
        cont++;
      
      if (cont == 8) {
        $('#createReportRpt').prop('disabled', false);
      } else {
        $('#createReportRpt').prop('disabled', true);
      }

      $('#formFields').html(cont + '/8');
    }

    // handle type violence click
    $('.chooseViolence').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#typeAlertRpt').val(chosenVal);
      validCampus();
    });
    // handle type aggressor click
    $('.chooseAgressor').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#typeAggressorRpt').val(chosenVal);
      validCampus();
    });
    // handle collective group click
    $('.chooseCollective').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#collectiveGroupRpt').val(chosenVal);
      validCampus();
    });
    // handle stage click
    $('.chooseStage').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#stagesRpt').val(chosenVal);
      validCampus();
    });
    //handle neighborhood chosen
    function uploadAutoComplete(dataautocomplete) {
      $('#searchNeighborhood').autocomplete({
        source: dataautocomplete,
        select: function( event, ui ) {
          const chosenVal = ui.item.id;
          $('#neighborhoodRpt').val(chosenVal);
          validCampus();
        }
      });

      $('#searchNeighborhood').on('change', function() {
        if ($(this).val().length === 0)
          $('#neighborhoodRpt').val('');
        validCampus();
      });
    }
    //handle description chosen
    $('#chooseDescription').on('change', function() {
      const chosenVal = $(this).val();
      $('#descriptionRpt').val(chosenVal);
      validCampus();
    });
    // handle stage click
    $('.chooseComplaint').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#complaintRpt').val(chosenVal);
      validCampus();
    });
    // handle coordinates
    $('.chooseCoordinateM').on('click', function() {
      $("#modalMapRpt").modal('show');
      setTimeout(function() {
        reportMap.invalidateSize();
      }, 1000);
    });

    $('.chooseCoordinateC').on('click', function() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          $("#latitudeRpt").val(position.coords.latitude);
          $("#longitudeRpt").val(position.coords.longitude);
          validCampus();
        });
      }
    });


    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    // firebase variables
    const dbRefNeighborhoods = firebase.database().ref().child('neighborhood');
    //
    dbRefNeighborhoods.on('value', snap => {
      const neighborhoods = snap.val();
      const dataautocomplete = [];

      Object.values(neighborhoods).forEach(item => {
        dataautocomplete.push({
          'value': item.name,
          'id': item.idNeighborhood
        });
      });
      
      uploadAutoComplete(dataautocomplete);
    });

    //LEAFLET click map
    reportMap.on('click', function(e) {
      if (markerRpt != 0)
        markerRpt.remove();
      markerRpt = L.marker([e.latlng.lat, e.latlng.lng]).addTo(reportMap);
      $("#latitudeRpt").val(e.latlng.lat);
      $("#longitudeRpt").val(e.latlng.lng);
      validCampus();
    });
  });
});