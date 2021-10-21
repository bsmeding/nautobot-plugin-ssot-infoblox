"""Infoblox Models for Infoblox integration with SSoT plugin."""
from nautobot_ssot_infoblox.diffsync.models.base import Network, IPAddress, Vlan, VlanView


class InfobloxNetwork(Network):
    """Infoblox implementation of the Network Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Network object in Infoblox."""
        diffsync.conn.create_network(
            prefix=ids["prefix"], comment=attrs["description"] if attrs.get("description") else ""
        )
        return super().create(ids=ids, diffsync=diffsync, attrs=attrs)

    def update(self, attrs):
        """Update Network object in Infoblox."""
        self.diffsync.conn.update_network(
            prefix=self.get_identifiers()["prefix"], comment=attrs["description"] if attrs.get("description") else ""
        )
        return super().update(attrs)

    def delete(self):
        """Delete Network object in Infoblox."""
        self.diffsync.conn.delete_network(self.get_identifiers()["prefix"])
        return super().delete()


class InfobloxVLANView(VlanView):
    """Infoblox implementation of the VLANView Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create VLANView object in Infoblox."""
        return NotImplementedError


class InfobloxVLAN(Vlan):
    """Infoblox implementation of the VLAN Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create VLAN object in Infoblox."""
        return NotImplementedError


class InfobloxIPAddress(IPAddress):
    """Infoblox implementation of the VLAN Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """NO-OP IPAddresses are automatically created in Infoblox."""
        return NotImplementedError

    def update(self, attrs):
        """NO-OP Currently don't support updating Infoblox IPAddress."""
        return NotImplementedError

    def delete(self):
        """NO-OP IPAddresses cannot be deleted in Infoblox."""
        return NotImplementedError
