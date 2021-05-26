class Car {

	constructor(entryID, listingURL, region, regionURL, entryPrice, entryYear, manufacturerOfVehicle, modelOfVehicle, conditionOfVehicle, numberOfCylinders) {
		this.entryID = entryID;
		this.listingURL = listingURL;
		this.region = region;
		this.regionURL = regionURL;
		this.entryPrice = entryPrice;
		this.entryYear = entryYear;
		this.manufacturerOfVehicle = manufacturerOfVehicle;
		this.modelOfVehicle = modelOfVehicle;
		this.conditionOfVehicle = conditionOfVehicle;
		this.numberOfCylinders = numberOfCylinders;
	}

	get entryID() { return this.entryID; }
	get listingURL() { return this.listingURL; }
	get region() { return this.region; }
	get regionURL() { return this.regionURL; }
	get entryPrice() { return this.entryPrice; }
	get entryYear() { return this.entryYear; }
	get manufacturerOfVehicle() { return this.manufacturerOfVehicle; }
	get modelOfVehicle() { return this.modelOfVehicle; }
	get conditionOfVehicle() { return this.conditionOfVehicle; }
	get numberOfCylinders() { return this.numberOfCylinders; }
}