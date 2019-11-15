from collections import deque
from openzwavemqtt import base


def test_direct_collection(options, caplog):
    class Level3(base.ZWaveBase):
        EVENT_ADDED = "level3_added"
        EVENT_CHANGED = "level3_change"
        EVENT_REMOVED = "level3_removed"

        @property
        def hello(self):
            return self.data.get("hello")

    class Level2(base.ZWaveBase):
        DIRECT_COLLECTION = "level3"
        EVENT_ADDED = "level2_added"
        EVENT_CHANGED = "level2_change"
        EVENT_REMOVED = "level2_removed"

        def create_collections(self):
            return {"level3": base.ItemCollection(self.options, self, Level3)}

    class Level1(base.ZWaveBase):
        DIRECT_COLLECTION = "level2"
        EVENT_ADDED = "level1_added"
        EVENT_CHANGED = "level1_change"
        EVENT_REMOVED = "level1_removed"

        def create_collections(self):
            return {"level2": base.ItemCollection(self.options, self, Level2)}

    level1 = Level1(options, None, None)
    level1.process_message(deque(["2", "3"]), {"hello": 1})
    assert level1.get_level2("2").get_level3("3").hello == 1

    # Only works on numbers
    level1.process_message(deque(["2", "a"]), {"hello": 1})
    assert level1.get_level2("2").get_level3("a") is None
    assert "cannot process message" in caplog.text
