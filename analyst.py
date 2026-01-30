import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="Gemini AI Analyst", page_icon="⚽", layout="wide")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Автономный ИИ-Аналитик")
st.caption(f"Текущая дата: {today_date} | Режим: Автоподбор модели")

# Боковая панель
with st.sidebar:
    api_key = st.text_input("Введите Google API Key", type="password")
    st.divider()
    st.info("Код автоматически определит доступную модель в вашем регионе.")

def get_working_model():
    """Функция для поиска активной модели в API"""
    try:
        genai.configure(api_key=api_key)
        # Получаем список всех доступных моделей
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Ищем самую новую (3 -> 2.5 -> 2 -> 1.5)
        for preferred in ['gemini-3-flash', 'gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']:
            for actual in available_models:
                if preferred in actual:
                    return actual
        return available_models[0] # Берем любую доступную, если ничего из списка не нашли
    except Exception:
        return None

match_input = st.text_input("Введите матч (например: Реал - Атлетико):")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            # 1. Находим рабочую модель
            working_model_name = get_working_model()
            
            if not working_model_name:
                st.error("Не удалось найти доступные модели для вашего API ключа.")
            else:
                st.write(f"🔄 Подключение к: `{working_model_name}`")
                
                # 2. Инициализируем модель с инструментами поиска
                # Важно: в 2026 году поиск часто включен в саму модель
                model = genai.GenerativeModel(
                    model_name=working_model_name,
                    tools=[{'google_search_retrieval': {}}]
                )
                
                with st.spinner('Выполняю поиск актуальных данных в Google...'):
                    query = (
                        f"Сегодня {today_date}. Ты профессиональный аналитик. "
                        f"Используй Google Search. Найди новости, травмы и результаты матчей за ЯНВАРЬ 2026 "
                        f"для команд {match_input}. Выдай: вероятности %, прогноз счета и ставку. "
                        f"Не используй старые данные 2024 года. Только свежая инфа."
                    )
                    
                    response = model.generate_content(query)
                    
                    st.markdown("---")
                    st.success("Анализ готов!")
                    st.markdown(response.text)
                    
        except Exception as e:
            if "429" in str(e):
                st.error("Ошибка 429: Лимит запросов исчерпан. Подождите 60 секунд.")
            else:
                st.error(f"Произошла ошибка: {str(e)}")
                st.info("Убедитесь, что библиотека установлена: pip install -U google-generativeai")
