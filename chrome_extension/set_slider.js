var storage = chrome.storage.local;
/*
var val = document.getElementById("skuaSlider").value
console.log('popup');
console.log(val);
*/
var slide = document.getElementById('skuaSlider');

storage.get('aValue', function(items) {
    if (items.aValue) {
      slide.value = items.aValue;
    } else {
      slide.value = 100;
    }
  });
