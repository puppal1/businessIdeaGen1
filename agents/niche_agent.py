from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def identify_niche(clarity_response, logger):
    logger.log_agent_input("NicheAgent", clarity_response)
    
    completion = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": f"""As a niche market expert, analyze this business clarity assessment and identify the ideal target market:

Previous Analysis: {clarity_response}

Please provide:
1. Recommended niche market(s)
2. Ideal customer avatar description
3. Key pain points and desires of target audience
4. Market size and competition analysis
5. Unique value proposition opportunities

Focus on actionable insights for targeting the right audience."""}
        ]
    )
    
    response = completion.choices[0].message.content
    logger.log_agent_output("NicheAgent", response)
    return response 