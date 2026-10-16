import requests
import time
# 引入您的基礎節點
from .base_api import BaseAPINode 

class MetronixWanVideoNode(BaseAPINode):
    """
    繼承 BaseAPINode，自動擁有 self.config 屬性
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "default": "A majestic dragon flying over snowy mountains, 8k resolution", 
                    "multiline": True
                }),
                "model": (["wan3.0-video", "wan3.0-video-prime"], {
                    "default": "wan3.0-video"
                }),
                "resolution": (["480P", "720P", "1080P"], {
                    "default": "720P"
                }),
            }
        }

    # 覆寫 BaseAPINode 的預設回傳名稱與分類 (如果您希望統一放 CustomAPI 也可以不覆寫 CATEGORY)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "Metronix API/Video"

    def generate_video(self, prompt, model, resolution):
        # 直接從基礎類別繼承來的 self.config 讀取 Key 與 Timeout
        api_key = self.config.get("METRONIX_API_KEY")
        if not api_key:
            return ("錯誤: config.json 中缺失 'METRONIX_API_KEY'。",)

        # 使用您 config 裡的預設超時設定，若無則預設為 30 秒
        timeout = self.config.get("DEFAULT_TIMEOUT", 30)

        base_url = "https://apigateway.metronixcloud.com/v1"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 1. 提交任務
        submit_url = f"{base_url}/videos"
        payload = {
            "model": model,
            "resolution": resolution,
            "prompt": prompt
        }
        
        print(f"[Metronix API] 提交任務中 ({model}, {resolution})...")
        try:
            # 加上 timeout 避免網路卡死
            response = requests.post(submit_url, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data.get("task_id")
            
            if not task_id:
                return ("錯誤: API 未返回任務 ID",)
            print(f"[Metronix API] 任務建立成功，Task ID: {task_id}")
            
        except Exception as e:
            return (f"任務提交失敗: {str(e)}",)

        # 2. 輪詢查詢狀態
        query_url = f"{base_url}/videos/{task_id}"
        
        while True:
            try:
                status_response = requests.get(query_url, headers=headers, timeout=timeout)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                
                if status == "success":
                    video_url = status_data.get("video_url")
                    print(f"[Metronix API] 影片生成成功！URL: {video_url}")
                    return (video_url,)
                elif status in ["failed", "error"]:
                    err_msg = status_data.get("message", "未知錯誤")
                    print(f"[Metronix API] 生成失敗: {err_msg}")
                    return (f"生成失敗: {err_msg}",)
                
                # 等待 5 秒後重試
                time.sleep(5)
                
            except Exception as e:
                return (f"狀態查詢異常: {str(e)}",)

# 將節點匯出供 __init__.py 註冊
NODE_CLASS_MAPPINGS = {
    "MetronixWanVideoNode": MetronixWanVideoNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MetronixWanVideoNode": "Metronix Wan3.0 Video"
}