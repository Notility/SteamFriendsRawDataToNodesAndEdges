document.addEventListener('DOMContentLoaded', bindGetPlayerSummariesButton);
document.addEventListener('DOMContentLoaded', bindGetFriendListButton);



function bindGetPlayerSummariesButton(){
	document.getElementById('getPlayerSummaries').addEventListener('click', function(event) {
	var homeURL = "http://localhost:3000/getplayersummary/?"
	var userInput = document.getElementById('getPlSummaryInput').value;
	var newURL = homeURL+userInput;
	var req = new XMLHttpRequest();
	req.open("GET", newURL, true);
	req.addEventListener('load', function(){
		if(req.status>= 200 && req.status<400){
		var response = JSON.parse(req.responseText);
		console.log(response);
		}
			else {
				console.log("Error in network request: " + request.statusText);
			}
	});
	req.send(null);
	event.preventDefault();
});
}

function bindGetFriendListButton(){
	document.getElementById('getFriendList').addEventListener('click', function(event) {
	var homeURL = "http://localhost:3000/getfriendlist/?"
	var userInput = document.getElementById('getFriendListInput').value;
	var newURL = homeURL+userInput;
	var req = new XMLHttpRequest();
	req.open("GET", newURL, true);
	req.addEventListener('load', function(){
		if(req.status>= 200 && req.status<400){
		var response = JSON.parse(req.responseText);
		console.log(response);
		}
			else {
				console.log("Error in network request: " + request.statusText);
			}
	});
	req.send(null);
	event.preventDefault();
});
}