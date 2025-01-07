from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def create_action_plan(clarity_response, niche_response, logger):
    logger.log_agent_input("ActionAgent", f"Clarity: {clarity_response}\nNiche: {niche_response}")
    
    completion = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": f"""As an action plan specialist, create a detailed step-by-step plan based on this analysis:

Clarity Assessment: {clarity_response}
Niche Analysis: {niche_response}

Provide specific actions for:
1. Which platforms to use for finding leads
2. How to search for and identify potential clients
3. Messaging templates and outreach strategies
4. Service/product offering recommendations
5. Daily action items and timeline
6. Tools and resources needed

Make it as specific and actionable as possible."""}
        ]
    )
    
    response = completion.choices[0].message.content
    logger.log_agent_output("ActionAgent", response)
    return response 