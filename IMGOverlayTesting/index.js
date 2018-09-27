var ZoomLevelChanges = [2,3,5,7,10,15];
var startingZoom = 8, minZoom=7;
var map;
var infowindows = [];

function getDataFromFields(){
  try {
    area = parseFloat($("#roof-SA").val());
  }
  catch(err){
    area = null;
  }
  try {
    inclination = parseFloat($("#roof-I").val());
  }
  catch(err){
    inclination = null;
  }
  try {
    eff = parseFloat($("#eff").val());
  }
  catch(err){
    eff = null;
  }
  
  

  if (!!!area) {
    area = 'undefined';
  }
  if (!!!inclination && inclination!==0) {
    inclination = 'undefined';
  }
  if (!!!eff) {
    eff = 'undefined';
  }

  console.log("++++++++++++++++++++++++++++++++++");
  console.log([area,inclination,eff]);
  return [area,inclination,eff]
}

function initMap(){
  map = new google.maps.Map(document.getElementById('map'),{
    zoom: startingZoom,
    minZoom: minZoom,
    center: {lat: 46.151377, lng: 14.866069},
    map: map,
    gestureHandling: 'greedy'
  });

  map.overlayMapTypes.insertAt(0, new CoordMapType(new google.maps.Size(256, 256)));

  var cur_zoom = startingZoom;

  zoomChangeListener = google.maps.event.addListener(map,'zoom_changed',function (event) {
    zoomChangeBoundsListener = google.maps.event.addListener(map,'bounds_changed',function (event) {  
      console.log("You changed zoom to " + map.getZoom());
      // $(".popup").hide();
      new_zoom = map.getZoom();

      if (ZoomLevelChanges.includes(new_zoom) && (new_zoom - cur_zoom) > 0) {
        console.log("I'll notify we need new layer at " + new_zoom);
        // $.post("/new_layer",{new_zoom:new_zoom},function(response){
        //   console.log(response);
        // });
      }
      cur_zoom = new_zoom;
      google.maps.event.removeListener(zoomChangeBoundsListener);
    });
  });

  map.addListener('click',function(event) {
    if (infowindows.length) {
      infowindows[0].close();
      infowindows = [];
    }
    var latitude = event.latLng.lat();
    var longitude = event.latLng.lng();
    console.log(event);
    $.post("/get_irradiance", {"lat":latitude,"lng":longitude},function(response,latitude,langitude){
      console.log(response);
      data = JSON.parse(response);
      // $(".popup").css( {position:"absolute", top:event.Ia.screenY, left: event.Ia.screenX});
      // $(".popup").show();
      // console.log(event.Ia.screenY);
      // var popup = document.getElementById("myPopup");
      // $("#myPopup").html("Area: " + data['irradiance']);
      // popup.classList.toggle("show");

      if (parseFloat(data['irradiance']) == -99.0) {
        irradiance = getData(data['lat'],data['lng'],1);
        var content = "Average yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub>";
      }
      else {
        sArea = data['irradiance'];
        efficiency = 0.15;
        inclin = 1.0;
        a = getDataFromFields();
        area = a[0];
        inclination = (Math.PI/180)*a[1];
        eff = a[2];

        if (area != 'undefined') {
          sArea = area;
        }
        if (eff != 'undefined') {
          efficiency = eff;
        }
        if (inclination != 'undefined') {
          inclin = 1.0/Math.cos(inclination);
        }

        irradiance = getData(data['lat'],data['lng'],1);
        var energy = parseInt(inclin * efficiency * irradiance * parseFloat(data['irradiance']));
        var content = "Expected yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub><br>Roof surface area: " + parseInt(data['irradiance']) + " m<sup>2</sup><br>Expected yearly energy production: " + energy + " kWh";

        document.getElementById("roof-SA").value = parseInt(data['irradiance']);

      localStorage.setItem("irradiance",irradiance);
      localStorage.setItem("inclin",inclin);
      localStorage.setItem("eff",efficiency);
      localStorage.setItem("SA",sArea);

        //var building = JSON.parse(data['mainBuilding']);
        // console.log("hez");
        // console.log(data['mainBuilding']);
        // //console.log(data['mainBuilding'].replace(/\'/g, '/'));
        // //var building = JSON.parse(data['mainBuilding'].replace(/\'/g, '/'));
        // var building = data['mainBuilding'];

        // console.log(building);

        // var house = new google.maps.Polygon({
        //   paths: building,
        //   strokeColor: '#FF0000',
        //   strokeOpacity: 0.8,
        //   strokeWeight: 2,
        //   fillColor: '#FF0000',
        //   fillOpacity: 0.35
        // });
        // house.setMap(map);
      }

      var infowindow = new google.maps.InfoWindow({
          content: content,
          //position: latLng
        });

      infowindow.setPosition({lat: data['lat'], lng: data['lng']});
      infowindow.open(map);
      infowindows.push(infowindow);

    });
  });
}

