import sys
import asyncio

import pyreaver
import pyrcrack


# Requires pyrcrack for monitor mode. You can set monitor mode another way.
async def scan_for_targets():
    """Scan for targets, return json."""
    async with pyrcrack.AirmonNg() as airmon:
        interface = await airmon.set_monitor(sys.argv[-1])

        async with pyreaver.Wash() as wash:
            await wash.run(interface=interface[-1]['interface'])
            printed = []
            while True:
                await asyncio.sleep(1)
                for apo in wash.sorted_aps():
                    if apo not in printed:
                        print(apo)
            printed = wash.sorted_aps()


asyncio.run(scan_for_targets())
