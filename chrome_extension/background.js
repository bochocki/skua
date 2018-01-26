var myVar = setInterval(skua_filter, 500);


var storage = chrome.storage.local;

// remove text in brackets
function removeBrackets(input) {
  return input
    .replace(/<.*?>/g, "");
}

var sliderValue;
var element = document.createElement("div");
element.className = "TESTER";


function skua_filter() {

  storage.get('aValue', function(items) {
      sliderValue = items.aValue;

      var tweets = document.getElementsByClassName("tweet-text");
      var skua_tweets = document.getElementsByClassName("skua-tweet");

      if (tweets.length != skua_tweets.length)
      {
        console.log("running skua")
        for(var i=0; i <tweets.length; i++)
        {

        if (tweets[i].classList.contains("skua-tweet"))
        {

        } else {
          $(tweets[i]).parent().prepend(element);

          tweets[i].className += " skua-tweet";
          $(tweets[i]).data('ss')
          var clean_text = removeBrackets(tweets[i].innerHTML);

          tweets[i].appendChild(element);

          $.get("https://www.skua.online/CleverBird", { tweet: clean_text, element: i })
            .done(function( result ) {
              $(tweets[result.element]).parents('.tweet').css('background', result.color);
              $(tweets[result.element]).data('ss', result.score);
            }, "json");
          }

          /*if (ss > sliderValue)
          {
            $(tweets[i]).parents('.tweet').css('color', 'red');
          }*/
        }

      }
      for(var i=0; i <tweets.length; i++)
      {
        if ($(tweets[i]).data('ss') > sliderValue) {
          $(tweets[i]).parents('.tweet').hide();
        } else {
          $(tweets[i]).parents('.tweet').show();
        }
      }
    });
}
