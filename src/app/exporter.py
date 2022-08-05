from kasa import exceptions
from prometheus_client import make_asgi_app, Gauge

from app.settings import Settings
from app.utils import get_device_reading

metrics_app = make_asgi_app()

voltage = Gauge(name='plug_measurements',
                documentation='Voltage measurements of smart plugs',
                unit="volts",
                labelnames=['location'])

current = Gauge(name='plug_measurements',
                documentation='Current measurements of smart plugs',
                unit="amperes",
                labelnames=['location'])

load = Gauge(name='plug_measurements',
             documentation='Power measurements of smart plugs',
             unit="watts",
             labelnames=['location'])


async def update_metrics(settings: Settings) -> None:
    """
    Updates the prometheus metrics with the current measurements
    :param settings: configurations with the current device list
    """
    for plug in settings.device_list:
        ip = plug['ip']
        alias = plug['alias']
        try:
            readings = await get_device_reading(ip)
            volts = readings['volt']
            amps = readings['ampere']
            watts = readings['watts']
        except exceptions.SmartDeviceException:
            volts = "nan"
            amps = "nan"
            watts = "nan"
        voltage.labels(alias).set(volts)
        current.labels(alias).set(amps)
        load.labels(alias).set(watts)
