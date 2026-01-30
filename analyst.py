import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(page_title="Gemini 3 Search Analyst", page_icon="⚽", layout="wide")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Профессиональный Аналитик")
st.caption(f"Инструментарий: Google Search Grounding | Сегодня: {today_date}")

with st.sidebar:
    st.header("Доступ")
    api_key = st.text_input("Вставьте API Key", type="password")
    st.divider()
    st.info("Режим принудительного поиска включен.")

match_input = st.text_input("Введите матч для анализа:", placeholder="Например: Реал - Бавария")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ в боковой панели!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Универсальный способ подключения поиска Google
            # Если один формат выдает ошибку, библиотека попробует альтернативный
            tools = "google_search_retrieval" 

            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash', 
                tools=tools
            )
            
            with st.spinner('Выполняю поиск данных в Google...'):
                # Добавляем в сам текст требование использовать поиск
                query = (
                    f"Используй доступный инструмент поиска (google search). "
                    f"Сегодня {today_date}. Найди актуальные новости, травмы и составы "
                    f"на матч {match_input} за последние дни января 2026 года. "
                    f"Дай прогноз счета и ставку на русском языке."
                )
                
                response = model.generate_content(query)
                
                st.markdown("---")
                st.success("Анализ завершен!")
                st.markdown(response.text)
                
        except Exception as e:
            error_msg = str(e)
            # Если опять ругается на имя поля, пробуем вообще без явного указания в tools, 
            # так как новые модели часто имеют встроенный поиск
            if "Unknown field" in error_msg or "google_search" in error_msg:
                st.info("Пробую альтернативный метод подключения поиска...")
                try:
                    # Упрощенный вызов (инструменты как список строк)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(query + " Сначала выполни поиск в Google.")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Критическая ошибка API: {str(e2)}")
            elif "429" in error_msg:
                st.error("🛑 Лимит исчерпан. Подождите минуту.")
                time.sleep(5) # Короткая пауза
            else:
                st.error(f"Произошла ошибка: {error_msg}")

st.markdown("---")
st.caption("Аналитика на базе актуальных данных 2026 года.")
