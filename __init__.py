from .wan_api import MetronixWanVideoNode

# ComfyUI 類別映射字典 (內部識別用的 Key : 節點 Class)
NODE_CLASS_MAPPINGS = {
    "MetronixWanVideoNode": MetronixWanVideoNode
}

# ComfyUI UI 介面上顯示的名稱 mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "MetronixWanVideoNode": "Metronix Wan3.0 Video Generator"
}

# 導出 mappings 讓 ComfyUI 自動加載
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]