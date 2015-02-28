
var map = null;
var marker = null;
var positionLatLng = null;

var updateTimeout = null;

var trackCounter = Date.now();

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}


function playTrack(track, spotify) {
	var trackName = spotify.name;
	var artistName = _.first(spotify.artists).name;

	var currentlyPlaying =  trackName + " - " + artistName;
	$(".song-city").text(track.location.name +", " + track.location.countryName);

	//track-info background
	//album-info album text
	//track-name name
	var img = _.first(spotify.album.images);
	$(".song-real-image").css({backgroundImage: "url(" + (img? img.url : '') + ")"});
	$(".artist-name").text(artistName);	
	$(".track-name").text(trackName);


	//Set audio!
	$('audio').prop("src", spotify.preview_url);
	$('audio')[0].play();
}

function nextTrack() {
	trackCounter++;
	
	$.get("http://192.168.137.117:8000/location/lat/" + positionLatLng.lat() + "/long/" + positionLatLng.lng() + "/", null, "application/json")
	.done(function(d) {
		var track = d.result[trackCounter%d.result.length];

		$.get("https://api.spotify.com/v1/tracks/" + track.uri.split(":")[2])
		.done(function(spotify) {
			playTrack(track, spotify);
		})
	});
}

function showPosition(position) {

	setPosition(new google.maps.LatLng(position.coords.latitude, position.coords.longitude), true);

	if (isPlayerIdle())
		nextTrack();

    updateTimeout = setTimeout(getLocation, 15 * 1000);
}

var pendingRequestTimer = null;

function setPosition(position, center) {

	positionLatLng = position;
	
	$("#demo").html("Latitude: " + position.lat() + 
    	"<br>Longitude: " + position.lng() + 
    	"<br>Time: " + new Date()
	);

	if (center) {
		centerMap(); 
	}
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

		marker.addListener('dragstart', function() {
			if (updateTimeout) {
				clearTimeout(updateTimeout);
				updateTimeout = null;
			}
			$('body').attr('data-location-state', "custom");
		});

		marker.addListener('drag', function() {
			positionLatLng = marker.getPosition();

			setPosition(positionLatLng, false);
		});

	}

	marker.setPosition(position);
	map.setCenter(position);
}

getLocation();

function isPlayerIdle() {
	var trackPaused = $("audio")[0].paused || $("audio")[0].src == "http://stream.spc.org:8008/longplayer";

	return trackPaused;
}

$('body').on("click", ".resume-following", function() {
	$('body').attr('data-location-state', "following");
	getLocation();
});

$('body').on("click", ".skip", function(e) {
	nextTrack();
});

$("audio").on("error ended", function() {
	nextTrack();
});

$("body").on("click", ".song-mask, .audio-container, .song-real-image", function(e) {
	e.stopImmediatePropagation();
	e.stopPropagation();
	var inMap = $("body").attr("data-view-mode");

	$("body").attr("data-view-mode", inMap ? "": "map");
});

$("body").on("click", ".song-image", function(e) {
	
	var inMap = $("body").attr("data-view-mode");

	if (!inMap)  {
		e.stopImmediatePropagation();
		e.stopPropagation();

		$("body").attr("data-view-mode", inMap ? "": "map");
	}
});


$( window ).resize(function() {
	if (positionLatLng) {
		setTimeout(centerMap, 100);
	}
});

$("body").on("click", "button", function(e) {
	e.stopImmediatePropagation();
	e.stopPropagation();
	nextTrack();
});