$("#address_input").keydown(function(t){
    if (t.which == 13) {
        var message = $("#address").val();

        if (message == "") {
            return
        }
        if (!message.replace(/\s/g, '').length) {
            return
        }

        document.getElementById("address").value =  "";
        getIrradiance()
      
    }
});

$("#address").keydown(function(t){
  if (t.which == 13) {
    getIrradiance();
  }
});

$("#submit_btn").click(function(){
  getIrradiance();
})

function getIrradiance() {
  if (infowindows.length) {
      console.log("closin infowindow");
      infowindows[0].close();
      infowindows = [];
    }
  var message = $("#address").val();

  if (message == "") {
      return
  }
  if (!message.replace(/\s/g, '').length) {
      return
  }

  document.getElementById("address").value =  "";

  $.post("/get_irradiance", {"address":message},function(response){
    console.log(response);
    data = JSON.parse(response);

    element = document.getElementById("map");
    var rect = element.getBoundingClientRect();
    console.log(rect.top, rect.right, rect.bottom, rect.left);

    var latLng = new google.maps.LatLng(data['lat'], data['lng']);
    // var projection = map.getProjection();
    // var bounds = map.getBounds();
    // var topRight = projection.fromLatLngToPoint(bounds.getNorthEast());
    // var bottomLeft = projection.fromLatLngToPoint(bounds.getSouthWest());
    // var scale = Math.pow(2, map.getZoom());
    // var worldPoint = projection.fromLatLngToPoint(latLng);
    // posX = Math.floor((worldPoint.y - topRight.y) * scale);
    // posY = Math.floor((worldPoint.x - bottomLeft.x) * scale);
    // console.log(posX,posY);

    map.setCenter(latLng);
    map.setZoom(19);

    //console.log(type(data['irradiance']))

    if (parseFloat(data['irradiance']) == -99.0) {
      irradiance = getData(data['lat'],data['lng'],1);
      var content = "Average yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub>"
    }
    else {
      sArea = data['irradiance'];
      efficiency = 0.15;
      inclin = 1.0
      a = getDataFromFields();
      area = a[0];
      inclination = (Math.PI/180)*a[1];
      eff = a[2];

      if (area != 'undefined') {
        sArea = area;
      }
      if (eff != 'undefined') {
        efficiency = eff;
      }
      if (inclination != 'undefined') {
        inclin = 1.0/Math.cos(inclination);
      }

      irradiance = getData(data['lat'],data['lng'],1);
      var energy = parseInt(inclin * efficiency * irradiance * parseFloat(sArea));
      var content = "Expected yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub><br>Roof surface area: " + parseInt(data['irradiance']) + "m<sup>2</sup><br>Expected yearly energy production: " + energy + " kWh"

      localStorage.setItem("irradiance",irradiance);
      localStorage.setItem("inclin",inclin);
      localStorage.setItem("eff",efficiency);
      localStorage.setItem("SA",sArea);


      document.getElementById("roof-SA").value = parseInt(data['irradiance']);
      //var building = JSON.parse(data['mainBuilding']);
      // console.log("hez2");
      // console.log(data['mainBuilding']);
      // //var building = JSON.parse(data['mainBuilding'].replace(/\'/g, '/'));
      // var building = data['mainBuilding']

      // var house = new google.maps.Polygon({
      //   paths: building,
      //   strokeColor: '#FF0000',
      //   strokeOpacity: 0.8,
      //   strokeWeight: 2,
      //   fillColor: '#FF0000',
      //   fillOpacity: 0.35
      // });
      // house.setMap(map);
    }

    var infowindow = new google.maps.InfoWindow({
        content: content,
        //position: latLng
      });

    infowindow.setPosition({lat: latLng.lat(), lng: latLng.lng()});
    infowindow.open(map);
    infowindows.push(infowindow);
    
  });
}

