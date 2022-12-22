# 🏰 PhishFort Counter-Phishing Lists

> Now protecting over 369 million users across the globe! 

This repository contains a blacklist and whitelist of domains maintained by [PhishFort](https://www.phishfort.com). These lists are used by the PhishFort Protect browser plugin ([Chrome](https://chrome.google.com/webstore/detail/phishfort-protect/bdiohckpogchppdldbckcdjlklanhkfc), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/protect/)), as well a number of third-party browser plugins and services to protect their users from crypto phishing attacks and scams.

## Blacklists

The blacklists directory contains two lists in JSON format:

-   A full list of blacklisted domains: [`domains.json`](blacklists/domains.json)
-   A "hot list" of recently blacklisted domains: [`hotlist.json`](blacklists/hotlist.json)

Teams are invited to openly pull from our [full blacklist](blacklists/domains.json) to ensure maximum coverage. However, in the case where performance or the size of the list is a concern (this list is always growing) we urge developers and/or teams to then consider consuming from our [hot list](blacklists/hotlist.json).

The hot list keeps a rolling window of 3 month detections (ie. items in the hotlist will only exist for 3 months). The **rolling window period is subject to change**. Although this should be ample time for PhishFort to execute a successful takedown on the site mentioned, we cannot guarantee that we will be executing takedowns on every single item in the list.

## Whitelists

The whitelist directory contains a number of lists we maintain for partner projects and internal reasons. We do not recommend consuming or making any assumptions based on this list.

## Use of CDN

Although we recommend loading directly from GitHub to maintain a perfect sync with the most up-to-date version of the PhishFort lists, significant performance improvements can be seen with using a CDN. For example by accessing the blacklist via jsdelivr CDN [here](https://cdn.jsdelivr.net/gh/phishfort/phishfort-lists@master/blacklists/domains.json).

**We cannot guarantee the integrity of lists downloaded via a 3rd party content delivery network. We recommend using the [PhishFort Public Blocklist API](https://lookup.phishfort.com/docs) instead of CDNs.**
