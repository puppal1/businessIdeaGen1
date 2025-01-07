from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def create_business_strategy(clarity_response, niche_response, action_response, logger):
    logger.log_agent_input("StrategyAgent", 
                          f"Clarity: {clarity_response}\nNiche: {niche_response}\nAction: {action_response}")
    
    completion = client.chat.completions.create(
        model="o1-mini",
        messages=[
                        {"role": "user", "content": f"""Based on the following analysis:

Clarity Assessment: {clarity_response}
Niche Analysis: {niche_response}
Action Plan: {action_response}

Create a prioritized action plan with:

1. Quick Wins (Next 7 Days)
   - List 2-3 highest-impact, lowest-effort actions to start immediately

2. Core Strategy
   - The single most efficient path to first revenue
   - Key market advantage to leverage

3. Critical Resources
   - Essential tools/resources needed
   - Estimated initial budget

4. Success Indicators
   - Primary metric to track
   - First major milestone to achieve

Focus on practical, immediate actions that maximize results with minimal resources."""}
        ]
    )
    
    response = completion.choices[0].message.content
    logger.log_agent_output("StrategyAgent", response)
    return response 