function point2LatLng(point, map) {
  var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
  var bottomLeft = map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest());
  var scale = Math.pow(2, map.getZoom());
  var worldPoint = new google.maps.Point(point.x / scale + bottomLeft.x, point.y / scale + topRight.y);
  return map.getProjection().fromPointToLatLng(worldPoint);
}

        // for (var i = 0; i < building.length; i++) {
        //   console.log(building[i][0] + " and " + building[i][1]);
        //   lat = point2LatLng(new google.maps.Point(building[i][0],building[i][1]),map).lat();
        //   lng = point2LatLng(new google.maps.Point(building[i][0],building[i][1]),map).lng();
        //   buildingCoordinates.push({lat: lat, lng: lng});
        // }

$("#roof-SA").keydown(function(t){
  if (t.which == 13) {
    var val = parseFloat(this.value);
    console.log(val);

    if (infowindows) {
      position =  infowindows[0].getPosition();

      console.log(position);
      console.log(position.lat());

      irradiance = localStorage.getItem("irradiance");
      inclin = localStorage.getItem("inclin");
      eff = localStorage.getItem("eff");

      localStorage.setItem("SA",val);

      var energy = parseInt(inclin * eff * irradiance * parseFloat(val));

      var content = "Expected yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub><br>Roof surface area: " + parseInt(val) + "m<sup>2</sup><br>Expected yearly energy production: " + energy + " kWh"

      infowindows[0].close();
      infowindows = [];

      var infowindow = new google.maps.InfoWindow({
          content: content,
          //position: latLng
        });

      infowindow.setPosition({lat: position.lat(), lng: position.lng()});
      infowindow.open(map);
      infowindows.push(infowindow);


    }
    else {
      return
    }
  }
});

$("#roof-I").keydown(function(t){
  if (t.which == 13) {
    var val = parseFloat(this.value);
    console.log(val);

    if (infowindows) {
      position =  infowindows[0].getPosition();

      console.log(position);
      console.log(position.lat());

      irradiance = localStorage.getItem("irradiance");
      eff = localStorage.getItem("eff");
      SA = localStorage.getItem("SA");

      localStorage.setItem("inclin",val);

      val = 1.0/Math.cos((Math.PI/180)*val);


      var energy = parseInt(parseFloat(val) * eff * irradiance * SA);

      var content = "Expected yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub><br>Roof surface area: " + parseInt(SA) + "m<sup>2</sup><br>Expected yearly energy production: " + energy + " kWh"

      infowindows[0].close();
      infowindows = [];

      var infowindow = new google.maps.InfoWindow({
          content: content,
          //position: latLng
        });

      infowindow.setPosition({lat: position.lat(), lng: position.lng()});
      infowindow.open(map);
      infowindows.push(infowindow);


    }
    else {
      return
    }
  }
});

$("#eff").keydown(function(t){
  if (t.which == 13) {
    var val = parseFloat(this.value);
    console.log(val);

    if (infowindows) {
      position =  infowindows[0].getPosition();

      console.log(position);
      console.log(position.lat());

      irradiance = localStorage.getItem("irradiance");
      SA = localStorage.getItem("SA");
      inclin = localStorage.getItem("inclin");

      localStorage.setItem("eff",val);
      
      console.log();
      var energy = parseInt(SA * inclin * irradiance * parseFloat(val));

      var content = "Expected yearly solar irradiance: " + irradiance + " <sup>kWh</sup>&frasl;<sub>m<sup>2</sup> year</sub><br>Roof surface area: " + parseInt(SA) + "m<sup>2</sup><br>Expected yearly energy production: " + energy + " kWh"

      infowindows[0].close();
      infowindows = [];

      var infowindow = new google.maps.InfoWindow({
          content: content,
          //position: latLng
        });

      infowindow.setPosition({lat: position.lat(), lng: position.lng()});
      infowindow.open(map);
      infowindows.push(infowindow);


    }
    else {
      return
    }
  }
});