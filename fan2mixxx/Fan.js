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
	var c = channel - 0xE5;
	value = channel * 128 + value - 1024;
	print(channel + "\t" + value);
	value /= Fan.TRANSMISSION_SCALE;
	//var alpha = 1./8;
	//var beta = alpha/32;
	//engine.scratchEnable(1, 15000, 100./3, alpha/2, beta/2, true);
	//engine.scratchTick(1, value);
	engine.setValue(deck, "scratch2_enable", true);
	engine.setValue(deck, "scratch2", value);
};

