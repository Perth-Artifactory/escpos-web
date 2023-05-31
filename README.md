# escpos-web
Python based HTTP api for interaction with ESCPOS based printers. Basically just a web api for [python-escpos](https://github.com/python-escpos/python-escpos)

## Setup

* `pip install -r requirements.txt`
* `cp config.json.example config.json`
* Set `config.json` parameters
* Point to your printer
  * Find your vendor and device IDs using `lsusb`
  * `cp printer.py.example printer.py`
  * Add your IDs in place of `1234` in `printer.py`

## Usage

Send a post request to `/control` with a JSON serialised array of command dicts. (Check `client.py` for examples)

### Text

Command name: `text`

`data` parameters:

| Parameter | Type | Usage | Optional |
| --------- | ---- | ----- | -------- |
| `text`    | `str` | The text to print | Required |
| `size`    | `int` | The size of the text | Optional, defaults to `2` |
| `newline` | `boolean` | | Whether a newline should be printed at the end of the text | Optional, defaults to `true` |

### Image

Command name: `image`

`data` parameters:

| Parameter | Type | Usage | Optional |
| --------- | ---- | ----- | -------- |
| `image`   | `str` | The image to print. Must be either a local file mapped in `config.json` or a url. | Required |

### QR code

Command name: `qr`

`data` parameters:

| Parameter | Type | Usage | Optional |
| --------- | ---- | ----- | -------- |
| `text`    | `str` | The contents of the QR code | Required |

### Cutting

Command name: `cut`

`data` parameters:

* None