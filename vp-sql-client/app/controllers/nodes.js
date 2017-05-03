'use strict';

angular.module('myApp.nodes', ['ngCookies']).

controller('nodesController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.tables = [];
    $scope.svgContainer = d3.select("#graph")
	.append("svg")
	.attr("width", 1000)
	.attr("height", 1000);

    // d3.select("body")
    // 	.transition()
    // 	.delay(750)
    // 	.style("color", "red");

    var token = $cookies.get('token');
    var call = "tables"
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function (data) {
        $scope.tables = data;
	var nodes = [];
	data.forEach(function(element) {
	    var x = Math.random() * 200;
	    var y = Math.random() * 100;
	    nodes.push({x: x, y: y});
	});

	var circle = $scope.svgContainer.selectAll("lol .lol")
	    .data(nodes)
	    .enter()
	    .append("svg:circle")
	    .attr("class", "node")
	    .attr("cx", function(d) { return d.x; }) // centre en posX = data.x
	    .attr("cy", function(d) { return d.y; }) // centre en posY = data.y
	    .attr("r", "10px") // rayon : 10px
	    .on("click", function(d) {
		console.log($scope.tables[0]);
		var token = $cookies.get('token');
		var call = $scope.tables[0].table_schema + "." + $scope.tables[0].table_name + "/columns";
		var promise = callDB('GET', call, {'Authorization': token}, {});

		promise.then(function (data) {

		    var tableCircles = [];
		    var tableLinks = [];
		    var gap = (360 / data.length) * Math.PI / 180;
		    var i = 0
		    data.forEach(function(element) {
			// x = Math.cos(a)
			// y = Math.sin(a)
			var x = (Math.cos(gap * i) * 40) + d.x;
			var y = (Math.sin(gap * i) * 40) + d.y;
			// var x = Math.random() * 100; // algo to change LOLZ
			// var y = Math.random() * 200;
			var tmpNode = {x: x, y: y};

			tableLinks.push({source: tmpNode, target: d});
			tableCircles.push(tmpNode);
			i = i + 1
		    });

		    var newCircle = $scope.svgContainer.selectAll("circle .node")
			.data(tableCircles)
			.enter()
			.append("svg:circle")
			.attr("class", "tableNode")
			.attr("cx", function(d) { return d.x; }) // centre en posX = data.x
			.attr("cy", function(d) { return d.y; }) // centre en posY = data.y
			.attr("r", "5px");

		    var newLink = $scope.svgContainer.selectAll("lulz .lulz")
			.data(tableLinks)
			.enter()
			.append("svg:line")
			.attr("class", "link")
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
		    
		}, function (error) {
		    Materialize.toast('Operation failed!', 4000);
		});

	    }); // end onclick

    }, function (error) {
        Materialize.toast('Operation failed!', 4000);
    });

}]);
