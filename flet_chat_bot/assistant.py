from openai import OpenAI
client = OpenAI(api_key = str(open("token.txt").read()))

# OpenAI.api_key = str(open("token.txt").read())

class PrabalGpt():
    def __init__(self):
        self.message = [
            {"role":"system","content":"You are a helpful assistant"},
        ]
        
    def PrabalGptResponse(self, user_text):
        try:
            self.user_text = user_text
            
            while True:
                
                #if say stop, then break the loop
                if self.user_text == "stop":
                    break
                
                #storing the user question in the message list
                self.message.append(
                    {"role":"user","content":self.user_text}
                    )
                
                # getting the responce from openai
                completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=self.message
                            )
                # append the generated responce so that AI remeber past responce
                self.message.append({"role":"assistant","content":str(completion.choices[0].message)})
                
                print(completion.choices[0].message)
                return completion.choices[0].message
        except Exception as e:
            print("=>",e)