# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing

class DeFiCircuitBreaker(gl.Contract):
    is_paused: bool
    last_analysis_reason: str

    def __init__(self):
        self.is_paused = False
        self.last_analysis_reason = "Initialized"

    @gl.public.view
    def get_status(self) -> bool:
        return self.is_paused

    @gl.public.write
    def run_health_check(self, token: str, news_data: str) -> typing.Any:
        
        def analyze_news() -> typing.Any:
            task = f"""
            Analyze the following news about {token}:
            {news_data}
            
            Return JSON only: {{"status": "DANGER" or "SAFE", "reason": "..."}}
            """
            
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            return json.loads(result)

        # Используем strict_eq для консенсуса по анализу
        result_json = gl.eq_principle.strict_eq(analyze_news)

        if result_json["status"] == "DANGER":
            self.is_paused = True
            self.last_analysis_reason = result_json["reason"]
        else:
            self.is_paused = False
            self.last_analysis_reason = "Safe"

        return result_json
