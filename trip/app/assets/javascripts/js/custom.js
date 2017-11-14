function getRandomColor() {
	var letters = '0123456789ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++ ) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

function searchForm(){
	var key = document.getElementById('key').value;
	if(key != null){
		citySearch(key);
	}
}

$(document).ready(function() {

	initMap();
	provinceMarker(12, 3);

	var center = $(window).width()/2;
	$(window).resize(function() {
		if(this.resizeTO) {
			clearTimeout(this.resizeTO);
		}
		this.resizeTO = setTimeout(function() {
			$(this).trigger('resizeEnd');
		}, 500);
	});

	$(window).on('resizeEnd', function() {
		var x = $(window).width() /2;
		console.log(x + ", "+center);
		var dist = center -	x;
		map.panBy(dist, 0);
		center = $(window).width() /2;
	});

	$(function() {
		$('#fh5co-subscribe').on("submit", function(e) {
			e.preventDefault();

			searchForm();
		});
	});
});
