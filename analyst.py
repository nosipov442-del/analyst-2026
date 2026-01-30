import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="Gemini 3 Аналитик", page_icon="⚽")

st.title("⚽ ИИ-Аналитик 2026")
st.caption(f"Сегодня: {datetime.now().strftime('%d.%m.%Y')} | Модель: Gemini 3 Flash")

# Ввод API ключа в боковой панели
with st.sidebar:
    api_key = st.text_input("Введите Google API Key", type="password")
    st.info("Температура установлена на 0 для точности.")

match_input = st.text_input("Матч для анализа:", placeholder="Например: Манчестер Сити - Ливерпуль")

if st.button("🚀 Получить прогноз"):
    if not api_key:
        st.error("Введите API ключ!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Настройка модели (Temperature 0)
            model = genai.GenerativeModel(
                model_name='gemini-3-flash',
                generation_config={"temperature": 0}
            )
            
            with st.spinner('Ищу данные и считаю вероятности...'):
                # Формируем промпт аккуратно
                prompt = f"""
                Сегодня {datetime.now().strftime('%d.%m.%Y')}. Ты профессиональный аналитик.
                Проведи анализ матча: {match_input}.
                Используй поиск для получения текущих составов и формы.
                Выдай: вероятности П1/X/П2, прогноз счета и лучшую ставку.
                Не упоминай 2024 год, сейчас 2026-й.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Ошибка: {e}")
                (Опиши текущее состояние команд и важные потери в составах)
                
                ###

