# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing

class DeFiCircuitBreaker(gl.Contract):
    is_paused: bool

    def __init__(self):
        self.is_paused = False

    @gl.public.write
    def run_health_check(self, token: str, news_data: str) -> typing.Any:
        
        def analyze_news() -> typing.Any:
            # Жесткий промпт, исключающий вариативность
            task = f"""
            Analyze the following text regarding {token}: "{news_data}".
            If it contains any hint of danger, hack, or exploit, return exactly: {{"status": "DANGER"}}
            Otherwise, return exactly: {{"status": "SAFE"}}
            Output only the JSON object. Do not add any extra fields, explanations, or markdown.
            """
            
            # Исполнение и первичная очистка
            result = gl.nondet.exec_prompt(task).strip()
            result = result.replace("```json", "").replace("```", "").strip()
            
            return json.loads(result)

        # Применение консенсуса к бинарному результату
        result_json = gl.eq_principle.strict_eq(analyze_news)

        # Обновление состояния
        self.is_paused = (result_json["status"] == "DANGER")
        
        return result_json

    @gl.public.view
    def get_status(self) -> dict[str, typing.Any]:
        return {
            "is_paused": self.is_paused
        }
