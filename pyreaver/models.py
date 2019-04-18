"""Models."""
from dataclasses import dataclass


@dataclass
class AccessPoint:
    """Represents an AP, as outputted by wash."""
    bssid: str
    essid: str
    channel: str
    rssi: str
    vendor_oui: str
    wps_version: str
    wps_state: str
    wps_locked: str
    wps_manufacturer: str
    wps_model_name: str
    wps_model_number: str
    wps_device_name: str
    wps_serial: str
    wps_uuid: str
    wps_response_type: str
    wps_primary_device_type: str
    wps_config_methods: str
    wps_rf_bands: str = None
    dummy: str = None
    wps_selected_registrar: str = None

    @property
    def score(self):
        """**Kinda-hackability** orientative score.

        TODO: add wps version, state etc here.
        """
        power_score = -float(self.rssi) / 100
        total_score = power_score
        return round((total_score / 1) * 100)
