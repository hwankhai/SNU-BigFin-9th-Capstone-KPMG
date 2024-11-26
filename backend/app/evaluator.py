import os
from openai import OpenAI
import json
from typing import Dict, Any
import asyncio
from dotenv import load_dotenv
import deepl

class HallucinationEvaluator:
    def __init__(self):
        load_dotenv()
        openai_key = os.getenv("OPENAI_API_KEY")
        deepl_key = os.getenv("DEEPL_API_KEY")
        
        if not openai_key:
            raise ValueError("OpenAI API key not found in environment variables")
        if not deepl_key:
            raise ValueError("DeepL API key not found in environment variables")
            
        self.client = OpenAI(api_key=openai_key, timeout=30.0)
        self.translator = deepl.Translator(deepl_key)
        
        # Get the absolute path to the prompt directory
        self.prompt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt")
        
    def read_prompt(self, file_path: str) -> str:
        """
        Reads content from a text file and returns it as a string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None

    async def translate_to_korean(self, text: str) -> str:
        try:
            result = await asyncio.to_thread(
                lambda: self.translator.translate_text(text, target_lang="KO")
            )
            return str(result)
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text

    async def get_gpt_response(self, prompt: str) -> str:
        try:
            async with asyncio.timeout(25):
                response = await asyncio.to_thread(
                    lambda: self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a hallucination detection expert."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0,
                    )
                )
            return response.choices[0].message.content
        except asyncio.TimeoutError:
            error_msg = "평가 요청이 시간 초과되었습니다. 다시 시도해주세요."
            return error_msg
        except Exception as e:
            error_msg = f"평가 중 오류가 발생했습니다: {str(e)}"
            print(f"Error in get_gpt_response: {str(e)}")
            return error_msg

    async def evaluate(self, question: str, knowledge: str, answer: str) -> Dict[str, Any]:
        try:
            # Phase 1: Non-fabrication Hallucination Checking
            nonfabric_prompt = self.read_prompt(os.path.join(self.prompt_dir, 'nonfabricationhallucinationcheckingprompt.txt'))
            if not nonfabric_prompt:
                raise ValueError("Failed to read non-fabrication prompt")
            
            formatted_nonfabric_prompt = nonfabric_prompt.format(
                question=question,
                answer=answer
            )
            
            nonfabric_response = await self.get_gpt_response(formatted_nonfabric_prompt)
            has_nonfabric_hallucination = "NONE" in nonfabric_response
            
            # Phase 2: Knowledge-based Judgment
            judgment_prompt = self.read_prompt(os.path.join(self.prompt_dir, 'Judgment.txt'))
            if not judgment_prompt:
                raise ValueError("Failed to read judgment prompt")
            
            query_knowledge = f"#Query-1#: {question}\n#Knowledge-1#: {knowledge}"
            formatted_judgment_prompt = judgment_prompt.format(
                question=question,
                answer=answer,
                query_knowledge=query_knowledge
            )
            
            judgment_response = await self.get_gpt_response(formatted_judgment_prompt)
            has_judgment_hallucination = 'INCORRECT' in judgment_response or 'INCONCLUSIVE' in judgment_response
            
            # 결과 분석
            has_hallucination = has_nonfabric_hallucination or has_judgment_hallucination
            
            result = {
                "has_hallucination": has_hallucination,
                "explanation": judgment_response if has_judgment_hallucination else (
                    "질문과 관련이 없는 답변을 하는 할루시네이션" if has_nonfabric_hallucination else 
                    "할루시네이션이 감지되지 않았습니다."
                ),
                "details": {
                    "phase1_result": nonfabric_response,
                    "judgment_result": judgment_response if has_judgment_hallucination else None
                }
            }
            
            # 결과를 한국어로 번역
            translated_result = {
                "has_hallucination": result["has_hallucination"],
                "explanation": await self.translate_to_korean(result["explanation"]),
                "details": {
                    "phase1_result": await self.translate_to_korean(result["details"]["phase1_result"]),
                    "judgment_result": await self.translate_to_korean(result["details"]["judgment_result"]) if result["details"]["judgment_result"] else None
                }
            }
            
            return translated_result

        except asyncio.TimeoutError:
            error_msg = "평가 요청이 시간 초과되었습니다. 다시 시도해주세요."
            return {
                "has_hallucination": None,
                "explanation": error_msg,
                "details": {
                    "phase1_result": None,
                    "judgment_result": None
                }
            }
        except Exception as e:
            error_msg = f"평가 중 오류가 발생했습니다: {str(e)}"
            print(f"Error in evaluate: {str(e)}")
            return {
                "has_hallucination": None,
                "explanation": error_msg,
                "details": {
                    "phase1_result": None,
                    "judgment_result": None
                }
            }
