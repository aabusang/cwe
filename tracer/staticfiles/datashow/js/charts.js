


function drawChart(data, chart_id="#btc-chart") {
  // Assuming the timeseries data is an array of objects like [{date: "2023-08-30", value: 100}, ...]

  const svg = d3.select("#btc-chart");
  const width = +svg.attr("width");
  const height = +svg.attr("height");

  const xValue = d => d.date;
  const yValue = d => d.value;

  const xScale = d3.scaleTime()
      .domain(d3.extent(timeseries, xValue))
      .range([0, width]);
      
  const yScale = d3.scaleLinear()
      .domain([0, d3.max(timeseries, yValue)])
      .range([height, 0]);
      
  const lineGenerator = d3.line()
      .x(d => xScale(xValue(d)))
      .y(d => yScale(yValue(d)));
      
  svg.append("path")
      .attr("d", lineGenerator(timeseries))
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2);

}

function drawLineChart(btcData, chart_id="#btc-chart") {
    console.log("drawLineChart called")
    // console.log("btcData:", btcData)
    try {
        const time = btcData.map(d => d.time);
        const concentration = btcData.map(d => d.concentration);
        const svgWidth = 928; //928 or 650
        const svgHeight = 450; //500
        const margin = { top: 40, right: 40, bottom: 60, left: 100 };
        const width = svgWidth - margin.left - margin.right;
        const height = svgHeight - margin.top - margin.bottom;

        const svg = d3.select(chart_id)
          .append("svg")
          .attr("width", svgWidth)
          .attr("height", svgHeight)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Set up scales
        const xScale = d3.scaleLinear()
          .domain([d3.min(time), d3.max(time)])
          .range([0, width]);

        const yScale = d3.scaleLinear()
          .domain([d3.min(concentration), d3.max(concentration)])
          .range([height, 0]);

        // Define the line
        const line = d3.line()
          .x((d, i) => xScale(time[i]))
          .y((d, i) => yScale(concentration[i]));

        // Draw the line chart
        svg.append("path")
          .datum(btcData)
          .attr("class", "line")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 1.5)
          .attr("fill", "none")
          .attr("d", line);

        // Add x-axis
        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(xScale));

        // Add y-axis
        svg.append("g")
          .call(d3.axisLeft(yScale));


        // Add x-axis label
        svg.append("text")
          .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 10) + ")")
          .style("text-anchor", "middle")
          .text("Time (hours))");

        // Add y-axis label
        svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left)
          .attr("x", 0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Observed Concentration (ppb)");

    } catch (error) {
        console.log("Error occured in drawChart:", error);
    }
  }
  