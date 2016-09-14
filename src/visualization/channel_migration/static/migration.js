$(document).ready(function() {
    console.log("javascript started");

    var svg = d3.select("svg");

    //  Get the current list of watching users and draw it
    $.ajax({
        url: "streams",
        method: "GET",
        dataType: "json",
        success: function(result) {
            // configure and draw circles
            var circles = svg.selectAll("circle")
                             .data(result)
                             .enter()
                             .append("circle")
                             .attr("class", "stream-node");

            circles.attr("r", function(d) { return Math.sqrt(d.watching.length); })
                   .attr("cx", function(d, i) { return i*200 + 30; })
                   .attr("cy", 200)
                   .attr("fill", "steelblue");

            // configure and draw labels
            var labels = svg.selectAll("text")
                            .data(result)
                            .enter()
                            .append("text")
                            .attr("class", "stream-label");
            labels.text(function(d) { return d.streamname; })
                  .attr("x", function(d, i) {return i*200 + 30; })
                  .attr("y", 200);
        }
    });
});
