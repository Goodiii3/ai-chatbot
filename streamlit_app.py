import streamlit as st
import google.generativeai as genai

# เปลี่ยน title เป็นรูปดัมเบลและอธิบาย Ken เป็น Personal Trainer
st.title("🏋️‍♂️ Ken: Your Personal Trainer")
st.subheader("Conversation with Ken - Your Weight Loss Expert")

gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Questions for user input
if "user_data" not in st.session_state:
    st.session_state.user_data = {"sex": None, "weight": None, "height": None, "goal_weight": None, "time_frame": None}

# 1. Sex (Male/Female)
st.session_state.user_data["sex"] = st.selectbox("Sex", ["Male", "Female"])

# 2. Weight (kg)
st.session_state.user_data["weight"] = st.number_input("Weight (kg)", min_value=1, step=1)

# 3. Height (cm)
st.session_state.user_data["height"] = st.number_input("Height (cm)", min_value=1, step=1)

# 4. Your goal weight (kg)
st.session_state.user_data["goal_weight"] = st.number_input("Your goal weight (kg)", min_value=1, step=1)

# 5. How long to reach your goal weight? (months)
st.session_state.user_data["time_frame"] = st.number_input("How long to reach your goal weight? (months)", min_value=1, step=1)

# Button for planning weight loss
if st.button("Create your plan"):
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, message in st.session_state.chat_history:
        st.chat_message(role).markdown(message)

    # Input from user
    if model:
        try:
            # Generate a weight loss plan based on the user's input
            sex = st.session_state.user_data["sex"]
            weight = st.session_state.user_data["weight"]
            height = st.session_state.user_data["height"]
            goal_weight = st.session_state.user_data["goal_weight"]
            time_frame = st.session_state.user_data["time_frame"]

            # Prompt Ken to generate a weight loss plan based on the user's information
            prompt = (
                f"You are Ken, a highly experienced personal trainer with over 10 years of expertise in weight loss. "
                f"The user is {sex}, weighs {weight} kg, is {height} cm tall, and wants to reach a goal weight of {goal_weight} kg "
                f"within {time_frame} months. Create a detailed weight loss plan for the user, including exercise routines, "
                f"recommended diet, and general tips for staying motivated."
            )

            response = model.generate_content(prompt)
            bot_response = response.text

            # Append the response (weight loss plan) to chat history
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"An error occurred while generating the weight loss plan: {e}")
