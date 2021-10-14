/*var consulta = $("#searchTable").DataTable();

$("#inputBusqueda").keyup(function(){
	consulta.search($(this).val()).draw();

	$("header").css({
		"height": "100vh",
		"background": "rgba(0,0,0,0.5)"
	})

	if ($("#inputBusqueda").val() == ""){
		$("header").css({
			"height": "auto",
			"background": "none"
		})

		$("#search").hide()

	} else {
		$("#search").fadeIn("fast");
	}
})*/

$(function () {
    $.get('./part-r-00000.txt', function (data) {
       words = data.split('\s');
       console.log(words);
    });
});
