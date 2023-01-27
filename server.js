var express = require('express');
var app = express();
const fs = require('fs');
var request = require('request');

app.set('port', 3000);

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

// Here gets parameters from end of URL to use in api address.  These parameters will come from submit buttons 
// on the respective sites
app.get('/getplayersummary', function(req, res) {
	var qParams = [];
	for (var p in req.query) {
		qParams.push({'name':p, 'value':req.query[p]})
	}
var url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=XXXXXXXXXXXXXXXXXXXX&steamids=' + qParams[0].name;
	request(url, function(err, response, body) {
		if(!err && response.statusCode < 400) {
			console.log(body);
			res.send(body);
		}
	});	
});

app.get('/getfriendlist', function(req, res) {
	var qParams = [];
	for (var p in req.query) {
		qParams.push({'name':p, 'value':req.query[p]})
	}
var nName = "jsonFiles/"+String(qParams[0].name)+".json";
var url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=XXXXXXXXXXXXXXXXXXX&steamid=' + qParams[0].name + '&relationship=friend';
	
	request(url, function(err, response, body) {
		if(!err && response.statusCode < 400) {
			console.log(body);
			
			fs.writeFile(nName, body, (err) => {
				if (err) {
					throw new Error('Something went wrong.')
				}
			res.send(body);
		})
	}});	
});

app.use(function(req,res){
  res.type('text/plain');
  res.status(404);
  res.send('404 - Not Found');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.send('500 - Server Error');
});

app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});