'use strict';

angular.module('myApp.nodes', ['ngCookies']).

controller('nodesController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    // $scope.tables = [];
    $scope.svgContainer = d3.select("#graph")
	.append("svg")
	.attr("width", 2000)
	.attr("height", 2000);
    // $scope.group = $scope.svgContainer.append("g")
    // 	.call(d3.drag().on("drag", function(d, i) {
    // 	    // console.log(d3.event);
    // 	    d3.select(this).attr("transform", function(d,i){
    // 	    	return "translate(" + [d3.event.x, d3.event.y] + ")";
    // 	    });
    // 	}));

    var token = $cookies.get('token');
    var call = "tables"
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function (response) {
        // $scope.tables = response.data;
	// var nodes = [];
	// response.data.forEach(function(element) {
	//     var x = Math.random() * 200 + 50;
	//     var y = Math.random() * 100 + 50;
	//     nodes.push({x: x, y: y, r: "20px", label: element.table_name});
	// });

	// var text = $scope.group.selectAll("txt .txt")
	//     .data(nodes)
	//     .enter()
	//     .append("svg:text")
	//     .attr("x", function(d) { return (d.x - (d.label.length / 2) * (6)) })
	//     .attr("y", function(d) { return d.y - parseInt(d.r) })
	//     .text(function(d) { return d.label });

	response.data.forEach(function(element) {
	    var nodes = [{x: Math.random() * 200 + 50, y: Math.random() * 100 + 50, r: "20px", label: element.table_name}];
	    var group = $scope.svgContainer.append("g")
		.call(d3.drag().on("drag", function(d, i) {
		    // console.log(d3.event);
		    d3.select(this).attr("transform", function(d,i){
	    		return "translate(" + [d3.event.x, d3.event.y] + ")";
		    });
		}));

	    var text = group.selectAll("txt .txt")
		.data(nodes)
		.enter()
		.append("svg:text")
		.attr("x", function(d) { return (d.x - (d.label.length / 2) * (6)) })
		.attr("y", function(d) { return d.y - parseInt(d.r) })
		.text(function(d) { return d.label });
	    
	    var circle = group.selectAll("circle .circle")
		.data(nodes)
		.enter()
		.append("svg:circle")
		.attr("class", "node")
		.attr("cx", function(d) { return d.x; }) // centre en posX = data.x
		.attr("cy", function(d) { return d.y; }) // centre en posY = data.y
		.attr("r", function(d) { return d.r; }) // rayon : 10px
		.on("click", function(d) {
		    // console.log($scope.tables[0]);
		    var token = $cookies.get('token');
		    var call = element.table_schema + "." + element.table_name + "/columns";
		    var promise = callDB('GET', call, {'Authorization': token}, {});

		    promise.then(function (response) {

			var tableCircles = [];
			var tableLinks = [];
			var gap = (360 / response.data.length) * Math.PI / 180;
			var i = 0
			response.data.forEach(function(element) {
			    var x = (Math.cos(gap * i) * (10 * parseInt(d.r))) + d.x;
			    var y = (Math.sin(gap * i) * (10 * parseInt(d.r))) + d.y;
			    var tmpNode = {x: x, y: y, r: "20px", label: element.COLUMN_NAME};

			    tableLinks.push({source: tmpNode, target: d});
			    tableCircles.push(tmpNode);
			    i = i + 1
			});

			var newCircle = group.selectAll("circle .circle")
			    .data(tableCircles)
			    .enter()
			    .append("svg:circle")
			    .attr("class", "tableNode")
			    .attr("cx", function(d) { return d.x; }) // centre en posX = data.x
			    .attr("cy", function(d) { return d.y; }) // centre en posY = data.y
			    .attr("r", function(d) { return d.r; });

			// console.log(tableCircles);
			var newText = group.selectAll("ntxt .ntxt")
			    .data(tableCircles)
			    .enter()
			    .append("svg:text")
			    .attr("x", function(d) { return (d.x - (d.label.length / 2) * 6) })
			    .attr("y", function(d) { return d.y - parseInt(d.r) })
			    .text(function(d) { return d.label });

			var newLink = group.selectAll("newLink .newLink")
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
		});
	});
    }, function (error) {
        Materialize.toast('Operation failed!', 4000);
    });
}]);
