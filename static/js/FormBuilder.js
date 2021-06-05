$.post("/postmethod", function (columns, status) {
	columns.color.forEach(id => d3.select("#color").append("option").text(id).property("value", id));
	columns.condition.forEach(id => d3.select("#condition").append("option").text(id).property("value", id));
	columns.cyl.forEach(id => d3.select("#cyl").append("option").text(id).property("value", id));
	columns.fuel_type.forEach(id => d3.select("#fuel_type").append("option").text(id).property("value", id));
	columns.manufacturer.forEach(id => d3.select("#manufacturer").append("option").text(id).property("value", id));
	d3.select("#odometer").attr("placeholder", columns.odometer);
	columns.size.forEach(id => d3.select("#size").append("option").text(id).property("value", id));
	columns.state.forEach(id => d3.select("#state").append("option").text(id.toUpperCase()).property("value", id.toUpperCase()));
	columns.title.forEach(id => d3.select("#title").append("option").text(id).property("value", id));
	columns.transmission.forEach(id => d3.select("#transmission").append("option").text(id).property("value", id));
	columns.car_type.forEach(id => d3.select("#car_type").append("option").text(id).property("value", id));
	d3.select("#year").attr("placeholder", columns.year);

	AttachDOM();
});

function AttachDOM() {
	d3.select("color");
	d3.select("condition");
	d3.select("cyl");
	d3.select("fuel_type");
	d3.select("manufacturer");
	d3.select("odometer");
	d3.select("size");
	d3.select("state");
	d3.select("title");
	d3.select("transmission");
	d3.select("car_type");
	d3.select("year");

	var button = d3.select("button");
	button.on("click", onButtonClick);
}

function onButtonClick() {
	var formData = {
		color: d3.select("#color").property("value"),
		condition: d3.select("#condition").property("value"),
		cyl: d3.select("#cyl").property("value"),
		fuel_type: d3.select("#fuel_type").property("value"),
		manufacturer: d3.select("#manufacturer").property("value"),
		odometer: d3.select("#odometer").property("value"),
		size: d3.select("#size").property("value"),
		state: d3.select("#state").property("value"),
		title: d3.select("#title").property("value"),
		transmission: d3.select("#transmission").property("value"),
		car_type: d3.select("#car_type").property("value"),
		year: d3.select("#year").property("value"),
	}

	if (formData.odometer == "")
		formData.odometer = d3.select("#odometer").attr("placeholder");
	if (formData.year == "")
		formData.year = d3.select("#year").attr("placeholder");

	var url = []
	for (const [key, value] of Object.entries(formData))
		url.push(`${key}=${value}`);

	var baseWindowPath = window.location.href;
	baseWindowPath = baseWindowPath.substring(0, baseWindowPath.lastIndexOf("/") + 1);
	window.location.replace(baseWindowPath + "submit/" + url.join("&"));
}
