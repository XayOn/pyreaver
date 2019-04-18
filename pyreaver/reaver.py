"""Airdecap-ng."""
from .executor import ExecutorHelper
import asyncio


class Reaver(ExecutorHelper):
    """Reaver v1.6.5-git-21-gf8847d4 WiFi Protected Setup Attack Tool
    Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

    Options:
        --interface=<wlan>          Name of the monitor-mode interface to use
        --bssid=<mac>               BSSID of the target AP
        --mac=<mac>                 MAC of the host system
        --essid=<ssid>              ESSID of the target AP
        --channel=<channel>         Set the 802.11 channel for the interface (implies -f)
        --session=<file>            Restore a previous session file
        --exec=<command>            Execute the supplied command upon successful pin recovery
        --fixed                     Disable channel hopping
        --5ghz                      Use 5GHz 802.11 channels
        --verbose                   Display non-critical warnings (-vv or -vvv for more)
        --quiet                     Only display critical messages
        --help                      Show help
        --pin=<wps pin>             Use the specified pin (may be arbitrary string or 4/8 digit WPS pin)
        --delay=<seconds>           Set the delay between pin attempts [1]
        --lock-delay=<seconds>      Set the time to wait if the AP locks WPS pin attempts [60]
        --max-attempts=<num>        Quit after num pin attempts
        --fail-wait=<seconds>       Set the time to sleep after 10 unexpected failures [0]
        --recurring-delay=<x:y>     Sleep for y seconds every x pin attempts
        --timeout=<seconds>         Set the receive timeout period [10]
        --m57-timeout=<seconds>     Set the M5/M7 timeout period [0.40]
        --no-associate              Do not associate with the AP (association must be done by another application)
        --no-nacks                  Do not send NACK messages when out of order packets are received
        --dh-small                  Use small DH keys to improve crack speed
        --ignore-locks              Ignore locked state reported by the target AP
        --eap-terminate             Terminate each WPS session with an EAP FAIL packet
        --timeout-is-nack           Treat timeout as NACK (DIR-300/320)
        --ignore-fcs                Ignore frame checksum errors
        --win7                      Mimic a Windows 7 registrar [False]
        --pixie-dust                Run pixiedust attack
        --output-file=<filename>    Write packets of interest into pcap file
    """  # noqa

    command = 'reaver'
    sync = False
    requires_tempfile = False
    requires_tempdir = False

    async def run(self, *args, **kwargs):
        """Run async and update results"""
        asyncio.create_task(self.result_updater())
        return await super().run(*args, **kwargs)

    async def result_updater(self):
        """Set result on local object."""

        self.meta['result'] = {'lines': []}

        while not self.proc:
            await asyncio.sleep(1)

        while self.proc.returncode is None:
            line = (await self.proc.stdout.readline()).decode()
            self.meta['result']['lines'].append(line)
