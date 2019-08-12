# DESCRIPTION

- Exports clockify reports of an entire workspace to google drive spreadsheets
- Send periodic reports to coworkers about their time registers, using telegram
- Send telegram alerts if a clock is running for more than certain time

The scripts are intended to be hosted in a VPS, and be triggered with cron tasks


# HOW TO USE
## DEPLOY SCRIPTS IN VPS
## FILL CREDENTIALS AND OTHER SETTINGS
## CREATE VIRTUAL ENVIORMENT WITH PIPENV
## SETUP CRON TASKS

`crontab -e`
E.g.:

`0 20 * * 6  /opt/software/clockify2gdrive/.venv/bin/python /opt/software/clockify2gdrive/send_individual_summaries.py`
`0 3 1 * *  /opt/software/clockify2gdrive/.venv/bin/python /opt/software/clockify2gdrive/generate_report.py`


# REFERENCES
- https://clockify.github.io/clockify_api_docs/  (deprecated but working)
- https://developers.google.com/sheets/api/quickstart/python
