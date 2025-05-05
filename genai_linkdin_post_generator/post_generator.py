from llm_helper import llm
from few_shot import FewShotPosts

fs = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def prompt_generator(length, language, tag):
    lenght_str = get_length_str(length)
    
    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {lenght_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    
    example = fs.get_filtered_post(length, language, tag)
    
    if len(example) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(example):
        post_text = post['text']
        prompt += f"\n\n Example {i+1}: \n\n {post_text}"
            
        if i == 1:
            break
            
    return prompt

def generate_post(length, language, tag):
    prompt = prompt_generator(length, language, tag)
    responce = llm.invoke(prompt)
    return responce.content
    
    
if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))