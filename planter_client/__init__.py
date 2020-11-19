import api
from sense_hat import SenseHat
from pathlib import Path
import json
import click
import os

API_KEY = os.getenv("PLANTER_API_KEY")
ROOT_URL = os.getenv("PLANTER_ROOT_URL")

class Client():
    def __init__(self, apikey:str, root_url:str, name:str=None, location:str=None):
        self.client = planter.Client(apikey, root_url)
        self.sense = SenseHat()

        planter_root = Path("/.planter-client")
        conf_path = planter_root / "config.json"
        if conf.is_file():
            with open(conf_path, "r") as f:
                self.conf = json.load(f)
        
        else:
            if name is None or location is None:
                raise(("No config file, new sensor must be created."
                        "Please provide name and location of new sensor"
                ))
            planter_root.mkdir()
            response = self.add_sensor(name, location)
            self.conf = response["result"]
            with open(planter_root / "config.json", "w") as f:
                json.dump(self.conf, f)

        self.sensor_id = self.conf["id"]
        self.name = self.conf["name"]
        self.location = self.conf["location"]

    def add_sensor(self, name:str, location:str):
        return self.client.add_sensor(name, location)

    def add_reading(self):
        self.reading = {"temperature": sense.get_temperature(),
                        "pressure": sense.get_pressure(),
                        "humidity": sense.get_humidity(),
        }
        self.client.add_reading(**self.reading)
    
@click.group()
def cli():
    pass

@click.command()
@click.argument('name')
@click.argument('location')
def init(name, location):
    click.echo("Initialising new sensor")
    client = Client(API_KEY, ROOT_URL, name, location)
    sensor_id = client.sensor_id
    click.echo(f"New sensor added with id {sensor_id}")

@click.command()
def take_reading():
    click.echo("Taking a reading...")
    client = Client(API_KEY, ROOT_URL)
    client.add_reading()
    click.echo("""New reading made!
                Temperature: {temperature}, 
                Humidity: {humidity}, 
                Pressure: {pressure}
                """.format(**client.reading)
                )
