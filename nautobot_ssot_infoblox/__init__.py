"""Plugin declaration for nautobot_ssot_infoblox."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.core.signals import nautobot_database_ready
from nautobot.extras.plugins import PluginConfig

from nautobot_ssot_infoblox.signals import infoblox_create_tag


class NautobotSSoTInfobloxConfig(PluginConfig):
    """Plugin configuration for the nautobot_ssot_infoblox plugin."""

    name = "nautobot_ssot_infoblox"
    verbose_name = "Nautobot SSoT Infoblox"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot SSoT Infoblox."
    base_url = "ssot-infoblox"
    required_settings = []
    min_version = "1.2.0"
    max_version = "1.9999"
    default_settings = {
        "enable_sync_to_infoblox": False,
        "enable_rfc1918_network_containers": False,
    }
    caching_config = {}

    def ready(self):
        super().ready()

        nautobot_database_ready.connect(infoblox_create_tag, sender=self)


config = NautobotSSoTInfobloxConfig  # pylint:disable=invalid-name
