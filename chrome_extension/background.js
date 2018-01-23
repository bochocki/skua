var targetNodes         = $(".stream-items");
var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
var myObserver          = new MutationObserver (mutationHandler);
var obsConfig           = { childList: true, characterData: true, attributes: true, subtree: true };

//--- Add a target node to the observer. Can only add one node at a time.
targetNodes.each ( function () {
    myObserver.observe (this, obsConfig);
} );

function removeBrackets(input) {
    return input
        .replace(/<.*?>/g, "");
}

function mutationHandler (mutationRecords) {

    mutationRecords.forEach ( function (mutation) {

	var matches = document.getElementsByClassName("tweet-text");
        for(var i=0; i <matches.length; i++)
        {
	    if (matches[i].classList.contains("clever-tweet")) {

	    } else {
		matches[i].className += " clever-tweet";

		var clean_text = removeBrackets(matches[i].innerHTML);

		$.get("https://localhost:5000/CleverBird", { tweet: clean_text, element: i })
		    .done(function( data ) {
			$(matches[data.element]).parent().parent().parent().css('background', data.score);
		    }, "json");
	    }
        }
    } );
}
