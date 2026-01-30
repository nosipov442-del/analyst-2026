import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(page_title="Gemini 3 Search Analyst", page_icon="⚽", layout="wide")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Профессиональный Аналитик")
st.caption(f"Инструментарий: Google Search v2 | Сегодня: {today_date}")

with st.sidebar:
    st.header("Доступ")
    api_key = st.text_input("Вставьте API Key", type="password")
    st.divider()
    st.info("Используется обновленный метод поиска 'google_search'.")

match_input = st.text_input("Введите матч для анализа:", placeholder="Например: Челси - Ливерпуль")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ в боковой панели!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Настройка обновленного инструмента поиска 2026 года
            # Заменяем старый google_search_retrieval на новый google_search
            tools = [{'google_search': {}}]

            # Выбор модели
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash', # Используем стабильную версию для поиска
                tools=tools
            )
            
            with st.spinner('Выполняю глубокий поиск данных в Google...'):
                query = (
                    f"Сегодня {today_date}. Ты — аналитик. Найди актуальную информацию "
                    f"о матче {match_input}: травмы, составы, последние игры за январь 2026. "
                    f"Дай прогноз счета и ставку. Отвечай на русском."
                )
                
                response = model.generate_content(query)
                
                st.markdown("---")
                st.success("Анализ завершен успешно!")
                st.markdown(response.text)
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("🛑 Лимит запросов исчерпан. Подождите минуту.")
                timer_placeholder = st.empty()
                for i in range(60, 0, -1):
                    timer_placeholder.write(f"⏳ Повторная попытка возможна через {i} сек.")
                    time.sleep(1)
                timer_placeholder.write("✅ Можно пробовать снова!")
            elif "400" in error_msg:
                st.error(f"Ошибка конфигурации (400): {error_msg}")
                st.info("Попробуйте обновить библиотеку: pip install -U google-generativeai")
            else:
                st.error(f"Произошла ошибка: {error_msg}")

st.markdown("---")
st.caption("Данные подтягиваются напрямую из поиска Google.")
