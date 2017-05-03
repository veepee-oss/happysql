'use strict';

angular.module('myApp.nodes', ['ngCookies']).

controller('nodesController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.tables = [];
    $scope.svgContainer = d3.select("#graph")
	.append("svg")
	.attr("width", 1000)
	.attr("height", 1000);
    
    var token = $cookies.get('token');
    var call = "tables"
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function (data) {
        $scope.tables = data;
	var nodes = [];
	data.forEach(function(element) {
	    var x = Math.random() * 200 + 50;
	    var y = Math.random() * 100 + 50;
	    nodes.push({x: x, y: y, r: "20px", label: element.table_name});
	});

	var text = $scope.svgContainer.selectAll("txt .txt")
	    .data(nodes)
	    .enter()
	    .append("svg:text")
	    .attr("x", function(d) { return (d.x - (d.label.length / 2) * (6)) })
	    .attr("y", function(d) { return d.y - parseInt(d.r) })
	    .text(function(d) { return d.label });

	var circle = $scope.svgContainer.selectAll("circle .circle")
	    .data(nodes)
	    .enter()
	    .append("svg:circle")
	    .attr("class", "node")
	    .attr("cx", function(d) { return d.x; }) // centre en posX = data.x
	    .attr("cy", function(d) { return d.y; }) // centre en posY = data.y
	    .attr("r", function(d) { return d.r; }) // rayon : 10px
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
			var x = (Math.cos(gap * i) * (10 * parseInt(d.r))) + d.x;
			var y = (Math.sin(gap * i) * (10 * parseInt(d.r))) + d.y;
			var tmpNode = {x: x, y: y, r: "20px", label: element.COLUMN_NAME};

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
			.attr("r", function(d) { return d.r; });

		    console.log(tableCircles);
		    var newText = $scope.svgContainer.selectAll("ntxt .ntxt")
			.data(tableCircles)
			.enter()
			.append("svg:text")
			.attr("x", function(d) { return (d.x - (d.label.length / 2) * 6) })
			.attr("y", function(d) { return d.y - parseInt(d.r) })
			.text(function(d) { return d.label });

		    var newLink = $scope.svgContainer.selectAll("newLink .newLink")
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

	    })
	    .call(d3.drag().on("drag", function(d, i) {
	    	d.x = d3.event.x
	        d.y = d3.event.y
	        d3.select(this).attr("transform", function(d,i){
	    	    return "translate(" + [ d.x,d.y ] + ")"
	    	})
	    }));
	
    }, function (error) {
        Materialize.toast('Operation failed!', 4000);
    });

}]);
