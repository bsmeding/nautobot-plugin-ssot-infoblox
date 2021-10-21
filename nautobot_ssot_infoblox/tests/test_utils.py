"""Util tests that do not require Django."""
import unittest
import os

from nautobot_ssot_infoblox.utils import get_vlan_view_name, nautobot_vlan_status

class TestUtils(unittest.TestCase):
    """Test Utils."""

    def test_vlan_view_name(self):
        """Test vlan_view_name util."""
        name = get_vlan_view_name(resource="vlan/ZG5zLnZsYW4kLmNvbS5pbmZvYmxveC5kbnMudmxhbl92aWV3JFZMVmlldzEuMTAuMjAuMTA:VLView1/VL10/10")
        assert name == "VLView1"
    
    def nautobot_vlan_status(self):
        """Test nautobot_vlan_status."""
        status = nautobot_vlan_status("Active")
        assert status == "ASSIGNED"