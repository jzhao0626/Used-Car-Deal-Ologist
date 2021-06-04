class Vehicle {
	
	constructor(manufacturer, type, color, condition, fuel, title, transmission, size, state, cyl, year, odometer) {
		this.manufacturer = manufacturer;
		this.type = type;
		this.color = color;
		this.condition = condition;
		this.fuel = fuel;
		this.title = title;
		this.transmission = transmission;
		this.size = size;
		this.state = state;
		this.cyl = cyl;
		this.year = year;
		this.odometer = odometer;
	}

	get manufacturer() { return this.manufacturer; }
	get type() { return this.type; }
	get color() { return this.color; }
	get condition() { return this.condition; }
	get fuel() { return this.fuel; }
	get title() { return this.title; }
	get transmission() { return this.transmission; }
	get size() { return this.size; }
	get state() { return this.state; }
	get cyl() { return this.cyl; }
	get year() { return this.year; }
	get odometer() { return this.odometer; }

	get isValid()
	{
	}
}
