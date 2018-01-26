var myVar = setInterval(skua_filter, 1000);


var storage = chrome.storage.local;

// remove text in brackets
function removeBrackets(input) {
  return input
    .replace(/<.*?>/g, "");
}

function skua_filter() {
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
      tweets[i].className += " skua-tweet";
      tweets[i]['skuaScore'] = 0;
      var clean_text = removeBrackets(tweets[i].innerHTML);

      $.get("https://www.skua.online/CleverBird", { tweet: clean_text, element: i })
        .done(function( data ) {
          $(tweets[data.element]).parents('.tweet').css('background', data.color);
          tweets[data.element]['skuaScore'] = data.score;
        }, "json");
      }

      storage.get('aValue', function(items, tweets, i) {
          console.log(tweets[i].innerHTML);

          /*if (tweets[i]['skuaScore'] > items.aValue) {
            console.log("block");
          } else {
            console.log('pass');
          }*/
        });

    }
  }
}
