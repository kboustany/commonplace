from openai import OpenAI


api_key = (
    'sk-proj-c6bt32OoUQquiFRlxhnILnjmcXQRPEEJ-M3iJgaan8BUuyrEPdwQFM-'
    'DIecH9_ynNKWf8bN61qT3BlbkFJfPbw0vMbbfjhRihjyZeR07-'
    '1wsZkP8Jo6zEVvlYtd_D8OsiQqttn2I6B6fPN9RwFVx4BlLc_4A'
)

client = OpenAI(api_key=api_key)

def get_tag_description(tag, category):
    prompt = (
        f"Produce a one-sentence description of {tag},"
        f"as understood under the category of {category}"
    )
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )
    return response.output_text

def get_item_comment(prompt):
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )
    return response.output_text