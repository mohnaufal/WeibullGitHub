$("#hitung_reliability").click(function(){
	var  data_reliability = {
		"loc" : $("#loc").val(),
		"shape" : $("#shape").val(),
		"scale" : $("#scale").val(),
		"tfail" : $("#tfail").val()
	}

	$.post( "/relia", data_reliability, function(data){
		$("#reliability").val(data);
	});
});

$("#hitung_reliablelife").click(function(){
	var  data_reliablelife = {
		"loc" : $("#loc").val(),
		"shape" : $("#shape").val(),
		"scale" : $("#scale").val(),
		"reliability" : $("#reliability").val()
	}

	$.post( "/relia?inv=1" , data_reliablelife, function(data){
		$("#tfail").val(data);
	});
});