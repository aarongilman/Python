var margin = {top: 8, right: 30, bottom: 3, left: 240},
    width = 280,
    height = 300,
    shift = 3,
    numberOfTicks = 5,
    fig_height = height - margin.top - margin.bottom,
    axis_loc = fig_height - 4
    bar_gap = 6;

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<span style='text-decoration: underline'>" +
        d.index + "</span>: <br><br> Change in purchasing power since 2000: <span style='color:orangered'>" +
        d.cumulative_change +
        "</span> <br><br> Average hourly earnings: <span style='color:orangered'>" +
        d.nominal_wage + "</span> <br><br> ";
    })

  d3.json("ahe.json", function (data) {

    var x = d3.scaleLinear()
            .domain(d3.extent(data, function(d) { return + d.cumulative_change; }))
            .range([0, width]);

    var y_spacing = fig_height / data.length;

    var canvas = d3.select("#bar_chart").append("svg")
      .attr("width", width + margin.left + margin.right + 10)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    canvas.call(tip)

    canvas.selectAll("rect.value_1")
      .data(data)
      .enter()
        .append("rect")
        .attr("class", "value_1")
        .attr("width", function (d) { return Math.abs(x(d.cumulative_change) - x(0)); })
        .attr("height", y_spacing - bar_gap)
        .attr("x", function (d) { return x(Math.min(0, d.cumulative_change)); })
        .attr("y", function (d, i) { return i * y_spacing; })
        .attr("fill", "darkblue")
        .on('mouseover', function(d){
          tip.show(d);
          d3.select(this).attr("fill", "orangered");})
        .on('mouseout', function(d){
          tip.hide(d);
          d3.select(this).attr("fill", "darkblue");}
        )
        .attr("transform", "translate(" + shift + ", 0)");

    canvas.selectAll("text.y_label")
      .data(data)
      .enter()
        .append("text")
        .attr("class", "y_label")
        .attr("fill", "black")
        .style("font-size", "12px")
        .attr("text-anchor", "end")
        .attr("y", function (d, i) { return i * y_spacing + 14; })
        .attr("x", shift - 28)
        .text(function (d) { return d.index; });

    canvas.selectAll("text.value_label")
      .data(data)
      .enter().append("text")
        .attr("class", "value_label")
        .text(function(d) {return d3.format(".1f")(d.cumulative_change);})
        .attr("text-anchor", "left")
        .attr("x", function(d, i) {
            if (d.cumulative_change <= 0) {
                console.log(d.cumulative_change);
                return  x(Math.min(0, d.cumulative_change)) + shift - 24;
            }
            else {return  x(Math.min(0, d.cumulative_change)) + Math.abs(x(d.cumulative_change) - x(0)) + shift + 2;}
        })
        .attr("y", function (d, i) { return i * y_spacing + 14; });

   canvas.append("g")
      .attr("transform", "translate(" + shift + "," + axis_loc + ")")
      .attr("class", "x axis")
      .call(d3.axisBottom(x).ticks(numberOfTicks));

   canvas.append("line")
    .attr("x1", x(0))
    .attr("y1", -3)
    .attr("x2", x(0))
    .attr("y2", fig_height)
    .style("stroke-width", 2)
    .style("stroke", "gray")
    .style("fill", "none")
    .attr("transform", "translate(" + shift + ", 0)");
  });
