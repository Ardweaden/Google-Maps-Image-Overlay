var ZoomLevelChanges = [5,10];
var startingZoom = 0;
//var overlayMapTypes = [];

function initMap(){
  map = new google.maps.Map(document.getElementById('map'),{
    zoom: startingZoom,
    center: {lat: 0.0, lng: 0.0},
    map: map,
    gestureHandling: 'greedy',
  });

  var cur_zoom = startingZoom;

  zoomChangeListener = google.maps.event.addListener(map,'zoom_changed',function (event) {
    zoomChangeBoundsListener = google.maps.event.addListener(map,'bounds_changed',function (event) {  
      console.log("You changed zoom to " + map.getZoom());
      new_zoom = map.getZoom();

      if (ZoomLevelChanges.includes(new_zoom) && (new_zoom - cur_zoom) > 0) {
        console.log("I'll notify we need a finer layer at " + new_zoom);
      }
      else if (ZoomLevelChanges.includes(new_zoom) && (new_zoom - cur_zoom) < 0) {
        console.log("I'll notify we need a cruder layer at " + new_zoom);
      }
      cur_zoom = new_zoom;
      google.maps.event.removeListener(zoomChangeBoundsListener);
    });
  });

  var imageMapType = new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {
      console.log(zoom);
      console.log(coord.x);
      return ['images/test0/',zoom,'_',coord.y,'_',coord.x,'.jpg'].join('')
    },
    tileSize: new google.maps.Size(256,256)
  });

  map.overlayMapTypes.push(imageMapType);
  imageMapType.setOpacity(0.5);
  //map.overlayMapTypes[0].setOpacity(.25);

}


