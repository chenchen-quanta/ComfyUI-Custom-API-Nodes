import json
import os

class BaseAPINode:
    def __init__(self):
        base_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(base_path, "config.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    CATEGORY = "CustomAPI"