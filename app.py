import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(page_title="Pixel Assistant", page_icon="🎨")
st.title("🎨 Pixel Assistant")
st.subheader("O teu assistente de Oficina Multimédia")

# Obter a chave API a partir dos segredos do Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configure a chave GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

# Definir a personalidade do Pixel
system_instruction = """
És o "Pixel", um assistente virtual jovem, criativo, prático e paciente para alunos da disciplina de Oficina Multimédia.
Falas de forma clara, utilizando analogias visuais e termos técnicos explicados de forma simples.
Ajudas em programas como Photoshop, Illustrator, Premiere, Audacity, GIMP e DaVinci Resolve.
Respondes a dúvidas sobre edição de imagem, áudio, vídeo, formatos de ficheiro e atalhos.
"""

# Inicializar o histórico da conversa na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt do utilizador
if prompt := st.chat_input("Como posso ajudar no teu projeto multimédia?"):
    # Guardar e exibir a mensagem do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta com a Gemini API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            chat_contents = [
                f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages
            ]

            response = client.models.generate_content(
                model="models/gemini-1.5-flash",
                contents=chat_contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro ao ligar ao Gemini: {e}")
