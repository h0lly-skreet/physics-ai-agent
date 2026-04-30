import streamlit as st
from google import genai
from google.genai import types
import os
from typing import Optional

def calculate_kinetic_energy(mass: float, speed: float) -> str:
    """
    Обчислює кінетичну енергію об'єкта за формулою KE = 0.5 * m * v^2.
    
    Args:
        mass: Маса об'єкта у кілограмах (кг).
        speed: Швидкість об'єкта у метрах на секунду (м/с).
        
    Returns:
        Результат обчислення кінетичної енергії у Джоулях (Дж) у вигляді рядка.
    """
    if mass < 0 or speed < 0:
        return "Помилка: Маса та швидкість мають бути невід'ємними числами."
    
    energy = 0.5 * mass * (speed ** 2)
    return f"Кінетична енергія об'єкта з масою {mass} кг та швидкістю {speed} м/с становить {energy:.2f} Дж."

def calculate_ohms_law(voltage: Optional[float] = None, resistance: Optional[float] = None, current_strength: Optional[float] = None) -> str:
    """
    Обчислює невідому величину за законом Ома (V = I * R).
    Для роботи функції необхідно надати РІВНО ДВІ з трьох величин.
    
    Args:
        voltage: Напруга у Вольтах (В).
        resistance: Опір у Омах (Ом).
        current_strength: Сила струму в Амперах (А).
        
    Returns:
        Рядок з результатом обчислення невідомої величини.
    """
    provided_args = sum(x is not None for x in [voltage, resistance, current_strength])
    
    if provided_args != 2:
        return "Помилка: Для використання закону Ома потрібно вказати рівно дві з трьох величин (V, I, R)."

    try:
        if voltage is None:
            result = current_strength * resistance
            return f"Напруга (V) = {current_strength:.2f} A * {resistance:.2f} Ом = {result:.2f} В."
            
        elif resistance is None:
            if current_strength == 0:
                return "Помилка: Неможливо обчислити опір, якщо струм дорівнює нулю."
            result = voltage / current_strength
            return f"Опір (R) = {voltage:.2f} В / {current_strength:.2f} A = {result:.2f} Ом."
            
        elif current_strength is None:
            if resistance == 0:
                return "Помилка: Неможливо обчислити струм, якщо опір дорівнює нулю."
            result = voltage / resistance
            return f"Сила струму (I) = {voltage:.2f} В / {resistance:.2f} Ом = {result:.2f} А."
            
    except TypeError:
         return "Помилка: Всі вхідні параметри мають бути числами."
    except Exception as e:
        return f"Помилка при обчисленні за законом Ома: {e}"
        
    return "Не вдалося визначити, яку величину потрібно обчислити." 

AVAILABLE_TOOLS = [
    calculate_kinetic_energy,
    calculate_ohms_law
]

def run_physics_agent(client: genai.Client, prompt: str):
    """
    Функція керування агентом для Streamlit
    """
    st.info(f"Агент отримав запит: **'{prompt}'**")
    
    config = types.GenerateContentConfig(
        tools=AVAILABLE_TOOLS
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config,
    )

    if response.function_calls:
        tool_outputs = []
        
        with st.spinner("Агент викликає інструмент(и) для розрахунків..."):
            for function_call in response.function_calls:
                function_name = function_call.name
                args = dict(function_call.args)
                
                st.code(f"Виклик: {function_name}({args})", language='python')

                if function_name == "calculate_kinetic_energy":
                    result = calculate_kinetic_energy(**args)
                elif function_name == "calculate_ohms_law":
                    result = calculate_ohms_law(**args)
                else:
                    result = f"Помилка: Невідомий інструмент {function_name}"
                
                st.code(f"Результат: {result}", language='python')
                
                tool_outputs.append(
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                )

        with st.spinner("Обробка результатів та формування фінальної відповіді..."):
            second_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    prompt,
                    response.function_calls,
                    tool_outputs
                ],
                config=config,
            )
        return second_response.text

    else:
        st.info("Інструменти не потрібні. Відповідь моделі...")
        return response.text

def main():
    st.set_page_config(page_title="GenAI Фізичний Агент", layout="wide")
    st.title("AI Агент-Калькулятор для Фізики")
    st.caption("Цей агент використовує модель Gemini та кастомні Python-функції (tools) для обчислень.")

    if "gemini_client" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Помилка: Не знайдено змінну середовища GEMINI_API_KEY.")
            st.error("Будь ласка, встановіть її перед запуском (або використовуйте файл .env).")
            return
        
        try:
            st.session_state.gemini_client = genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"Помилка ініціалізації клієнта: {e}")
            return
        
    client = st.session_state.gemini_client

    st.markdown("---")
    
    user_prompt = st.text_input(
        "Введіть ваше фізичне питання або обчислення:",
        placeholder="Наприклад: Обчислити напругу, якщо струм 0.5 А, а опір 100 Ом."
    )

    if st.button("Запустити Агента"):
        if user_prompt:
            st.subheader("Послідовність виконання:")
            
            final_result = run_physics_agent(client, user_prompt)
            
            st.markdown("---")
            st.subheader("Фінальна відповідь Агента:")
            st.success(final_result)
        else:
            st.warning("Будь ласка, введіть запит.")
            
    st.markdown("---")
    st.markdown("""
    ### Доступні інструменти (Tools):
    * Розрахувати кінетичну енергію.
    * Розрахувати невідому величину за законом Ома.
    """)

if __name__ == "__main__":
    main()