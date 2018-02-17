var storage = chrome.storage.local;
var slide = document.getElementById('skuaSlider');

slide.oninput = function() {
  storage.set({'aValue': this.value}, function() { });
}
