// Set up initial plot sizes
var width = 960;
var height = 700;
var radius = Math.min(width, height) / 2;
var color = d3.scale.category20c();

// Append the SVG element to DOM element
var svg = d3.select("#plot").append("svg").attr("width", width).attr("height",
		height).append("g").attr("transform",
		"translate(" + width / 2 + "," + height * .52 + ")");

var partition = d3.layout.partition().sort(null).size(
		[ 2 * Math.PI, radius * radius ]).value(function(d) {
	return 1;
});

var arc = d3.svg.arc().startAngle(function(d) {
	return d.x;
}).endAngle(function(d) {
	return d.x + d.dx;
}).innerRadius(function(d) {
	return Math.sqrt(d.y);
}).outerRadius(function(d) {
	return Math.sqrt(d.y + d.dy);
});

d3.json("/sunburst/asterank_json", function(error, root) {
	var path = svg.datum(root).selectAll("path").data(partition.nodes).enter()
			.append("path").attr("display", function(d) {
				return d.depth ? null : "none";
			}) // hide inner ring
			.attr("d", arc).style("stroke", "#fff").style("fill", function(d) {
				return color((d.children ? d : d.parent).name);
			}).each(stash).style("opacity", 1).on("mouseover", mouseover);

	// Add the mouseleave handler to the bounding circle.
	d3.select("#plot").on("mouseleave", mouseleave);

	d3.selectAll("input").on(
			"change",
			function change() {
				var value = this.value === "count" ? function() {
					return 1;
				} : function(d) {
					return d.size;
				};

				path.data(partition.value(value).nodes).transition().duration(
						1500).attrTween("d", arcTween);
			});
});

// Fade all but the current sequence, and show it in the breadcrumb trail.
function mouseover(d) {
	// var percentage = (100 * d.value / totalSize).toPrecision(3);
	// var percentageString = percentage + "%";
	// if (percentage < 0.1) {
	// percentageString = "< 0.1%";
	// }

	d3.select("#percentage").text("100%");

	d3.select("#explanation").style("visibility", "");

	var sequenceArray = getAncestors(d);
	// updateBreadcrumbs(sequenceArray, percentageString);

	// Fade all the segments.
	d3.selectAll("path").style("opacity", 0.3);

	// Then highlight only those that are an ancestor of the current segment.
	svg.selectAll("path").filter(function(node) {
		return (sequenceArray.indexOf(node) >= 0);
	}).style("opacity", 1);
}

// Restore everything to full opacity when moving off the visualization.
function mouseleave(d) {

	// Hide the breadcrumb trail
	// d3.select("#trail")
	// .style("visibility", "hidden");

	// Deactivate all segments during transition.
	d3.selectAll("path").on("mouseover", null);

	// Transition each segment to full opacity and then reactivate it.
	d3.selectAll("path").transition().duration(1000).style("opacity", 1).each(
			"end", function() {
				d3.select(this).on("mouseover", mouseover);
			});

	d3.select("#explanation").transition().duration(1000).style("visibility",
			"hidden");
}

// Given a node in a partition layout, return an array of all of its ancestor
// nodes, highest first, but excluding the root.
function getAncestors(node) {
	var path = [];
	var current = node;
	while (current.parent) {
		path.unshift(current);
		current = current.parent;
	}
	return path;
}

// Stash the old values for transition.
function stash(d) {
	d.x0 = d.x;
	d.dx0 = d.dx;
}

// Interpolate the arcs in data space.
function arcTween(a) {
	var i = d3.interpolate({
		x : a.x0,
		dx : a.dx0
	}, a);
	return function(t) {
		var b = i(t);
		a.x0 = b.x;
		a.dx0 = b.dx;
		return arc(b);
	};
}

d3.select(self.frameElement).style("height", height + "px");