function Thinklight() {};
//Thinklight.midiChannel = 0xF0;
Thinklight.currentDeck = 1;

Thinklight.init = function init() {
	print("Thinklight init");
	var deck = Thinklight.currentDeck == 1 ? "[Channel1]" : "[Channel2]";
	connectControl(deck, "beat_active", this.onBeatActiveValueCB);
};

Thinklight.onBeatActiveValueCB = function (value) {
	print("t" + value);
	midi.sendShortMsg(status, 0xF0, value);
};

Thinklight.shutdown = function shutdown() {
	print("shutdown");
};

