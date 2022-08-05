import os
import logging

from app.utils import get_all_devices


class Settings:

    def __init__(self):
        self.broadcast_ip = os.getenv('BROADCAST_IP', "192.168.1.255")
        self.update_period = int(os.getenv('UPDATE_PERIOD', "5"))
        self.discovery_period = int(os.getenv('DISCOVERY_PERIOD', "30"))
        self.device_list = []

    async def update_plug_list(self) -> None:
        """
        updates current devices in the network
        """
        devices = await get_all_devices(self.broadcast_ip)

        logging.info(devices)
        self.device_list = devices


settings = Settings()
