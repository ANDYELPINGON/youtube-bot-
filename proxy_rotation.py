"""Simple proxy rotation module for testing purposes"""

class ProxyRotator:
    """Simple proxy rotator class"""
    
    def __init__(self):
        self.proxies = [
            "proxy1.example.com:8080",
            "proxy2.example.com:8080", 
            "proxy3.example.com:8080"
        ]
        self.current_index = 0
    
    def get_next_proxy(self):
        """Get the next proxy in rotation"""
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy