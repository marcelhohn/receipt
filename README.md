# receipt

An application for generating receipt details of shopping baskets

## Prerequisites

- Python 3.7+

The application was only tested on Windows, but should work on other OS as well.
If using a different OS than Windows, some of the commands for installation may differ.

## Installation

This installation guide is written for Windows and assumes that the commands are excuted inside a powershell. For other OS use the corresponding commands.

### Clone the repository

```ps
git clone https://github.com/marcelhohn/receipt.git
```

### Change into the project directory

```ps
chdir receipt
```

### Optional: Create a virtual environment and activate it

This assumes python is in your `PATH`.

```ps
python -m venv env
.\env\Scripts\Activate.ps1
```

For other commands for activating the virtual environment depending on your platform and shell see [the python doumentation on venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

### Install the application

```ps
pip install .
```

## Usage

Run the application from anywhere on your system via

```ps
receipt input
```

where `input` is the path to the input file.

### Example

Assume we are in the same directory as the file `input.txt`, which has the following content:

```text
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85
```

Then running the application prints out the receipt details to the console:

```ps
> receipt input.txt
1 book: 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83
```

The application handles only one input file at once.

---

## Developer's guide

### Install dev dependencies

Create and activate a virtual environment as explained [above](#optional-create-a-virtual-environment-and-activate-it).

Install the package and its dependencies:

```ps
pip install -e .[dev] 
```

### Run the tests

```ps
python -m unittest
```
