var mymap = null;

initMap();


function initMap() {
	this.mymap = L.map('mapid', { zoomControl: false }).setView([parseFloat($('#user_latUb').val()), parseFloat($('#user_lngUb').val())], 13);
	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(mymap);

	L.circle([parseFloat($('#user_latUb').val()), parseFloat($('#user_lngUb').val())], 2000)
	.setLatLng([parseFloat($('#user_latUb').val()), parseFloat($('#user_lngUb').val())])
	.bindPopup("El usuario está aquí con 2 kilometros de aproximacion")
	.openPopup()
	.addTo(mymap);
}