// access chrome local storage
var storage = chrome.storage.local;

// set reload interval
var reload = setInterval(skua_filter, 500);

// add classes for skua buttons
var trollButton = $("#skua-troll");
var notTrollButton = $("#skua-notTroll");

// variable to store the slider value
var sliderValue;

// a function to remove text between brackets
function removeBrackets(input) {
  return input
    .replace(/<.*?>/g, "");
}

// a function to implement filtering
function skua_filter() {

  // get the slider value
  storage.get('aValue', function(items) {
      sliderValue = items.aValue;

      // get all tweets on the current page
      var tweets = document.getElementsByClassName("tweet-text");

      // get all tweets tagged with `skua-tweet`
      var skua_tweets = document.getElementsByClassName("skua-tweet");

      // if there are unprocessed tweets, find them and process them
      if (tweets.length != skua_tweets.length)
      {
        console.log("running skua")
        for(var i=0; i <tweets.length; i++)
        {

        // if the current tweet has the `skua-tweet` class, it's been processed
        // already, so do nothing. Otherwise, process the tweet.
        if (tweets[i].classList.contains("skua-tweet")) {
        } else {
          // add the `skua-tweet` class
          tweets[i].className += " skua-tweet";

          // make new data elements to store the `skua_score` and `user_score`
          $(tweets[i]).parents('.tweet').data('skua_score')
          $(tweets[i]).parents('.tweet').data('user_score')

          // get the tweet text and clean it
          var clean_text = removeBrackets(tweets[i].innerHTML);

          // send the clean_text to the skua API
          $.get("https://www.skua.online/CleverBird", { tweet: clean_text, element: i })
            .done(function( result ) {
              // update the tweet background based on the skua_score
              $(tweets[result.element]).parents('.tweet').css('background', result.color);

              // save the skua_score as data for the element
              $(tweets[result.element]).parents('.tweet').data('skua_score', result.score);
            }, "json");

            // add troll button button if it doesn't already exist.
            if ($(tweets[i]).parents('.tweet').find( ".skua-troll" )[0]) {
            } else {
              $(tweets[i]).parents('.tweet').find("ul").prepend('<li class="skua-troll" role="presentation"> <button type="button" class="dropdown-link" role="menuitem">Troll (Skua)</button></li>');
            }

            // add notTroll button if it doesn't already exist.
            if ($(tweets[i]).parents('.tweet').find( ".skua-notTroll" )[0]) {
            } else {
              $(tweets[i]).parents('.tweet').find("ul").prepend('<li class="skua-notTroll" role="presentation"> <button type="button" class="dropdown-link" role="menuitem">Not Troll (Skua)</button></li>');
            }

            // click action for troll button
            $(tweets[i]).parents('.tweet').find( ".skua-troll" ).click(function() {
              // set tweet background and update user_score
              $(this).parents('.tweet').css('background', 'rgb(222, 45, 38)');
              $(this).parents('.tweet').data('user_score', 100);
              // log tweet in database
              $.get("https://www.skua.online/SkuaLogging", {
                tweet: removeBrackets($(this).parents('.tweet').find('.tweet-text').text()),
                troll: 'True' });
            });

            // click action for notTroll button
            $(tweets[i]).parents('.tweet').find( ".skua-notTroll" ).click(function() {
              // set tweet background and update user_score
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

      // filter tweets based on slider value, skua_score, and user_score
      for(var i=0; i <tweets.length; i++)
      {
        if ($(tweets[i]).parents('.tweet').data('skua_score') > sliderValue) {

          // skua_score is higher than slider value, tweet should be hidden
          // unless manually labeled `notTroll` by user.

          if ($(tweets[i]).parents('.tweet').data('user_score') == 0) {

            // user manually labeled tweet as notTroll, tweet should be shown
            $(tweets[i]).parents('.tweet').show();

          } else {

            // skua_score is higher than slider value and user has not labeled
            // tweet as notTroll; hide tweet.
            $(tweets[i]).parents('.tweet').hide();

          }
          
        } else if ($(tweets[i]).parents('.tweet').data('user_score') > sliderValue) {

          // user has labeled tweet as troll. Hide if slider value is less than 100.
          $(tweets[i]).parents('.tweet').hide();

        } else {

          // no reason to hide tweet, so show it.
          $(tweets[i]).parents('.tweet').show();

        }
      }
    });
}
