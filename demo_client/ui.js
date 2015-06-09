
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
		var sample_data = {
			"tra_id":1,
		  "tra_pro_id":1,
		  "tra_ter_id":1,
		  "tra_sta_id":15,
		  "tra_ins_id":2,
		  "tra_geo4_id":158,
		  "tra_trarepenr_id":1506,
		  "tra_houmemenr_id":14266,
		  "tra_haschangedgeolocation":0,
		  "tra_number":1,
		  "tra_accountnumber":"",
		  "tra_flagcollected":1,
		  "tra_consecutiveunclaimed":0,
		  "tra_valuesubsidy":10000.0,
		  "tra_valuearrears":0.0,
		  "tra_valuearrearsenrolment":0.0,
		  "tra_valuetotal":10000.0,
		  "tra_istransferfieldwork":0,
		  "tra_datefieldwork":"",
		  "tra_fieldwork_use_id":0
		}
		
		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/write',
			type: "POST",
			contentType: 'application/json',
		 		data: JSON.stringify(sample_data),
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