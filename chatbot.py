import google.generativeai as genai


def aira_assist(information, query):
    API_KEY = "AIzaSyDxiXqLTdeGJavlu" + "_cW1VOoYWq66PWkSfg"
    MODEL_ID = "gemini-1.5-flash"
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel(
        model_name=MODEL_ID,
        system_instruction="Dont give any other response other than required and respond precisely with no extra content and respond in second person point of view."
                           "You are a Resume assistant, you will be provided with the user LinkedIn profile data."
                           "You need to assist and suggest user with all the queries in regarding his profile."
                           "If there is a query other than regarding the resume handle it and give response like and assistant",
    )

    try:
        response = model.generate_content(f'This is the user information, {information} and the query is --- {query}')
        return (response.text)


    except Exception as e:
        return f"Error generating response: {e}"

