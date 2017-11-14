var areaLat = 0.0;
var areaLng = 0.0;
var map;
var zoomLevel;
var markers = [];

function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: {
			lat: 36.381404,//36.769876,
			lng: 128.004450//126.931744
		}, //페이지 로딩시의 위치, Geolocation 값
		zoom: 7, //지도 확대/축소 수준, 한스텝에 1씩, 1:세계, 5:대륙, 10:시/군/구, 15:도로, 20:건물
		mapTypeControl: false,
		fullscreenControl: false,
		maxZoom: 10,
		minZoom: 7
	});

	//marker, marker 1로 차트 처럼 표시!
	google.maps.event.addListener(map, 'zoom_changed', function() {
		zoomLevel = map.getZoom();
		console.log(zoomLevel);
		switch( zoomLevel ){
			case 10:
				cityMarker(12, 12);
			case 9:
				cityMarker(9.5, 8.5);
				break;
			case 8:
				map.setCenter({lat:36.381404, lng:128.004450});
				provinceMarker(16, 4);
				break;
			case 7:
				map.setCenter({lat:36.381404, lng:128.004450});
				provinceMarker(12, 3);
				break;
		}
	});
}

function setMapOnAll(map) {
	for(var i = 0; i < markers.length; i++){
		markers[i].setMap(map);
	}
}

function provinceMarker(markSize, fontSize){
	jQuery.ajax({
		type: "GET",
		url: "/province",
		success: function(data){
			setMapOnAll(null);
			markers = [];
			for(var i = 0; i < data.length; i++){
				var pos = data[i].prov_pos.hits.hits[0]._source.prov_pos;
      	areaLat = pos.lat;
				areaLng = pos.lon;
				var tmpMark = new google.maps.Marker({
					position: {lat: areaLat, lng: areaLng},
					icon: {
						path: google.maps.SymbolPath.CIRCLE,
						scale: Math.log(data[i].sum_cnt.value) * markSize,
						fillColor: getRandomColor(),
						fillOpacity: .75,
						strokeColor: 'white',
						strokeWeight: .5
					},
					label: {
						color: 'white',
						fontSize: (Math.log(data[i].sum_cnt.value)*fontSize) + 'pt',
						fontWeight: 'bold',
						text: data[i].key+"("+data[i].sum_cnt.value+")"
					},
					map:map
				});
				tmpMark.addListener('click', function() {
					pos =	this.getPosition();
					map.setCenter(pos);
					map.setZoom(9);
				});
				markers.push(tmpMark);
			}
		}
	});
}

function focusToKey(key){
	var Lat, cLng;
  if( ($("#key").val() != "") && (data[i].key.indexOf($("#key").val()) > -1) ){
		cLat = areaLat;
		cLng = areaLng;
		map.setCenter( {lat: cLat, lng: cLng} );
	}
}
var infowindows = [];
function cityMarker(markSize, fontSize){
	jQuery.ajax({
		type: "GET",
		url: "/city",
		success: function(data){
			setMapOnAll(null);
			markers = [];
			for(var i = 0; i < data.length; i++){
				var pos = data[i]._source.city_pos;
				areaLat = pos.lat;
				areaLng = pos.lon;

				var contentString = '<div id="content">'+
                   '<h4 id="firstHeading" class="firstHeading">'+data[i]._source.province+' '+data[i]._source.city+'</h1>'+
				           '<div id="bodyContent">'+
						       '<p>Reference count: '+data[i]._source.count+'</p>'+
						       '<p>Geo-position: '+data[i]._source.city_pos.lat+' '+data[i]._source.city_pos.lon+'</p>'+
						       '</div>'+
						       '</div>';

				var infoWindow = new google.maps.InfoWindow({ content: contentString });

				var tmpMark = new google.maps.Marker({
					position: {lat: areaLat, lng: areaLng},
					title: ""+data[i]._source.city,
					icon: {
						path: google.maps.SymbolPath.CIRCLE,
						scale: Math.log(data[i]._source.count*10) * markSize,
						fillColor: getRandomColor(),
						fillOpacity: .75,
						strokeColor: 'white',
						strokeWeight: .5
					},
					label: {
						color: 'white',
						fontSize: (Math.log(data[i]._source.count*10)*fontSize) + 'pt',
						fontWeight: 'blod',
						text: data[i]._source.count+""
					},
					infowindow: infoWindow,
					map: map
				});


				tmpMark.addListener('mouseover', function() {
					this.infowindow.open(map, this);
				});
				tmpMark.addListener('mouseout', function() {
					this.infowindow.close();
				});
				tmpMark.addListener('click', function() {
					citySearch(this.getTitle());
				});
				markers.push(tmpMark);
			}
		}
	});
}

function citySearch(name){
	if(name.length <= 4){
		name = name.substring(0, name.length-1);
	} else {
		name = name.substring(0, name.length-3);
	}
	jQuery.ajax({
		type: "GET",
		url: "/search/"+name,
		success: function(data){
			posts = data.posts;
			console.log(posts);
			$('.list-group').empty();				
			for(var i = 0; i < posts.length; i++){
				source = posts[i]._source;
				var item = '<div class="list-group-item">'+
						'<a href="'+source.url+'" target="_blank">'+
						'<div class="list-header">'+
						'<img class="img-responsive img-circle" src="'+source.img+'" width="32px" height="32px">'+
						'<span>'+source.author+'</span>'+
						'</div>'+
						'<div class="list-body">'+
						'<h4 class="heading"><strong>'+source.title+'</strong></h4>'+
						'<p class="desc">'+source.desc.substring(0, 80)+'</p>'+
						'</div>'+
						'</a>'+
						'</div>'+'<hr style="color:lightgray"/>'
				$('.list-group').append(item);
			}
			city = data.city[0];
			cityLat = city._source.city_pos.lat;
			cityLng = city._source.city_pos.lon;
			map.setZoom(10);
			map.setCenter({lat: cityLat, lng: cityLng});
		}
	});
}
