import google.generativeai as genai
from ..interface import BaseNLP


class GeminiNLP(BaseNLP):
    def __init__(self, gemini_client: genai):
        self.genai = gemini_client

    def chat(self, model_name, instructions, messages):
        model = self.genai.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        response = model.generate_content(messages)
        return response.text

    def struct_output(self, model_name, instructions, messages, structure):
        model = self.genai.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        response = model.generate_content(
            contents=messages,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": structure,
            },
        )
        return structure.model_validate_json(response.text)

    def func_call(self, model_name, messages, instructions, func):
        model = self.genai.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        try:
            response = model.generate_content(messages, tools=[func])
            call = response.candidates[0].content.parts[0].function_call

            if call:
                try:
                    result = func(**call.args)
                    return result
                except Exception as e:
                    args_dict = dict(call.args)
                    return f"Error when calling {call.name} with args {args_dict}: {e}"

        except Exception as e:
            return f"Error during model generation: {e}"

        return None
