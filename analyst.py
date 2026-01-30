import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(page_title="Gemini Analyst 429-Fix", page_icon="⚽")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Аналитик (Защита от перегрузки)")

with st.sidebar:
    api_key = st.text_input("Введите Google API Key", type="password")
    st.warning("Ошибка 429? Подождите 60 секунд — это ограничение бесплатного тарифа Google.")

match_input = st.text_input("Введите матч:")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите ключ!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Динамический выбор модели
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Берем самую легкую версию, чтобы меньше тратить квоту
            model_name = next((m for m in models if "flash" in m), models[0])
            
            # Пытаемся запустить поиск
            model = genai.GenerativeModel(
                model_name=model_name,
                tools=[{'google_search_retrieval': {}}]
            )
            
            with st.spinner('Подключаюсь к Google Search...'):
                query = f"Сегодня {today_date}. Найди последние новости и травмы матча {match_input} за январь 2026. Дай прогноз: П1/X/П2, счет, ставка. На русском."
                response = model.generate_content(query)
                st.success("Готово!")
                st.markdown(response.text)
                
        except Exception as e:
            if "429" in str(e):
                st.error("🛑 ЛИМИТ ИСЧЕРПАН. Google просит подождать 1 минуту.")
                # Показываем визуальный таймер
                bar = st.progress(0)
                for i in range(60):
                    time.sleep(1)
                    bar.progress((i + 1) / 60)
                st.info("🔄 Минута прошла! Попробуйте нажать кнопку еще раз.")
            else:
                st.error(f"Ошибка: {str(e)}")
