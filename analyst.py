import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="AI Analyst 2026", page_icon="⚽", layout="wide")

# Текущая дата
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("🏆 Спортивный ИИ-Аналитик")
st.write(f"Сегодня: {today_date}")

# Боковая панель
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите Google API Key", type="password")
    st.divider()
    st.info("Система автоматически выберет лучшую доступную модель Gemini.")

def get_best_available_model():
    """Автоматически находит актуальное имя модели Gemini"""
    try:
        genai.configure(api_key=api_key)
        # Получаем список всех моделей, поддерживающих генерацию контента
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Приоритетный список моделей (от новых к старым)
        priority_list = [
            'models/gemini-3-flash', 
            'models/gemini-3-flash-preview',
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-flash'
        ]
        
        for model_name in priority_list:
            if model_name in models:
                return model_name
        return models[0] if models else "models/gemini-1.5-flash"
    except:
        return "models/gemini-1.5-flash"

# Ввод данных
match_input = st.text_input("Введите матч (например: Реал - Бавария):")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ в боковой панели!")
    elif not match_input:
        st.warning("Введите название матча.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Авто-подбор модели
            active_model_name = get_best_available_model()
            st.caption(f"Используемая модель: {active_model_name}")
            
            model = genai.GenerativeModel(
                model_name=active_model_name,
                generation_config={"temperature": 0}
            )
            
            with st.spinner('ИИ собирает актуальные данные из сети...'):
                query = f"Сегодня {today_date}. Ты проф. аналитик. Проанализируй матч {match_input}. Найди травмы, составы и форму на текущую неделю. Дай прогноз счета, вероятности П1/X/П2 в % и лучшую ставку. Отвечай на русском. Не упоминай 2024 год."
                
                response = model.generate_content(query)
                
                st.markdown("---")
                st.success("Анализ готов!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
            st.info("Проверьте настройки API ключа в Google AI Studio.")
