'use strict';

angular.module('myApp.nodes', ['ngCookies']).

controller('nodesController', ['$scope', '$cookies', 'callDB', function($scope, $cookies, callDB) {
    $scope.svgContainer = d3.select("#graph")
	.append("svg")
	.attr("width", 2000)
	.attr("height", 2000);

    var token = $cookies.get('token');
    var call = "tables";
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function (response) {
	response.data.forEach(function(element) {
	    var nodes = [{x: Math.random() * 200 + 50, y: Math.random() * 100 + 50, r: "20px", label: element.table_name}];
	    var group = $scope.svgContainer.append("g")
		.call(d3.drag().on("drag", function(d, i) {
		    d3.select(this).attr("transform", function(d,i){
	    		return "translate(" + [d3.event.x - nodes[0].x, d3.event.y - nodes[0].y] + ")";
		    });
		}));

	    var text = group.selectAll("txt.txt")
		.data(nodes)
		.enter()
		.append("svg:text")
		.attr("x", function(d) { return (d.x - (d.label.length / 2) * (6)) })
		.attr("y", function(d) { return d.y - parseInt(d.r) })
		.text(function(d) { return d.label });

	    var circle = group.selectAll("circle.circle")
		.data(nodes)
		.enter()
		.append("svg:circle")
		.attr("class", "node")
		.attr("cx", function(d) { return d.x; })
		.attr("cy", function(d) { return d.y; })
		.attr("r", function(d) { return d.r; })
		.on("click", function(d) {
		    var groupNodes = group._groups[0][0].childNodes;
		    var nbStartNodes = 2;
		    if (groupNodes.length > nbStartNodes) {
			var i = (groupNodes.length - nbStartNodes);
			for (var j = 0; j < i; ++j) {
			    groupNodes[nbStartNodes].remove();
			}
			return ;
		    }
		    var token = $cookies.get('token');
		    var call = element.table_schema + "." + element.table_name + "/columns";
		    var promise = callDB('GET', call, {'Authorization': token}, {});

		    promise.then(function (response) {
			var guid = response.headers('X-Guid');
			var tableCircles = [];
			var tableLinks = [];
			var gap = (360 / response.data.length) * Math.PI / 180;
			var i = 0
			response.data.forEach(function(element) {
			    var x = (Math.cos(gap * i) * (10 * parseInt(d.r))) + d.x;
			    var y = (Math.sin(gap * i) * (10 * parseInt(d.r))) + d.y;
			    var tmpNode = { x: x, y: y, r: "20px", label: element.COLUMN_NAME };
			    tableLinks.push({source: tmpNode, target: d});
			    tableCircles.push(tmpNode);
			    i = i + 1
			});

			var newCircle = group.selectAll("subCircle.circle")
			    .data(tableCircles)
			    .enter()
			    .append("svg:circle")
			    .attr("class", function(d) { if (d.label === guid) { return ("guidNode") } else { return ("tableNode") } })
			    .attr("cx", function(d) { return d.x; })
			    .attr("cy", function(d) { return d.y; })
			    .attr("r", function(d) { return d.r; });

			var newText = group.selectAll("ntxt.ntxt")
			    .data(tableCircles)
			    .enter()
			    .append("svg:text")
			    .attr("x", function(d) { return (d.x - (d.label.length / 2) * 6) })
			    .attr("y", function(d) { return d.y - parseInt(d.r) })
			    .text(function(d) { return d.label });

			var newLink = group.selectAll("newLink.newLink")
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
