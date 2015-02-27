
var map = null;
var marker = null;
var positionLatLng = null;

var x = document.getElementById("demo");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude + 
    "<br>Longitude: " + position.coords.longitude + 
    "<br>Time: " + new Date();


    positionLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

	centerMap();

    setTimeout(getLocation, 15 * 1000);
}

function centerMap() {
	var position = positionLatLng;
	if (!map) {
		var mapOptions = {
			center: position,
			zoom: 13
    	};

		map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
		marker = new google.maps.Marker({
	    position: map.getCenter(),
	    icon: {
	      path: google.maps.SymbolPath.CIRCLE,
	      scale: 10
	    },
	    draggable: true,
	    map: map
	  });	
	}

	marker.setPosition(position);
	map.setCenter(position);
}

getLocation();

$( window ).resize(function() {
	if (positionLatLng) {
		setTimeout(centerMap, 100);
	}
});