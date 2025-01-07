from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()

def get_business_clarity(user_input, logger):
    logger.log_agent_input("ClarityAgent", user_input)
    
    completion = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": f"""As a business clarity expert, help understand this entrepreneur's goals and provide clear direction:

User Input: {user_input}

Please analyze:
1. Their current situation and goals
2. Main challenges they're facing
3. Potential opportunities for making money online
4. Initial recommendations for getting started

Provide a clear and actionable response."""}
        ]
    )
    
    response = completion.choices[0].message.content
    logger.log_agent_output("ClarityAgent", response)
    return response 