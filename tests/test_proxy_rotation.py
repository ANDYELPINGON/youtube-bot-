import pytest
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import proxy_rotation


class TestProxyRotator:
    """Test the ProxyRotator class"""
    
    def test_init(self):
        """Test ProxyRotator initialization"""
        rotator = proxy_rotation.ProxyRotator()
        
        assert hasattr(rotator, 'proxies')
        assert hasattr(rotator, 'current_index')
        assert isinstance(rotator.proxies, list)
        assert len(rotator.proxies) > 0
        assert rotator.current_index == 0
    
    def test_get_next_proxy(self):
        """Test getting the next proxy in rotation"""
        rotator = proxy_rotation.ProxyRotator()
        
        # Get first proxy
        first_proxy = rotator.get_next_proxy()
        assert first_proxy == rotator.proxies[0]
        assert rotator.current_index == 1
        
        # Get second proxy
        second_proxy = rotator.get_next_proxy()
        assert second_proxy == rotator.proxies[1]
        assert rotator.current_index == 2
    
    def test_proxy_rotation_cycle(self):
        """Test that proxy rotation cycles back to the beginning"""
        rotator = proxy_rotation.ProxyRotator()
        num_proxies = len(rotator.proxies)
        
        # Get all proxies once
        proxies_first_cycle = []
        for i in range(num_proxies):
            proxies_first_cycle.append(rotator.get_next_proxy())
        
        # Should cycle back to the beginning
        assert rotator.current_index == 0
        
        # Get first proxy of second cycle
        first_proxy_second_cycle = rotator.get_next_proxy()
        assert first_proxy_second_cycle == proxies_first_cycle[0]
    
    def test_proxy_format(self):
        """Test that proxies are in the expected format"""
        rotator = proxy_rotation.ProxyRotator()
        
        for proxy in rotator.proxies:
            assert isinstance(proxy, str)
            assert ':' in proxy  # Should have host:port format
            parts = proxy.split(':')
            assert len(parts) == 2
            assert parts[1].isdigit()  # Port should be numeric