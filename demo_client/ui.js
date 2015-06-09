
(function($){
	$('#read-ndef').click(function(event) {
		$('#write-template').hide();
	  $('#read-template').fadeIn(1000);
		console.log("hello")
		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/read'})
		req.done(function(data){
			console.log(data)
		})

		req.fail(function(){
			$('#logContainter').append('Sorry Something went wrong')
		})
	});

	$('form').submit(function(event) {
		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/write',
							type: "POST",
							contentType: 'application/json',
						 		data: JSON.stringify([{
              	name: 'elijah',
              	id: '343434'
            		}]),
            		dataType: 'json'
							});


		req.done(function(data){
			console.log(data)
		})
		req.fail(function(xhr){
			console.log('error'+xhr)
		})
		return false;
	});

	$('#write-tab').click(function(event){
	  $('#read-template').hide()
	  $('#write-template').fadeIn(1000);
	})

	$('.clear-logs').click(function(event){
	  $('pre').fadeOut(600)
	})	
	
})(jQuery)