// Set up initial plot sizes
var width = 700;
var height = 700;
var radius = Math.min(width, height) / 2;
var color = d3.scale.category10();

// Total size of all segments; we set this later, after loading the data.
var totalSize = 0;

// Append the SVG element to DOM element
var svg = d3.select("#plot").append("svg").attr("width", width).attr("height",
		height).append("g").attr("transform",
		"translate(" + width / 2 + "," + height / 2 + ")");

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
			.attr("d", arc).style("stroke", "#fff").style("fill",
					function(d) {
						return color((d.children ? d : d.parent).name);
					}).style("opacity", 1).on("mouseover",
					mouseover);

	// Add the mouseleave handler to the bounding circle.
	svg.on("mouseleave", mouseleave);

	// Get total size of the tree = value of root node from partition.
	totalSize = path.node().__data__.value;
});

// Fade all but the current sequence, and show it in the breadcrumb trail.
function mouseover(d) {
	var sequenceArray = getAncestors(d);
	var percentage = (100 * d.value / totalSize).toPrecision(3);
	
	var percentageString = percentage + "%";
	var descriptionString = "of asteroids "
	
	// Step through the ancestors' features
	sequenceArray.forEach(function(element, index, array) {
		if (element.feature != null) {
			// Add the "and" conjunction only on last element
			if (index == (array.length - 1) && array.length > 1) {
				descriptionString += " and ";
			}
			
			// Translate meaning of feature to English
			if (element.feature == "spectra") {
				descriptionString += "are spectral type " + element.name;
			} else if (element.feature == "discovery") {
				descriptionString += "were discovered in the " + element.name;
			} else if (element.feature == "size") {
				descriptionString += "are of " + element.name + "size";
			}
			
			// Oxford comma... yeah
			if (index < (array.length - 1) && array.length > 2) {
				descriptionString += ", ";
			}
		}
	});

	d3.select("#percentage").text(percentageString);
	d3.select("#descriptive_text").text(descriptionString);
	d3.select("#explanation").style("visibility", "");

	// Fade all the segments.
	d3.selectAll("path").style("opacity", 0.3);

	// Then highlight only those that are an ancestor of the current segment.
	svg.selectAll("path").filter(function(node) {
		return (sequenceArray.indexOf(node) >= 0);
	}).style("opacity", 1);
}

// Restore everything to full opacity when moving off the visualization.
function mouseleave(d) {

	// Deactivate all segments during transition.
	d3.selectAll("path").on("mouseover", null);

	// Transition each segment to full opacity and then reactivate it.
	d3.selectAll("path").transition().duration(500).style("opacity", 1).each(
			"end", function() {
				d3.select(this).on("mouseover", mouseover);
			});

	d3.select("#explanation").transition().duration(500).style("visibility",
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

d3.select(self.frameElement).style("height", height + "px");