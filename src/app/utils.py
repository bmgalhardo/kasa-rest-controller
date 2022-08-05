from kasa import SmartPlug, Discover
from pydantic import BaseModel


class Device(BaseModel):
    ip: str


class DeviceName(Device):
    name: str


async def get_all_devices(broadcast_ip: str) -> dict:
    """
    Retrieve all devices in a given network
    :param broadcast_ip: broadcast ip
    :return: list of devices
    """
    devices = await Discover.discover(target=broadcast_ip)
    devices_found = {}

    if devices:
        devices_found = [{
            "alias": devices[ip].alias,
            "ip": ip
        } for ip in devices]

    return devices_found


async def get_device_reading(ip: str) -> dict:
    """
    Retrieve measurements of a given device
    :param ip: device ip
    :return: dictionary with the measurements
    """
    p = SmartPlug(ip)
    await p.update()

    m = p.emeter_realtime
    volts = m['voltage_mv'] / 1000  # mV -> V
    amps = m['current_ma'] / 1000  # mA -> A
    watts = m['power_mw'] / 1000  # mW -> W

    data = {
        'volt': volts,
        'ampere': amps,
        'watts': watts,
    }
    return data



