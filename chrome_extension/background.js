var myVar = setInterval(skua_filter, 500);
var trollButton = $("#skua-troll");
var notTrollButton = $("#skua-notTroll");

var storage = chrome.storage.local;

// remove text in brackets
function removeBrackets(input) {
  return input
    .replace(/<.*?>/g, "");
}

var sliderValue;

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
          tweets[i].className += " skua-tweet";

          // make a new data element to store skua score
          $(tweets[i]).parents('.tweet').data('skua_score')
          $(tweets[i]).parents('.tweet').data('user_score')

          var clean_text = removeBrackets(tweets[i].innerHTML);

          $.get("https://www.skua.online/CleverBird", { tweet: clean_text, element: i })
            .done(function( result ) {
              $(tweets[result.element]).parents('.tweet').css('background', result.color);
              $(tweets[result.element]).parents('.tweet').data('skua_score', result.score);
            }, "json");

            // add online learning buttons
            $(tweets[i]).parents('.tweet').find("ul").prepend('<li class="skua-troll" role="presentation"> <button type="button" class="dropdown-link" role="menuitem">Troll (Skua)</button></li>');
            $(tweets[i]).parents('.tweet').find("ul").prepend('<li class="skua-notTroll" role="presentation"> <button type="button" class="dropdown-link" role="menuitem">Not Troll (Skua)</button></li>');

            // TROLL BUTTON
            $(tweets[i]).parents('.tweet').find( ".skua-troll" ).click(function() {
              // set background and score
              $(this).parents('.tweet').css('background', 'rgb(222, 45, 38)');
              $(this).parents('.tweet').data('user_score', 100);
              // log tweet in database
              $.get("https://www.skua.online/SkuaLogging", {
                tweet: removeBrackets($(this).parents('.tweet').find('.tweet-text').text()),
                troll: 'True' });
            });

            // NOT TROLL BUTTON
            $(tweets[i]).parents('.tweet').find( ".skua-notTroll" ).click(function() {
              // set background and score
              $(this).parents('.tweet').css('background', 'white');
              $(this).parents('.tweet').data('user_score', 0);
              // log tweet in database
              $.get("https://www.skua.online/SkuaLogging", {
                tweet: removeBrackets($(this).parents('.tweet').find('.tweet-text').text()),
                troll: 'False' });
            });
          }
        }
      }

      for(var i=0; i <tweets.length; i++)
      {
        if ($(tweets[i]).parents('.tweet').data('skua_score') > sliderValue) {
          if ($(tweets[i]).parents('.tweet').data('user_score') == 0) {
          } else {
            $(tweets[i]).parents('.tweet').hide();
          }
        } else if ($(tweets[i]).parents('.tweet').data('user_score') > sliderValue) {
          $(tweets[i]).parents('.tweet').hide();
        } else {
          $(tweets[i]).parents('.tweet').show();
        }
      }
    });
}
