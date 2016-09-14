$(document).ready(function() {
    console.log("javascript started");

    var svg = d3.select("svg");
    var circle = svg.selectAll("circle")
        .data([32, 57, 112, 293]);
    var circleEnter = circle.enter().append("circle");

    circle.style("fill", "steelblue");
    circle.attr("r", 30);

    //circle.attr("cx", function() { return Math.random() * 720; });

    circle.data([32, 57, 112]);
    // d refers to the data bound to the circle
    circle.attr("r", function(d) { return Math.sqrt(d); });
    // i refers to the index of the circle in the set of circles
    circle.attr("cx", function(d,i) { return i * 100 + 30; });

    circleEnter.attr("cy", 60);
    circleEnter.attr("cx", function(d,i) { return i * 100 + 30; });
    circleEnter.attr("r", function(d) { return Math.sqrt(d); });

    streamname = "summit1g";
    $.ajax({
        url: "streams/" + streamname,
        method: "GET",
        dataType: "json",
        success: function(result) {
            result.forEach(function(element, index, array) {
                if (console && console.log) {
                    console.log("summit1g viewers ...");
                    console.log(element.watching);
                }
            });
        }
    });
});
