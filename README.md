# parking-lot

ParkingLot is a Python service imitating a parking lot like system.

The service indicates rather a vehicle allowed or not allowed to enter the parking lot.

## Installation

Please make sure you're having a Postgres DB on your machine.

```bash
pip install parkinglot
```

## Usage

```python
from parkinglot import ParkingLot

# By default, it create 'parkinglot' DB and 'entrances' table with given Postgres user and password.
# By default, user='postgres' and password='password'.
pl = ParkingLot()

# Check rather a vehicle is allowed or not allowed by given string like path to an image on your machine.
pl.check(...)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
