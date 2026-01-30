import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- Инициализация ---
st.set_page_config(page_title="Gemini AI Analyst", page_icon="⚽", layout="wide")
today_date = datetime.now().strftime("%d.%m.%Y")

st.title("⚽ Автономный ИИ-Аналитик")
st.caption(f"Статус: Активен | Дата: {today_date}")

with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите Google API Key", type="password")
    st.divider()
    st.info("Код автоматически подберет доступную модель Gemini.")

def get_best_model():
    """Автоматически находит самую актуальную модель в вашем API"""
    try:
        genai.configure(api_key=api_key)
        # Получаем список моделей, поддерживающих генерацию
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Приоритет выбора (от новых к старым)
        priority = ['gemini-3-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']
        
        for p in priority:
            for m in models:
                if p in m:
                    return m
        return models[0] if models else None
    except:
        return None

match_input = st.text_input("Введите матч (например: Эспаньол - Севилья):")

if st.button("🚀 ЗАПУСТИТЬ АНАЛИЗ"):
    if not api_key:
        st.error("Введите API ключ в боковой панели!")
    elif not match_input:
        st.warning("Введите названия команд.")
    else:
        try:
            # 1. Подбираем модель
            working_model = get_best_model()
            
            if not working_model:
                st.error("Ошибка: Не удалось найти доступные модели. Проверьте API ключ.")
            else:
                st.write(f"📡 Подключено к: `{working_model}`")
                
                # 2. Настраиваем модель (пробуем поиск)
                # В 2026 году Google часто вшивает поиск по умолчанию в новые модели
                try:
                    # Пытаемся подключить инструмент поиска
                    model = genai.GenerativeModel(
                        model_name=working_model,
                        tools=[{'google_search_retrieval': {}}]
                    )
                except:
                    # Если инструменты не поддерживаются данной версией, берем чистую модель
                    model = genai.GenerativeModel(model_name=working_model)
                
                with st.spinner('Синхронизация с данными Google Search 2026...'):
                    query = (
                        f"Сегодня {today_date}. Используй поиск Google. "
                        f"Найди последние новости, травмы и результаты для {match_input}. "
                        f"Игнорируй данные 2024 года. Дай отчет: вероятности %, прогноз счета и ставку. "
                        f"Отвечай на русском."
                    )
                    
                    # Устанавливаем температуру 0 через generation_config
                    response = model.generate_content(
                        query,
                        generation_config={"temperature": 0}
                    )
                    
                    st.markdown("---")
                    st.success("Анализ готов!")
                    st.markdown(response.text)
                    
        except Exception as e:
            if "429" in str(e):
                st.error("Превышена квота (429). Подождите 60 секунд.")
            else:
                st.error(f"Ошибка API: {str(e)}")
