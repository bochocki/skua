# Skua: A smart filter for abusive tweets.

Skua is a Chrome Extension that uses machine learning to help you avoid bullies
and trolls on Twitter. Skua automatically hides abusive tweets based on
real-time text classification.

Skua adds a red background color to tweets in your feed that it thinks are
likely to be abusive. The darker the shade of red, the more confident Skua is
that the tweet is abusive.

You can take Skua a step further and automatically hide abusive tweets from your
feed. Simply click on the browser extension and dial into the level of
filtering you're comfortable with.

You can help make Skua smarter! To tag a tweet as "trolling" or "not trolling",
simply click the dropdown menu and label the tweet accordingly. Skua will
remember your decision and use that information to improve its filtering
methods.

You can try Skua by going to [skua.online] and adding the extension from the
Chrome Store.

### About this Repo
This repository contains five directories:

 - **chrome_extension:** the code (mostly JavaScript) used to build the Skua
 extension.
 - **data_utils:** utility functions used to conduct model training/testing.
 - **flask_api:** the Flask/Python RESTful API that powers Skua.
 - **model_building:** code for data exploration and model selection.
 - **raw_data:** the data initially used to train Skua.

 The repository also contains `chrome_extension.zip`, a zipped version of the
 chrome_extension directory.
