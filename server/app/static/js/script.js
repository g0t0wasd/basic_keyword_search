var search_url = "http://127.0.0.1:5000/api/search/";
var details_url = "http://127.0.0.1:5000/api/details/"

var pager;
var numItemsOnPage = 10;

paginate = function(){
    pager = new Pager('results', numItemsOnPage); 
    pager.init(); 
    pager.showPageNav('pager', 'paging'); 
    pager.showPage(1);
}


$("#search_button").click(function() {
	var query = $("#text_input").val();
	if (query !== ""){
		$.ajax({
			url: search_url + query,
			success: function(result){
				var results = result["results"];
				var total_time = result["time"];
				var total_results = result["total_results"];
				$("#results").empty();
				if (results.length > 0){
					$("#messages").text("Search time " + total_time + " seconds. Total results: " + total_results);
					$("#results").append($("<thead><th>Book ID</th><th>Title</th><th>Score</th></thead><tbody></tbody>"));
					for (var i = 0; i < results.length; i++) {
						var result_render = $("<tr class='book_row'><td class='book_id_column' onclick='get_details(this);'>" + results[i][0] + "</td><td>" + results[i][1] + "</td><td>" + results[i][2] + "</td></tr><tr><td></td><td><span>" + results[i][3] + "</span> <strike>" + results[i][4] + "</strike></td></tr>");
						$("#results tbody").append(result_render);
					}
					paginate();
				} else {
					$("#messages").text("");
					$("#results").append($("<tr><td> For your query there were no results </td></tr>"));
				}
			},
			fail: function(){
				$("#messages").text("Failed to get url response!");
			},
			error: function(){
				$("#messages").text("Backend error occured!");
			}
		});
	} else {
		$("#messages").text("Empty query!");
	}
});


get_details = function(e){
	var book_id = $(e).text();
	$.ajax({
		url: details_url + book_id,
		success: function(result){
			data = result["details"];
			$("#modal").show();
			$("#book_id").text(book_id);
			$("#book_title").text(data[0]);
			$("#book_category").text(data[2]);
		},
		fail: function(){
			alert("Fail");
		}
	})
}

$(".close").click(function() {
	$("#modal").hide();	
});