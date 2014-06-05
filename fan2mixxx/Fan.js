function Fan() {};
//Fan.midiChannel = 0xE0;
Fan.TRANSMISSION_SCALE = 128.;
Fan.currentDeck = 1;

Fan.init = function init() {
	print("init");
	var deck = Fan.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	engine.setValue(deck, "scratch2_enable", true);
};

Fan.shutdown = function shutdown() {
	print("shutdown");
};

Fan.scratch = function scratch(channel, control, value, status, group) {
	var deck = Fan.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	var playing = engine.getValue(deck, "play") ? 1. : 0.;
	engine.setValue(deck, "scratch2_enable", true);
	var c = channel - 0xE5;
	value = channel * 256 + value - 2048;
	value /= Fan.TRANSMISSION_SCALE;
	//print(value);
	engine.setValue(deck, "scratch2", value);
};

