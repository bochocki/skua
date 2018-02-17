// access chrome's local storage
var storage = chrome.storage.local;

// access skua's slider
var slide = document.getElementById('skuaSlider');

// get/set skua's slider value
storage.get('aValue', function(items) {
    if (items.aValue) {
      slide.value = items.aValue;
    } else {
      slide.value = 100;
    }
  });
