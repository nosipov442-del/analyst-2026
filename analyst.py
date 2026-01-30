import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(page_title="Gemini Analyst Pro", page_icon="⚽", layout="wide")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Спортивный Аналитик")
st.write(f"Сегодня: {today_date}")

with st.sidebar:
    api_key = st.text_input("Введите Google API Key", type="password")
    st.info("При ошибке 429 подождите 1 минуту.")

match_input = st.text_input("Матч для анализа:")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ!")
    elif not match_input:
        st.warning("Введите матч.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Включаем поиск Google
            tools = [{'google_search_retrieval': {}}]
            
            # Пробуем сначала Gemini 3, если нет - 1.5
            model_names = ['gemini-3-flash-preview', 'gemini-1.5-flash']
            
            success = False
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name=m_name, tools=tools)
                    
                    with st.spinner(f'Использую {m_name}. Ищу свежие данные...'):
                        query = (
                            f"Сегодня {today_date}. Используй Google Search. "
                            f"Найди актуальные новости на ЭТУ НЕДЕЛЮ про матч {match_input}. "
                            f"Дай прогноз: вероятности %, счет и ставку. Отвечай на русском."
                        )
                        response = model.generate_content(query)
                        
                        st.markdown("---")
                        st.success(f"Анализ готов (Модель: {m_name})")
                        st.markdown(response.text)
                        success = True
                        break # Если получилось, выходим из цикла
                except Exception as e:
                    if "429" in str(e):
                        continue # Пробуем следующую модель
                    else:
                        raise e
            
            if not success:
                st.error("Превышена квота запросов (Error 429). Пожалуйста, подождите 1-2 минуты и попробуйте снова.")

        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")
