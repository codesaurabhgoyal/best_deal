from src.discovery.demo import DemoDiscovery

def test_demo_discovery():
    d = DemoDiscovery()
    urls = d.discover_urls("Rolex 116610LN")
    assert len(urls) == 2
