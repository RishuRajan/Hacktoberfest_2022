# Twitter Follower Factory analysis script

This Python script was inspired by the New York Times' [Follower Factory article](https://www.nytimes.com/interactive/2018/01/27/technology/social-media-bots.html), which showed that Twitter accounts can be analyzed to discover whether someone has purchased fake followers for that account. This script enables you to analyze any Twitter account and generate a similar scatter plot visualization of their followers. You can typically tell when someone purchased fake followers for an account when there are solid lines of followers that were created around the same time, as shown in the New York Times article.

**Note that you can [execute the code in this notebook on Binder](https://mybinder.org/v2/gh/rhiever/Data-Analysis-and-Machine-Learning-Projects/master?filepath=follower-factory%2FTwitter%2520Follower%2520Factory.ipynb) - no local installation required.**

## Dependencies

You will need to install Python's [python-twitter](https://github.com/sixohsix/twitter/) library:

    pip install twitter

You will also need to create an app account on https://dev.twitter.com/apps

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions

Following these steps will create 4 tokens that you will need to place in the script, as discussed below.

## Usage

Before you can run this script, you need to fill in the following 5 variables in the file:

```Python
USER_TO_ANALYZE = ''
OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
```

`USER_TO_ANALYZE` is straightforward: If you want to analyze my Twitter account, you would enter `randal_olson` in between the two single quotes.

Once you've created the Twitter app account as described under the Dependencies section, you should be able to find the OAUTH and CONSUMER keys on the "Key and Access Tokens" section, as shown in the image below.

<img src='images/twitter-app-example.png' />

Once you've filled out those 5 variables, the script below will handle the rest.

If you're analyzing an account with 100,000s or more of followers, running the script may take a while as the script follows the Twitter API's usage restrictions. A progress bar will keep you updated on the progress of the analysis.

Once the script finishes, it will save an image to the directory that you ran the script in. That image will contain the scatter plot visualization for the account you targeted.

## Security concerns

Although you should be fine with this notebook, you should beware of placing private API keys and security-related information into scripts like this one. If you're particularly paranoid about the security of your Twitter account, you are welcome to review the code below and all of the open source libraries that it relies upon.

If it looks like anything fishy is going on with the API keys, please don't hesitate to [file an issue on this repository](https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/issues/new) and raise your concerns.

## Questions and Comments

If you have any questions or comments, please [file an issue on this repository](https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/issues/new) and I'll get back to you as soon as I can. If you'd like to submit a pull request to improve this script in any way, please file an issue first to discuss your change(s). I'm generally open to accepting pull requests on this repository.
%matplotlib inline
from __future__ import print_function
import time
from datetime import datetime
import os

from twitter import Twitter, OAuth, TwitterHTTPError
from tqdm import tqdm_notebook as tqdm
import pandas as pd
import matplotlib.pyplot as plt

USER_TO_ANALYZE = ''
OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

twitter_connection = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

pbar = tqdm()
pbar.write('Collecting list of Twitter followers for @{}'.format(USER_TO_ANALYZE))

rl_status = twitter_connection.application.rate_limit_status()
if rl_status['resources']['followers']['/followers/ids']['remaining'] <= 0:
    sleep_until = rl_status['resources']['followers']['/followers/ids']['reset']
    sleep_for = int(sleep_until - time.time()) + 10 # wait a little extra time just in case
    if sleep_for > 0:
        pbar.write('Sleeping for {} seconds...'.format(sleep_for))
        time.sleep(sleep_for)
        pbar.write('Awake!')

followers_status = twitter_connection.followers.ids(screen_name=USER_TO_ANALYZE)
followers = followers_status['ids']
next_cursor = followers_status['next_cursor']
pbar.update(len(followers))

while next_cursor != 0:
    rl_status = twitter_connection.application.rate_limit_status()
    if rl_status['resources']['followers']['/followers/ids']['remaining'] <= 0:
        sleep_until = rl_status['resources']['followers']['/followers/ids']['reset']
        sleep_for = int(sleep_until - time.time()) + 10 # wait a little extra time just in case
        if sleep_for > 0:
            pbar.write('Sleeping for {} seconds...'.format(sleep_for))
            time.sleep(sleep_for)
            pbar.write('Awake!')

    followers_status = twitter_connection.followers.ids(screen_name=USER_TO_ANALYZE, cursor=next_cursor)
    # Prevent duplicate Twitter user IDs
    more_followers = [follower for follower in followers_status['ids'] if follower not in followers]
    followers += more_followers
    next_cursor = followers_status['next_cursor']

    pbar.update(len(more_followers))

pbar.close()

pbar = tqdm(total=len(followers))
pbar.write('Collecting join dates of Twitter followers for @{}'.format(USER_TO_ANALYZE))
followers_created = list()

rl_status = twitter_connection.application.rate_limit_status()
remaining_calls = rl_status['resources']['users']['/users/lookup']['remaining']

for base_index in range(0, len(followers), 100):
    if remaining_calls == 50:
        # Update the remaining calls count just in case
        rl_status = twitter_connection.application.rate_limit_status()
        remaining_calls = rl_status['resources']['users']['/users/lookup']['remaining']

    if remaining_calls <= 0:
        sleep_until = rl_status['resources']['users']['/users/lookup']['reset']
        sleep_for = int(sleep_until - time.time()) + 10 # wait a little extra time just in case
        if sleep_for > 0:
            pbar.write('Sleeping for {} seconds...'.format(sleep_for))
            time.sleep(sleep_for)
            pbar.write('Awake!')
            rl_status = twitter_connection.application.rate_limit_status()
            remaining_calls = rl_status['resources']['users']['/users/lookup']['remaining']

    remaining_calls -= 1

    # 100 users per request
    user_info = twitter_connection.users.lookup(user_id=list(followers[base_index:base_index + 100]))
    followers_created += [x['created_at'] for x in user_info]

    pbar.update(len(followers[base_index:base_index + 100]))

pbar.close()
print('Creating Follower Factory visualization for @{}'.format(USER_TO_ANALYZE))

days_since_2006 = [(x.year - 2006) * 365 + x.dayofyear for x in pd.to_datetime(followers_created)]

mpl_style_url = 'https://gist.githubusercontent.com/rhiever/d0a7332fe0beebfdc3d5/raw/1b807615235ff6f4c919b5b70b01a609619e1e9c/tableau10.mplstyle'
alpha = 0.1 * min(9, 80000. / len(days_since_2006))
with plt.style.context(mpl_style_url):
    plt.figure(figsize=(9, 12))
    plt.scatter(x=range(len(days_since_2006)), y=days_since_2006[::-1], s=2, alpha=alpha)
    plt.yticks(range(0, 365 * (datetime.today().year + 1 - 2006), 365), range(2006, datetime.today().year + 1))
    plt.xlabel('Follower count for @{}'.format(USER_TO_ANALYZE))
    plt.ylabel('Date follower joined Twitter')
    plt.savefig('{}-follower-factory.png'.format(USER_TO_ANALYZE))

print('Follower Factory visualization saved to {}'.format(os.getcwd()))
