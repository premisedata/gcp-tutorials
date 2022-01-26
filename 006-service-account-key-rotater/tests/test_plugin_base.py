from plugins.base import BasePlugin


class MockPlugin(BasePlugin):

    schema = {
            'key1': "value1",
            'key2': "value2"
        }
    type = "mock"
    valid_keys = []

    def initalize_backend(self, data, key):
        pass

    def update_key(self, data, key):
        pass

class TestPluginBase:
    def test_write_label(self):
        base = MockPlugin()
        label_key, key = base._write_label({},"")
        assert label_key == "mock0"
        assert key == "key1-_value1-_key2-_value2"
    
    def test_parse_label(self):
        label = "key1-_value1-_key2-_value2"
        base = MockPlugin()
        parsed_label = base.parse_label(label)
        assert parsed_label == base.schema