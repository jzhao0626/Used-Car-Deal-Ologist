// class Car {

// 	constructor(entryID, listingURL, region, regionURL, entryPrice, entryYear, manufacturerOfVehicle, modelOfVehicle, conditionOfVehicle, numberOfCylinders) {
// 		this.entryID = entryID;
// 		this.listingURL = listingURL;
// 		this.region = region;
// 		this.regionURL = regionURL;
// 		this.entryPrice = entryPrice;
// 		this.entryYear = entryYear;
// 		this.manufacturerOfVehicle = manufacturerOfVehicle;
// 		this.modelOfVehicle = modelOfVehicle;
// 		this.conditionOfVehicle = conditionOfVehicle;
// 		this.numberOfCylinders = numberOfCylinders;
// 	}

// 	get entryID() { return this.entryID; }
// 	get listingURL() { return this.listingURL; }
// 	get region() { return this.region; }
// 	get regionURL() { return this.regionURL; }
// 	get entryPrice() { return this.entryPrice; }
// 	get entryYear() { return this.entryYear; }
// 	get manufacturerOfVehicle() { return this.manufacturerOfVehicle; }
// 	get modelOfVehicle() { return this.modelOfVehicle; }
// 	get conditionOfVehicle() { return this.conditionOfVehicle; }
// 	get numberOfCylinders() { return this.numberOfCylinders; }
// }


var manufacturer = ['Make', 'bmw', 'toyota', 'honda', 'chevrolet', 'mazda', 'ford', 'volvo', 'cadillac', 'saturn', 'subaru', 'dodge', 'gmc', 'ram', 'chrysler', 'mercedes-benz', 'infiniti', 'jeep', 'buick', 'nissan', 'volkswagen', 'mercury', 'hyundai', 'lexus', 'porsche', 'rover', 'audi', 'fiat', 'mini', 'mitsubishi', 'lincoln', 'jaguar', 'kia', 'pontiac', 'acura', 'tesla', 'alfa-romeo', 'datsun', 'harley-davidson', 'land rover', 'aston-martin', 'ferrari'];

var type = ['Type', 'SUV', 'mini-van', 'convertible', 'coupe', 'truck', 'wagon', 'sedan', 'pickup', 'hatchback', 'van', 'other', 'bus', 'offroad'];

var color = ['Color', 'blue', 'white', 'grey', 'black', 'brown', 'red', 'silver', 'green', 'yellow', 'purple', 'custom', 'orange'];

var condition = ["Condition", "New", "Like New", "Excellent", "Good", "Fair", "Salvage"];

var fuel = ["Fuel Type", "Electric", "Gas", "Diesel", "Other"];

var title = ["Title Status", "Clean", "Rebuilt", "Lien", "Salvage", "Parts Only", "Missing"];

var transmission = ["Transmission", "Automatic", "Other", "Manual"];

var size = ["Vehicle Size", "Compact", "Sub-Compact", "Mid-Size", "Full-Size"];

var state = ['State', 'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'nc', 'ne', 'nv', 'nj', 'nm', 'ny', 'nh', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy'];
var cylinders = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

refresh()

manufacturer.forEach(id => d3.select('#manufacturer').append('option').text(id).property("value", id));
type.forEach(id => d3.select('#type').append('option').text(id).property("value", id));
color.forEach(id => d3.select('#color').append('option').text(id).property("value", id));
condition.forEach(id => d3.select('#condition').append('option').text(id).property("value", id));
fuel.forEach(id => d3.select('#fuel').append('option').text(id).property("value", id));
title.forEach(id => d3.select('#title').append('option').text(id).property("value", id));
transmission.forEach(id => d3.select('#transmission').append('option').text(id).property("value", id));
size.forEach(id => d3.select('#size').append('option').text(id).property("value", id));
state.forEach(id => d3.select('#state').append('option').text(id.toUpperCase()).property("value", id.toUpperCase()));
cylinders.forEach(id => d3.select('#cyl').append('option').text(id).property("value", id));

function refresh() {
	d3.select('#manufacturer').html("")
	d3.select('#type').html("")
	d3.select('#color').html("")
	d3.select('#condition').html("")
	d3.select('#fuel').html("")
	d3.select('#title').html("")
	d3.select('#transmission').html("")
	d3.select('#size').html("")
	d3.select('#state').html("")
	d3.select('#cyl').html("")
}

var button = d3.select("button");
button.on("click", onButtonClick);
function onButtonClick() {
	var formData = {
		manufacturer: d3.select('#manufacturer').property("value"),
		type: d3.select('#type').property("value"),
		color: d3.select('#color').property("value"),
		condition: d3.select('#condition').property("value"),
		fuel: d3.select('#fuel').property("value"),
		title: d3.select('#title').property("value"),
		transmission: d3.select('#transmission').property("value"),
		size: d3.select('#size').property("value"),
		state: d3.select('#state').property("value"),
		cyl: d3.select('#cyl').property("value"),
	}
	console.log(formData);
}


