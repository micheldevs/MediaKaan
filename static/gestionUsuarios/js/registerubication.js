var mymap = null;
var marker = null;

initMap();
mymap.on('locationfound', onLocationFound);
mymap.on('locationerror', onLocationError);
mymap.on('click', onMapClick);

function initMap() {
	this.mymap = L.map('mapid').setView([40.4165000, -3.7025600], 13);
	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(mymap);
}

function onLocationFound(e) {
	var radius = e.accuracy / 2;
	$('#id_latUb').val(e.latlng.lat);
	$('#id_lngUb').val(e.latlng.lng);
	if(this.marker == null) {
		this.marker = L.marker(e.latlng).addTo(mymap)
		.bindPopup("Estás aquí, con " + radius + " metros de aproximacion").openPopup();
	} else {
		this.marker
		.setLatLng(e.latlng)
		.bindPopup("Estás aquí, con " + radius + " metros de aproximacion")
		.openPopup()
		.openOn(mymap);
	}

}

function onLocationError(e) {
	alert("¡Debe permitir encontrar ubicación para establecerla!");
}

function locateUser() {
	this.mymap.locate({ setView: true });
}

function onMapClick(e) {
	$('#id_latUb').val(e.latlng.lat);
	$('#id_lngUb').val(e.latlng.lng);
	this.marker
		.setLatLng(e.latlng)
		.bindPopup("La ubicación establecida tiene una latitud de: " + e.latlng.lat.toString() + " y una longitud de: " + e.latlng.lng.toString())
		.openPopup()
		.openOn(mymap);
	circle.setLatLng(e.latlng, radius).addTo(mymap);
}