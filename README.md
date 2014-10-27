Pinger
======

Service monitoring tool


Features
--------
* Pluggable (See plugins section)
* Unobtrusive (independent request intervals, parallel requests)


Installation
------------
```
$ pip install pinger
$ curl https://raw.githubusercontent.com/pedrospdc/pinger/master/config/example.json >> ~/pinger/config.json
$ vim ~/pinger/config.json
$ echo "export PINGER_SETTINGS=~/pinger/config.json" >> ~/.bashrc
$ source ~/.bashrc
$ pinger
```


Config
------
Pinger supports some few configurations by default. Configurations in *italic* are required.

| Param                | Description                                          | Default                   |
| ------------------   | ---------------------------------------------------- | ------------------------- |
| *default_interval*   | Default interval between requests.                   | 10                        |
| *default_timeout*    | Default timeout for requests.                        | 30                        |
| *main_process_sleep* | Main process sleep time.                             | 0.5                       |
| plugins              | Plugins list                                         | ['save_on_db']            |
| *websites*           | Websites list                                        | Check config/example.json |



Timeout and interval can be overwritten by each website if needed.

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

It's rather easy to create a plugin for Pinger. Check pinger/ext/`__init__`.py for some documentation and
I recommend taking a look at the existing plugins. Put your plugins in pinger/ext/plugins and add them to
the plugins section on your configuration.

*Available Plugins*
* stdout - Prints logs to stdout
* sqlite - Saves results into an sqlite database
* log - Logs results
