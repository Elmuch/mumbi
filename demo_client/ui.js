
(function($){
	$('#read-ndef').click(function(event) {
		$('#write-template').hide();
	  $('#read-template').fadeIn(1000);
		
		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/read'})
		
		req.done(function(data){
			data = JSON.parse(data);
				$tbl = $('<table/>',{
					'class':"table stripped"
				})
			console.log(data)
			for (var i = 0; i < data.length; i++) {
				$tr = $('<tr/>')
				$tr.append($('<td/>',{
					"text": data[i].name,
					"class":'data-key'
				}),$('<td/>',{
					"text":data[i].data,
					"class": "data-val"
				}))
				$tbl.append($tr)
			}
			$('#user-data').append($tbl)
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
				// data: JSON.stringify(sample_data),
		 		data: JSON.stringify({
		 			date: (function(){
		 				var date = new Date()
		 				$('#date').val(date.toLocaleString());
		 				return date.toLocaleString()
		 			})(), 
		 			tra_id: $('#tra-id').val(),
		 			tra_valuesubsidy: $('#tra_valuesubsidy').val(),
		 			tra_fieldwork_use_id: $('#tra_fieldwork_use_id').val()
		 		}),
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