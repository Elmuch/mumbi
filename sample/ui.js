
(function($){
	
	// Detect reader
	$(document).ready(function(){
		function deviceInfo(device){
			// A lot more readers are supported
			// Only ACR122U have been tested

			var compatibleDevices = [
			  {
			    deviceName: 'ACR122U PICC Interface',
			    productId: 0x2200,
			    vendorId: 0x072f,
			    thumbnailURL: 'images/acr122u.png'
			  },
			  {
			    deviceName: 'SCL3711 Contactless USB Smart Card Reader',
			    productId: 0x5591,
			    vendorId: 0x04e6,
			    thumbnailURL: 'images/scl3711.png'
			  }
			],
			deviceInfo = null;

			for (var i = 0; i < compatibleDevices.length; i++)
		    if (device.name === compatibleDevices[i].deviceName){
		      deviceInfo = compatibleDevices[i];
		    }
		    
		  if (!deviceInfo)
		    return;
		  
		  var thumbnail = document.querySelector('#device-thumbnail');
		  thumbnail.src = deviceInfo.thumbnailURL;
		  thumbnail.classList.remove('hidden');
		  
		  var deviceName = document.querySelector('#device-name');
		  deviceName.textContent = deviceInfo.deviceName;
		  
		  var productId = document.querySelector('#device-product-id');
		  productId.textContent = deviceInfo.productId;
		  
		  var vendorId = document.querySelector('#device-vendor-id');
		  vendorId.textContent = deviceInfo.vendorId;
			
			log("Card Reader Found",'text-success')
		}

		$.ajax({
			url: 'http://127.0.0.1:5000/'
		})

		.done(deviceInfo)
		.fail(function(jqxhr) {
			log(jqxhr.responseText,'text-danger')
		})
		
	})
	
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

	function displayData(data){
		log('Tag(s) Found',"text-success")
		console.log(data)

		$imgWrapper = $('<div/>',{
			'class': 'image-wrapper'
		})

		$tbl = $('<table/>',{
			'class':"table table-striped"
		});

		$img = $("<img>",{
			'class':'avatar'
		});

		for (var i = 0; i < data.length; i++) {
			if(data[i].name === 'photo') {
				$img.attr('src',data[i].data)
			}else{
				$img.attr('src', 'images/placeholder.png');
			} 

			$('<tr/>').append($('<td/>',{
				"text": data[i].name,
				"class":'data-key'
			}),$('<td/>',{
				"text":data[i].data,
				"class": "data-val"
			})).appendTo($tbl)
		}

		$('#read-template').fadeIn(function() {
			$('.ajax-loader').hide();
			$('#user-data').html($imgWrapper.append($img).add($tbl))
		});
	}

	$('#read-ndef').click(function(event) {
		$('#form-transfer').hide();
	  $('#read-template').fadeIn(1000);

		var req = $.ajax({
			url: 'http://127.0.0.1:5000/card-api/read',
			contentType: false,
      processData: false,
      dataType: 'json'
    })

		$('#user-data').html('Touch a tag <img src="images/loader.gif">')

		req.done(displayData)

		req.fail(function(xhr){
			log(xhr.responseText, "text-danger")
		})
	});

	$('#write-ndef').click(function(event) {
		event.preventDefault()

		var form_data = new FormData($('#form-transfer')[0]);
		$('#form-transfer').hide(function() {
			$('.ajax-loader').show();
		});

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
	
		var req = $.ajax({ 
			url: 'http://127.0.0.1:5000/card-api/write',
			type: "POST",
			data: form_data,
			contentType: false,
      processData: false,
      dataType: 'json'
		});


		req.done(displayData)

		req.fail(function(xhr){
			log(xhr.responseText,"text-success")
		})
		
		return false;
	});

	$('#write-tab').click(function(event){
	  $('#read-template').hide()
	  $('#form-transfer').fadeIn(1000);
	})

	$('.clear-logs').click(function(event){
	  $('pre').fadeOut(600)
	})	
	
})(jQuery)