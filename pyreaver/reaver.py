"""Airdecap-ng."""
from .executor import ExecutorHelper
import asyncio


class Reaver(ExecutorHelper):
    """Reaver v1.6.5-git-21-gf8847d4 WiFi Protected Setup Attack Tool
    Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

    Options:
        -i, --interface=<wlan>          Name of the monitor-mode interface to use
        -b, --bssid=<mac>               BSSID of the target AP
        -m, --mac=<mac>                 MAC of the host system
        -e, --essid=<ssid>              ESSID of the target AP
        -c, --channel=<channel>         Set the 802.11 channel for the interface (implies -f)
        -s, --session=<file>            Restore a previous session file
        -C, --exec=<command>            Execute the supplied command upon successful pin recovery
        -f, --fixed                     Disable channel hopping
        -5, --5ghz                      Use 5GHz 802.11 channels
        -v, --verbose                   Display non-critical warnings (-vv or -vvv for more)
        -q, --quiet                     Only display critical messages
        -h, --help                      Show help
        -p, --pin=<wps pin>             Use the specified pin (may be arbitrary string or 4/8 digit WPS pin)
        -d, --delay=<seconds>           Set the delay between pin attempts [1]
        -l, --lock-delay=<seconds>      Set the time to wait if the AP locks WPS pin attempts [60]
        -g, --max-attempts=<num>        Quit after num pin attempts
        -x, --fail-wait=<seconds>       Set the time to sleep after 10 unexpected failures [0]
        -r, --recurring-delay=<x:y>     Sleep for y seconds every x pin attempts
        -t, --timeout=<seconds>         Set the receive timeout period [10]
        -T, --m57-timeout=<seconds>     Set the M5/M7 timeout period [0.40]
        -A, --no-associate              Do not associate with the AP (association must be done by another application)
        -N, --no-nacks                  Do not send NACK messages when out of order packets are received
        -S, --dh-small                  Use small DH keys to improve crack speed
        -L, --ignore-locks              Ignore locked state reported by the target AP
        -E, --eap-terminate             Terminate each WPS session with an EAP FAIL packet
        -J, --timeout-is-nack           Treat timeout as NACK (DIR-300/320)
        -F, --ignore-fcs                Ignore frame checksum errors
        -w, --win7                      Mimic a Windows 7 registrar [False]
        -K, --pixie-dust                Run pixiedust attack
        -O, --output-file=<filename>    Write packets of interest into pcap file
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
        while not self.proc:
            await asyncio.sleep(1)

        self.meta['result'] = {'lines': []}

        while self.proc.returncode is None:
            lines = (await self.proc.communicate())[0].decode()
            self.meta['result']['lines'].update(lines.split('\n'))
