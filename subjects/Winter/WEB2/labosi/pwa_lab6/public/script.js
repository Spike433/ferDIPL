
const base32 = '0123456789bcdefghjkmnpqrstuvwxyz'; // (geohash-specific) Base32 map

function encode(lat, lon, precision) {
    // infer precision?
    if (typeof precision == 'undefined') {
        // refine geohash until it matches precision of supplied lat/lon
        for (let p=1; p<=12; p++) {
            const hash = Geohash.encode(lat, lon, p);
            const posn = Geohash.decode(hash);
            if (posn.lat==lat && posn.lon==lon) return hash;
        }
        precision = 12; // set to maximum
    }

    lat = Number(lat);
    lon = Number(lon);
    precision = Number(precision);

    if (isNaN(lat) || isNaN(lon) || isNaN(precision)) throw new Error('Invalid geohash');

    let idx = 0; // index into base32 map
    let bit = 0; // each char holds 5 bits
    let evenBit = true;
    let geohash = '';

    let latMin =  -90, latMax =  90;
    let lonMin = -180, lonMax = 180;

    while (geohash.length < precision) {
        if (evenBit) {
            // bisect E-W longitude
            const lonMid = (lonMin + lonMax) / 2;
            if (lon >= lonMid) {
                idx = idx*2 + 1;
                lonMin = lonMid;
            } else {
                idx = idx*2;
                lonMax = lonMid;
            }
        } else {
            // bisect N-S latitude
            const latMid = (latMin + latMax) / 2;
            if (lat >= latMid) {
                idx = idx*2 + 1;
                latMin = latMid;
            } else {
                idx = idx*2;
                latMax = latMid;
            }
        }
        evenBit = !evenBit;

        if (++bit == 5) {
            // 5 bits gives us a character: append it and start over
            geohash += base32.charAt(idx);
            bit = 0;
            idx = 0;
        }
    }

    return geohash;
}


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        var x = document.getElementById("location");
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}
function showPosition(position) {
    var x = document.getElementById("location");
    x.innerHTML = "Vaša lokacija:<br> zemljopisna širina: " + position.coords.latitude + "<br>zemljopisna dužina: " + position.coords.longitude;

    var latlon = position.coords.latitude + "," + position.coords.longitude;

    $.ajax({
        type:"GET",
        url:"https://app.ticketmaster.com/discovery/v2/events.json?" +
            "apikey=wl6cQfbqRGGfnvnWIUIG6OtkZ1AytTeH" +
            "&size=5" +
            "&latlong="+latlon +
            "&sort=distance,date,asc",
        async:true,
        dataType: "json",
        success: function(json) {
            console.log(json);
            var e = document.getElementById("events");
            e.innerHTML = "Pronađeno: " + json._embedded.events.length + " događaja.";
            showEvents(json);
            initMap(position, json);
        },
        error: function(xhr, status, err) {
            console.log(err);
        }
    });

}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    }
}


function showEvents(json) {
    for(var i=0; i<json.page.size; i++) {
        $("#events").append("<p>"+json._embedded.events[i].name+"</p>");
    }
}


function initMap(position, json) {
    var mapDiv = document.getElementById('map');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: position.coords.latitude, lng: position.coords.longitude},
        zoom: 6
    });

    var marker_dict = {}
    for(var i=0; i<json.page.size; i++) {
        var location_string = `${json._embedded.events[i]._embedded.venues[0].location.latitude},${json._embedded.events[i]._embedded.venues[0].location.longitude}`
        if(location_string in marker_dict) {
            marker_dict[location_string].push(json._embedded.events[i].name)
        } else {
            marker_dict[location_string] = [json._embedded.events[i].name]
        }
    }
    console.log(marker_dict)
    for (var location_ in marker_dict) {
        addMarker(map, location_, marker_dict[location_]);
    }
}

function addMarker(map, location_, events_array) {

    var events_string = ""
    for (var event_ in events_array) {
        events_string += `${events_array[event_]}<br>`
    }

    var infowindow =  new google.maps.InfoWindow({
        content: events_string,
        map: map
    });

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(location_.split(",")[0], location_.split(",")[1]),
        map: map
    });
    marker.addListener('mouseover', function() {
        infowindow.open(map, this);
    });

// assuming you also want to hide the infowindow when user mouses-out
    marker.addListener('mouseout', function() {
        infowindow.close();
    });
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
    console.log(marker);
}


getLocation();
