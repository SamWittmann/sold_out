# sold_out
A Python purchasing bot for automating buying clothing from Supreme's webstore using the Selenium library.

***IMPORTANT NOTE***
The webstore may require you to fill out a Captcha when it tries to checkout. You should make sure you're watching the browsing window that opens so that you can fill out a Captcha if it appears, as the bot cannot complete them.
***/IMPORTANT NOTE***

The actual script is located in script/sold_out.py. 

The top of the script contains 3 dictionaries, which you must fill out according to the comments next to each field. 

Once you've filled out these dictionaries, execute the script, and it will automatically carry out the requested purchase on the next Thursday at 11AM EST (the time when Supreme's webstore updates).

Note that currently the script can only support purchasing a single item at a time.

I would recommend finding a link to the item you're after - the script will execute faster if you can give it a direct link, and there's less chance for failure from a misspelled name or color.

