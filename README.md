Pinger
======

Website monitoring application


Features
--------
* Pluggable (See plugins section)
* Easy to install and configure
* Unobtrusive (independent request intervals, parallel requests)


Installation
------------
* Copy config/example.json to somewhere
* Edit the file as you will
* Set environment variable PINGER_SETTINGS setting to your configuration file
* Run pinger


Config
------
Pinger supports some few configurations by default. Configurations in bold are required.

| Param                | Description                                          | Default                   |
| ------------------   | ---------------------------------------------------- | ------------------------- |
| *default_interval*   | Default interval between requests.                   | 10                        |
| *default_timeout*    | Default timeout for requests.                        | 30                        |
| *main_process_sleep* | Main process sleep time.                             | 0.5                       |
| plugins              | Plugins list                                         | ['save_on_db']            |
| *websites*           | Websites list                                        | Check config/example.json |



Each website has a couple configurations that can overwrite the default configurations.

| Param                  | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| *name*                 | Website name                                         |
| *url*                  | Website URL                                          |
| *expected_content*     | Expected response content                            |
| *expected_status_code* | Expected response status code                        |
| timeout                | Overwrites global timetout                           |
| interval               | Overwrites global interval                           |


Plugins
=======

It's rather easy to create a plugin for Pinger. Check pinger/ext/__init__.py for some documentation and
I recommend taking a look at the existing plugins. Put your plugins in pinger/ext/plugins and add them to
the plugins section on your configuration.
