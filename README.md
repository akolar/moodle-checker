A tool for checking whether the contents of a Moodle classroom has changed.

## Usage

```
usage: moodle-checker.py [-h] [--timeout TIMEOUT] [--phonenumber PHONENUMBER]
                         domain id

tool for checking whether the contents of a Moodle classroom has been changed.

positional arguments:
  domain                domain of the moodle classroom (e.g. ucilnica.fmf.uni-
                        lj.si)
  id                    id of the class

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     seconds between sequential refreshes [default: 180]
  --phonenumber PHONENUMBER
                        phone number for receiving notifications
```

If you want to login into Moodle using your own credentials set export them as
```
export MOODLE_CREDENTIALS='<username>:<password>'
```

In order to send text messages using the najdi.si platform set your credentials as follows:
```
export NAJDISI_CREDENTIALS='<username>:<password>'
```

## Dependencies

- requests
- beautifulsoup4
- najdisi_sms
