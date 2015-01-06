function X220T() {}
//X220T.midiChannel = 0xE0;
//X220T.pressureChannel = 0xE1;
//X220T.clicktapsChannel = 0xE2;
X220T.currentDeck = 1;
X220T.speed = 0;
X220T.pressure = 0;
X220T.locked = 0;
X220T.inertia = 0;

X220T.init = function init() {
	print("init");
};

X220T.shutdown = function shutdown() {
	print("shutdown");
};

X220T.scratch = function scratch(channel, control, value, status, group) {
	var deck = X220T.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	var playing = engine.getValue(deck, "play") ? 1. : 0.;
	value = value - 64
	value = value / 10.;
	//print("scratch " + value);
	//engine.setValue(group, "scratch2_enable", value < 0 || value > 0);
	if (X220T.pressure < 4) X220T.locked = 0;
	if (X220T.locked != 1) {
		p = X220T.pressure / 32;
		if (X220T.pressure >= 32) { p = 1.; X220T.locked = 1; }
		value = p * value + (1. - p) * playing;
	}
	if ((X220T.inertia > 30 && X220T.speed > 0) ||
			(X220T.inertia > 90 && X220T.speed < 0))
		X220T.speed = 0.999 * X220T.speed + 0.001 * value;
	else
		X220T.speed = 0.75 * X220T.speed + 0.25 * value;
	if (X220T.speed > 3 || X220T.speed < -3) X220T.inertia += 1;
	if (X220T.speed < 1 && X220T.speed > -1) X220T.inertia = 0;
	engine.setValue(deck, "scratch2", X220T.speed);
};

X220T.pressure = function pressure(channel, control, value, status, group) {
	var deck = X220T.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	var playing = engine.getValue(deck, "play") ? 1. : 0.;
	value = value - 64;
	//print("pressure " + value);
	X220T.pressure = value;
	engine.setValue(deck, "scratch2_enable", value >= 1);
	if (value < 1) X220T.speed = playing;
};

X220T.clicktaps = function clicktaps(channel, control, value, status, group) {
	value = value - 64;
	var deck = X220T.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	if (value == 0)
		engine.setValue("[Channel1]", "keylock",
				!engine.getValue("[Channel1]", "keylock"));
	if (value == 1)
		engine.setValue("[Channel2]", "keylock",
				!engine.getValue("[Channel2]", "keylock"));
	if (value == 2) X220T.currentDeck = 1;
	if (value == 3) X220T.currentDeck = 2;
	if (value == 4) {};
	if (value == 5) {};
	if (value == 6)
		engine.setValue("[Channel1]", "play",
				!engine.getValue("[Channel1]", "play"));
	if (value == 7)
		engine.setValue("[Channel2]", "play",
				!engine.getValue("[Channel2]", "play"));
	if (value == 8 || value == 9)
		engine.setValue(deck, "play", !engine.getValue(deck, "play"));
}
