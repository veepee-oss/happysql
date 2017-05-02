var vis = d3.select("#graph")
    .append("svg");

var nodes = [{x: 30, y: 50},
	     {x: 200, y: 80},
	     {x: 90, y: 60}];

var links = [
    {source: nodes[0], target: nodes[1]},
    {source: nodes[2], target: nodes[1]}
];


vis.selectAll("circle .nodes")
    .data(nodes)
    .enter()
    .append("svg:circle")
    .attr("class", "node")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("r", "10px")
    // .attr("fill", "black")

