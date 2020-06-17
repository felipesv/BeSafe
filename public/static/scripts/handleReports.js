$(document).ready(function() {
  // script to use
  script1 = $.getScript('https://www.felipesv.tech/static/scripts/firebaseConfig.js');

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
      // page #1
      let contp1 = 0;
      if ($('#typeAlertRpt').val().length > 0) {
        contp1++;
        $('#n-1').removeAttr('disabled');
      }

      // page #2
      let contp2 = 0;
      if ($('#typeAggressorRpt').val().length > 0) {
        contp2++;
        $('#n-2').removeAttr('disabled');
      }

      // page #3
      let contp3 = 0;
      if ($('#collectiveGroupRpt').val().length > 0)
        contp3++;
      if ($('#descriptionRpt').val().length > 0)
        contp3++;
      if ($('#complaintRpt').val().length > 0)
        contp3++;
      
      if (contp3 == 3)
        $('#n-3').removeAttr('disabled');

      // page #4
      let contp4 = 0;
      if ($('#stagesRpt').val().length > 0)
        contp4++;
      if ($('#neighborhoodRpt').val().length > 0)
        contp4++;
      if ($('#latitudeRpt').val().length > 0 && $('#longitudeRpt').val().length > 0)
        contp4++;
 
      cont = contp1 + contp2 + contp3 + contp4;
      if (cont == 8) {
        $('#createReportRpt').prop('disabled', false);
      } else {
        $('#createReportRpt').prop('disabled', true);
      }

      $('#formFields').html(cont + '/8');
      console.log("Van seleccionados "+ cont + "/8");
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
    // handle stage click
    $('.chooseStage').on('click', function() {
      const chosenVal = $(this).attr('attr-id');
      $('#stagesRpt').val(chosenVal);
      validCampus();
    });
    //handle autocomplete fields chosen
    function uploadAutoComplete(dataautocomplete, input, chooseVal) {
      $(input).autocomplete({
        source: dataautocomplete,
        select: function( event, ui ) {
          const chosenVal = ui.item.id;
          $(chooseVal).val(chosenVal);
          validCampus();
        }
      });

      $(input).on('change', function() {
        if ($(this).val().length === 0)
          $(chooseVal).val('');
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

    const dbRefNeighborhoods = firebase.database().ref().child('neighborhood');
    dbRefNeighborhoods.on('value', snap => {
      const neighborhoods = snap.val();
      const dataautocomplete = [];

      Object.values(neighborhoods).forEach(item => {
        dataautocomplete.push({
          'value': item.name,
          'id': item.idNeighborhood
        });
      });
      uploadAutoComplete(dataautocomplete, '#searchNeighborhood', '#neighborhoodRpt');
    });

    const dbRefIndentity = firebase.database().ref().child('collective_group');
    dbRefIndentity.on('value', snap => {
      const collective_group = snap.val();
      const dataautocomplete = [];

      Object.values(collective_group).forEach(item => {
        dataautocomplete.push({
          'value': item.name,
          'id': item.idCollective
        });
      });

      uploadAutoComplete(dataautocomplete, '#searchIdentity', '#collectiveGroupRpt');
    });

    const dbRefStages = firebase.database().ref().child('stages');
    dbRefStages.on('value', snap => {
      const stages = snap.val();
      const dataautocomplete = [];

      Object.values(stages).forEach(item => {
        dataautocomplete.push({
          'value': item.name,
          'id': item.idStages
        });
      });

      uploadAutoComplete(dataautocomplete, '#searchStage', '#stagesRpt');
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
  $('#n-1').click(function (e) { 
    e.preventDefault();
    $('#second').animate({'left': '0'}, 'slow');
    $('#third').animate({'left': '100vw'}, 'slow');
    $('#fourth').animate({'left': '200vw'}, 'slow');
  });
  $('#n-2').click(function (e) { 
    e.preventDefault();
    $('#third').animate({'left': '0'}, 'slow');
    $('#fourth').animate({'left': '100vw'}, 'slow');
  });
  $('#n-3').click(function (e) { 
    e.preventDefault();
    $('#fourth').animate({'left': '0'}, 'slow');
    $('.submit').css('display', 'inline-block');
  });
  $('#b-1').click(function (e) { 
    e.preventDefault();
    $('#second').animate({'left': '100vw'}, 'slow');
    $('#third').animate({'left': '200vw'}, 'slow');
    $('#fourth').animate({'left': '300vw'}, 'slow');
  });
  $('#b-2').click(function (e) { 
    e.preventDefault();
    $('#third').animate({'left': '100vw'}, 'slow');
    $('#fourth').animate({'left': '200vw'}, 'slow');
  });
  $('#b-3').click(function (e) { 
    e.preventDefault();
    $('#fourth').animate({'left': '100vw'}, 'slow');
    $('#fifth').animate({'left': '+=100vw'}, 'slow');
  });
  $('#b-4').click(function (e) { 
    e.preventDefault();
    $('#fifth').animate({'left': '+=100vw'}, 'slow');
  });

  $('#n-1').prop('disabled', 'true');
  $('#n-2').prop('disabled', 'true');
  $('#n-3').prop('disabled', 'true');
});
