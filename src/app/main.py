import uvicorn
import logging

from fastapi import FastAPI, status, HTTPException
from kasa import SmartPlug, exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.exporter import metrics_app, update_metrics
from app.settings import settings
from app.utils import Device, get_device_reading, get_all_devices, DeviceName

app = FastAPI()
app.mount("/metrics", metrics_app)

logging.basicConfig(level=logging.INFO)


@app.get("/discover")
async def discover_devices():
    """
    Find all devices in the network through broadcast
    :return: list of devices
    """
    devices = await get_all_devices(settings.broadcast_ip)
    return devices


@app.post("/readings")
async def get_reading(device: Device):
    """
    Get smart device metrics
    :param device: device ip
    :return: dictionary with the measurements
    """
    try:
        readings = await get_device_reading(device.ip)
        return readings
    except exceptions.SmartDeviceException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/switch", status_code=status.HTTP_201_CREATED)
async def toggle_switch(device: Device):
    """
    Toggle the power state of a given device. on->off OR off->on
    :param device: device ip
    :return: current state of the device
    """
    p = SmartPlug(device.ip)
    try:
        await p.update()
        if p.is_on:
            await p.turn_off()
            return {'on': False}
        else:
            await p.turn_on()
            return {'on': True}
    except exceptions.SmartDeviceException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/label", status_code=status.HTTP_201_CREATED)
async def change_label(device_name: DeviceName):
    """
    Change the label of given device.
    This alias will be assigned the label <location> in prometheus metrics
    :param device_name: device ip and chosen name
    :return: device chosen name
    """
    p = SmartPlug(device_name.ip)
    try:
        await p.update()
        await p.set_alias(device_name.name)
        return {"name": device_name.name}
    except exceptions.SmartDeviceException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/info")
async def get_info(device: Device):
    """
    Retrieve device information
    :param device: device ip
    :return: dictionary with relevant device info
    """
    p = SmartPlug(device.ip)
    try:
        await p.update()
        return p.sys_info
    except exceptions.SmartDeviceException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.on_event("startup")
async def startup_event():
    """
    In server startup, start running the discovery and updates in parallel
    """
    logging.info('starting background tasks')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_metrics, 'interval', [settings], seconds=settings.update_period)
    scheduler.add_job(settings.update_plug_list, 'interval', seconds=settings.discovery_period)
    scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
