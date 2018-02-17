// access chrome's local storage
var storage = chrome.storage.local;

// access skua's slider
var slide = document.getElementById('skuaSlider');

// store the slider's value so it cna have a persistent setting.
slide.oninput = function() {
  storage.set({'aValue': this.value}, function() { });
}
