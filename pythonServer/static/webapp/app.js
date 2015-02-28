
var map = null;
var marker = null;
var positionLatLng = null;

var updateTimeout = null;

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function getMoreTracks() {
	//just use the input text for now ...
	addArtists($('[name=artist-list]').val());
}

function addArtists(artist_list) {
	if (!artist_list)
		return;

	if (artist_list) {
		artist_list = artist_list.replace(/\;\,/g, ",").replace(/\s*\,\s*/g, ",").replace(/(^\s*|\s*$)/g, "").replace(/\s+/g, "+");
		artists = artist_list.split(",");

		_.each(artists, function(artist_query, k) {
			if (!artist_query) return;
			$.get("https://api.spotify.com/v1/search", { q: artist_query, type: "artist", limit:1 })
			.done(function(data) {
				var artist = _.first(data.artists.items);
				if (!artist) {
					console.log("Failed to get data for", artist_query)
				}
				else {
					$.get("https://api.spotify.com/v1/artists/" + artist.id + "/top-tracks", {country: "SE"})
					.done(function(data) {
						_.each(data.tracks, function(track) {
							track.artist = artist;
							addTrack(track);
						});
					})
					.error(function() {
						alert("Failed to get tracks for " + artist.name);
					});
				}
			})
			.error(function() {
				alert("Failed to get artist data");
			});
		})
		
	}
}

function setCurrentlyPlaying(track, album, artist) {
	var currentlyPlaying =  track + " - " + artist;
	$(".currently-playing").text(currentlyPlaying);
	document.title = "\u25b6 " + currentlyPlaying;
}

function renderTrack(track) {
	
	//artist-info background
	//artist-name name
	var img = _.first(track.artist.images);
	$(".artist-info").css({backgroundImage: "url(" +  (img? img.url : '') + ")"});
	$(".artist-name").text(track.artist.name);

	//track-info background
	//album-info album text
	//track-name name
	var img = _.first(track.album.images);
	$(".track-info").css({backgroundImage: "url(" + (img? img.url : '') + ")"});
	$(".album-info").text(track.album.name);	
	$(".track-name").text(track.name);


	setCurrentlyPlaying(track.name, track.album.name, track.artist.name)


	//Set audio!
	$('audio').prop("src", track.preview_url);
	$('audio')[0].play();
}

function nextTrack() {
	var track = allTracks.shift();

	if (!track) {
		getMoreTracks();
	} else {
		updateTrackList();
		renderTrack(track);

		if (allTracks.length == 0)
			getMoreTracks();
	}
}

function showPosition(position) {

	setPosition(new google.maps.LatLng(position.coords.latitude, position.coords.longitude), true);

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

	if (pendingRequestTimer) {
		clearTimeout(pendingRequestTimer);
		pendingRequestTimer = null;
	}

	pendingRequestTimer = setTimeout(function() {
		$.get("http://192.168.137.117:8000/location/lat/" + position.lat() + "/long/" + position.lng() + "/", null, "application/json")
		.done(function(d) {
			var artistList = _.map(d.result, function(v) { return v.artist}).join(",");
			$('[name=artist-list]').val(artistList);

			if (isPlayerIdle())
				getMoreTracks();
		});
	}, 400);

	if (isPlayerIdle()) {
		getMoreTracks();
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

	return allTracks.length == 0 && trackPaused;
}

var allTracks = [];

function addTrack(track) {
	/*
		Keep some tracks in the queue
		//just log for now ...
	*/

	var wasIdle = isPlayerIdle();

	track.timestamp = new Date();
	allTracks.push(track);

	while (allTracks.length > 10) {
		allTracks = _.shuffle(allTracks);
		allTracks.shift();
	}

	if (wasIdle) {
		nextTrack();
	}

	updateTrackList();
}

function updateTrackList() {
	$('.playlist-entries').empty();
	_.each(allTracks, function(track) {
		$('.playlist-entries').append($("<li>").text(track.name));	
	});
}

$('body').on("click", ".resume-following", function() {
	$('body').attr('data-location-state', "following");
	getLocation();
});

$('body').on("click", ".skip", function(e) {
	nextTrack();
});

$('body').on("submit", ".artist-lookup", function(e) {
	e.preventDefault();
	var artist_list = $(this).find('[name=artist-list]').val();
	addArtists(artist_list);
});

$("audio").on("error ended", function() {
	nextTrack();
});

$( window ).resize(function() {
	if (positionLatLng) {
		setTimeout(centerMap, 100);
	}
});