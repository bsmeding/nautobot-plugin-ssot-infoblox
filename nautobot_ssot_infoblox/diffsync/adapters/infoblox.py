"""Infoblox Adapter for Infoblox integration with SSoT plugin."""
from diffsync import DiffSync
from nautobot_ssot_infoblox.diffsync.client import InfobloxApi
from nautobot_ssot_infoblox.diffsync.models.infoblox import (
    InfobloxIPAddress,
    InfobloxNetwork,
    InfobloxVLANView,
    InfobloxVLAN,
)


class InfobloxAdapter(DiffSync):
    """DiffSync adapter using requests to communicate to Infoblox server."""

    prefix = InfobloxNetwork
    ipaddress = InfobloxIPAddress
    vlangroup = InfobloxVLANView
    vlan = InfobloxVLAN

    top_level = ["prefix", "ipaddress", "vlangroup", "vlan"]

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Infoblox.

        Args:
            job (object, optional): Infoblox job. Defaults to None.
            sync (object, optional): Infoblox DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync
        self.conn = InfobloxApi()
        self.subnets = []

    def load_prefixes(self):
        """Method to load InfobloxNetwork DiffSync model."""
        for _pf in self.conn.get_all_subnets():
            self.subnets.append(_pf["network"])
            new_pf = self.prefix(
                network=_pf["network"],
                description=_pf["comment"] if _pf.get("comment") else "",
            )
            self.add(new_pf)

    def load_ipaddresses(self):
        """Method to load InfobloxIPAddress DiffSync model."""
        for _prefix in self.subnets:
            for _ip in self.conn.get_all_ipv4address_networks(prefix=_prefix):
                new_ip = self.ipaddress(
                    address=_ip["ip_address"],
                    prefix=_ip["network"],
                    status=self.conn.get_ipaddr_status(_ip),
                    description=_ip["comment"],
                )
                self.add(new_ip)

    def load_vlanviews(self):
        """Method to load InfobloxVLANView DiffSync model."""
        for _vv in self.conn.get_vlanviews():
            new_vv = self.vlangroup(
                name=_vv["name"],
                description=_vv["comment"] if _vv.get("comment") else "",
            )
            self.add(new_vv)

    def load_vlans(self):
        """Method to load InfoblocVlan DiffSync model."""
        for _vlan in self.conn.get_vlans():
            new_vlan = self.vlan(
                name=_vlan["name"],
                vid=_vlan["id"],
                status=_vlan["status"],
                description=_vlan["comment"] if _vlan.get("comment") else "",
            )
            self.add(new_vlan)

    def load(self):
        """Method for one stop shop loading of all models."""
        self.load_prefixes()
        self.load_ipaddresses()
        self.load_vlanviews()
        self.load_vlans()
