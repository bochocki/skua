var storage = chrome.storage.local;
/*
var val = document.getElementById("skuaSlider").value
console.log('popup');
console.log(val);
*/
var slide = document.getElementById('skuaSlider');

/*storage.get('aValue', function(items) {
    if (items.aValue) {
      slide.value = items.aValue);
    } else {
      console.log('nothing')
    }
  });
*/
// THIS WORKS:
//storage.set({'aValue': slide.value}, function() { });

slide.oninput = function() {
  storage.set({'aValue': this.value}, function() { });
}

/*
$("#skuaSlider").bind("change", function() {
        storage.set({'aValue': "testing"}, function() { });
});
*/
