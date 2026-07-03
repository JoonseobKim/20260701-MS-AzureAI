import gradio as gr
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

# 1. STT API 호출 로직 (본인의 Azure API 정보로 수정하세요)
def request_stt(audio_path):
    if audio_path is None:
        return ""
    

    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    # [주의] 본인의 엔드포인트와 키를 입력하세요
    endpoint = os.getenv("SPEECH_ENDPOINT")
    api_key = os.getenv("SPEECH_KEY")
    
    with open(audio_path, "rb") as audio:
        audio_data = audio.read()
        
    headers = {
        'Content-Type': 'audio/wav',
        'Ocp-Apim-Subscription-Key': api_key
    }
    
    # API 요청
    try:
        response = requests.post(endpoint, headers=headers, data=audio_data)
        response_json = response.json()
        
        # 결과 처리
        if response_json.get('RecognitionStatus') == 'Success':
            return response_json.get('NBest')[0].get('Display')
        else:
            return "변환 실패"
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 2. Gradio UI 구성
with gr.Blocks() as demo:
    gr.Markdown("# STT 실습 페이지")
    
    with gr.Column():
        input_mic = gr.Audio(
            label="마이크 입력", 
            sources="microphone", 
            type="filepath"
        )
        output_textbox = gr.Textbox(
            label="변환된 텍스트", 
            placeholder="여기에 결과가 출력됩니다."
        )
    
    # 마이크 입력 시 이벤트 연결
    input_mic.change(
        fn=request_stt, 
        inputs=[input_mic], 
        outputs=[output_textbox]
    )

if __name__ == "__main__":
    demo.launch()