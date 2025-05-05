import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# def sanitize_text(text):
#     """Remove surrogate characters from the input text."""
#     return re.sub(r'[\ud800-\udfff]', '', text)

def process_post(raw_file_path,processed_file_path=None):
    enriched_post = []
    
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            # sanitized_text = sanitize_text(post['text'])
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_post.append(post_with_metadata)
    
    # the responce comes are in dictionary formate 
    unified_tags = get_unified_tags(enriched_post)        
    print(f"\n\n==>3 {unified_tags}")
    for post in enriched_post:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)
    
    # writting json formate data in file 
    with open(processed_file_path,encoding='utf-8',mode='w') as outfile:
        json.dump(enriched_post,outfile,indent=4)
            
def extract_metadata(post):
    
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    responce = chain.invoke(input={"post":post})
    try:
        json_parse = JsonOutputParser()
        res = json_parse.parse(responce.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res
    
def get_unified_tags(post_with_metadata):
    unique_tags = set()
    
    for post in post_with_metadata:
        unique_tags.update(post['tags'])
        
    print("\n\n==>1",unique_tags)
    
    
    # from give set we need to string that contain the tags with comma separated
    #  like job seeking, job search, job hunting
    unique_tags_string = ", ".join(unique_tags)
    print("\n\n==>2",unique_tags_string)
    print("\n\n==>2",type(unique_tags_string))
    
    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    responce = chain.invoke(input={"tags":str(unique_tags_string)})
    try:
        json_parse = JsonOutputParser()
        res = json_parse.parse(responce.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

if __name__ == "__main__":
    process_post("data/raw_posts.json","data/processed_posts.json")