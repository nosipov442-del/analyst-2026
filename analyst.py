import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="AI Analyst 2026", page_icon="⚽", layout="wide")

# Дата
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("🏆 Спортивный ИИ-Аналитик")
st.write(f"Модель: Gemini 3 Flash | Дата: {today_date}")

# Боковая панель
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите Google API Key", type="password")
    st.divider()
    st.info("Температура: 0 | Поиск: ВКЛ")

# Ввод данных
match_input = st.text_input("Введите матч (например: Реал - Бавария):")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Настройка строгости ответов
            generation_config = {
                "temperature": 0,
                "top_p": 1,
                "max_output_tokens": 2048,
            }

            model = genai.GenerativeModel(
                model_name='gemini-3-flash',
                generation_config=generation_config
            )
            
            with st.spinner('ИИ собирает данные из сети...'):
                # Упрощенный формат промпта для избежания SyntaxError
                text_query = f"Сегодня {today_date}. Ты проф. аналитик. Проанализируй матч {match_input}. Найди через поиск травмы, составы и форму. Дай прогноз счета, вероятности П1/X/П2 в % и лучшую ставку. Отвечай на русском. Не упоминай 2024 год."
                
                response = model.generate_content(text_query)
                
                st.markdown("---")
                st.success("Анализ готов!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")


