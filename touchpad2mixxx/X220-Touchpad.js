function X220T() {}
//X220T.midiChannel = 0xE0;
//X220T.pressureChannel = 0xE1;
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
	var playing = engine.getValue(group, "play") ? 1. : 0.;
	value = value - 64
	value = value / 10.;
	//print("scratch " + value);
	//engine.setValue(group, "scratch2_enable", value < 0 || value > 0);
	if (X220T.pressure < 4) X220T.locked = 0;
	if (X220T.locked != 1) {
		p = X220T.pressure / 36;
		if (X220T.pressure >= 36) { p = 1.; X220T.locked = 1; }
		value = p * value + (1. - p) * playing;
	}
	if ((X220T.inertia > 30 && X220T.speed > 0) ||
			(X220T.inertia > 90 && X220T.speed < 0))
		X220T.speed = 0.999 * X220T.speed + 0.001 * value;
	else
		X220T.speed = 0.75 * X220T.speed + 0.25 * value;
	if (X220T.speed > 3 || X220T.speed < -3) X220T.inertia += 1;
	if (X220T.speed < 1 && X220T.speed > -1) X220T.inertia = 0;
	engine.setValue(group, "scratch2", X220T.speed);
};

X220T.pressure = function pressure(channel, control, value, status, group) {
	var playing = engine.getValue(group, "play") ? 1. : 0.;
	value = value - 64;
	//print("pressure " + value);
	X220T.pressure = value;
	engine.setValue(group, "scratch2_enable", value >= 1);
	if (value < 1) X220T.speed = playing;
};

