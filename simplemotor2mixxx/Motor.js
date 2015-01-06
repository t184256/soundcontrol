function Motor() {};
//Motor.midiChannel = 0xE0;
Motor.TRANSMISSION_SCALE = 128.;
Motor.currentDeck = 1;

Motor.init = function init() {
	print("init");
	var deck = Motor.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	engine.setValue(deck, "scratch2_enable", true);
	//connectControl(deck, "beat_active", this.onBeatActiveValueCB);
};

//Motor.onBeatActiveValueCB = function (value) {
//	midi.sendShortMsg(status, 0xF0, value);
//};


Motor.shutdown = function shutdown() {
	print("shutdown");
};

Motor.scratch = function scratch(channel, control, value, status, group) {
	var deck = Motor.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	var playing = engine.getValue(deck, "play") ? 1. : 0.;
	var c = channel - 0xE5;
	value = channel * 128 + value - 1024;
	print(channel + "\t" + value);
	value /= Motor.TRANSMISSION_SCALE;
	//var alpha = 1./8;
	//var beta = alpha/32;
	//engine.scratchEnable(1, 15000, 100./3, alpha/2, beta/2, true);
	//engine.scratchTick(1, value);
	engine.setValue(deck, "scratch2_enable", true);
	engine.setValue(deck, "scratch2", value);
};

