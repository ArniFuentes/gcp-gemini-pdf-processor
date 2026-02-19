import google.generativeai as genai


def get_model(api_key, model_name):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    return model
