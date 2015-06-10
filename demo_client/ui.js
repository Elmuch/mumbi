
(function($){
	
	function log(message, errorType, object) {
	  $logArea = $('.logs');
	  $pre = $('<pre/>',{
	    "text": message,
	    'class' : errorType
	  })

	  function flash(){
	    $pre.fadeOut(100)
	  }

	 $logArea.append($pre);
	}

	$('#read-ndef').click(function(event) {
		$('#write-template').hide();
	  $('#read-template').fadeIn(1000);
		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/read'})
		var waitNode = 'Please swipe the card <img src="images/loader.gif">'
		$('#user-data').html(waitNode)

		req.done(function(data){
			log('Tag(s) Found',"text-success")
			data = JSON.parse(data);
			$tbl = $('<table/>',{
				'class':"table table-striped"
			});

			console.log(data)

			for (var i = 0; i < data.length; i++) {
				
				if (data[i].name === 'photo'){
					$('#read-template').find('img').attr('src', '../'+data[i].data);
				}else{
					$('#read-template').find('img').attr('src', 'images/placeholder.png')
				}

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
			
			$('#user-data').html($tbl)
		})

		req.fail(function(xhr){
			log(xhr.responseText, "text-danger")
		})
	});

	$('form').submit(function(event) {
		event.preventDefault()

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
		// var formData = new FormData($('form'));
		// debugger;

		var req = $.ajax({ url: 'http://127.0.0.1:5000/card-api/write',
			type: "POST",
			contentType: 'application/json',
				//data: JSON.stringify(sample_data),
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


		req.done(function(xhr){
			log(xhr.responseText,"text-success")
		})

		req.fail(function(xhr){
			log(xhr.responseText,"text-success")
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