"""Walsh."""
from contextlib import suppress
import asyncio
import json

from .executor import ExecutorHelper
from .models import AccessPoint


class Wash(ExecutorHelper):
    """
    Wash v1.6.5-git-21-gf8847d4 WiFi Protected Setup Scan Tool
    Copyright (c) 2011, Tactical Network Solutions, Craig Heffner


    Options:
        --interface=<iface>              Interface to capture packets on
        --file [FILE1 FILE2 FILE3 ...]   Read packets from capture files
        --channel=<num>                  Channel to listen on [auto]
        --probes=<num>                   Maximum number of probes to send
        --ignore-fcs                     Ignore frame checksum errors
        --2ghz                           Use 2.4GHz 802.11 channels
        --5ghz                           Use 5GHz 802.11 channels
        --scan                           Use scan mode
        --survey                         Use survey mode [default]
        --all                            Show all APs, even those without
        --json                           print extended WPS info as json
        --utf8                           Show UTF8 ESSID
        --progress                       Show percentage of crack progress
        --help                           Show help
    """

    command = 'wash'
    sync = False
    requires_tempfile = False
    requires_tempdir = False

    async def run(self, *args, **kwargs):
        """Run async, with json mode"""
        if not ('json' in kwargs or 'j' in kwargs):
            kwargs.pop('j', None)
            kwargs['json'] = True
        asyncio.create_task(self.result_updater())
        return await super().run(*args, **kwargs)

    async def result_updater(self):
        """Set result on local object."""
        while not self.proc:
            await asyncio.sleep(1)

        self.meta['result'] = {'aps': []}

        while self.proc.returncode is None:
            with suppress(json.JSONDecodeError):
                self.meta['result']['aps'].append(
                    AccessPoint(
                        **json.loads(await self.proc.stdout.readline())))

    def sorted_aps(self):
        """Return sorted aps by score."""
        return sorted(
            self.meta['result']['aps'], key=lambda x: x.score, reverse=True)
