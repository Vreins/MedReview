from langchain_groq import ChatGroq
from preprocess import review_clean
import re
import streamlit as st

llm = ChatGroq(
    api_key=st.secrets["groq"]["api_key"],
    model_name="llama-3.3-70b-versatile"
)

def get_sentiment(review: str):
    """Predict sentiment using Groq LLM with confidence score."""
    review_cleaned = review_clean(review)

    prompt = f"""
    Analyze the sentiment of the following drug review.

    Classify it as one of: Positive, Neutral, or Negative.

    Respond in JSON only, like this:
    {{
        "sentiment": "Positive"
    }}

    Review: "{review_cleaned}"
    """

    response = llm.invoke(prompt)
    result = response.content.strip()

    # Default values
    sentiment = "Neutral"

    # Try to extract sentiment from the LLM's JSON response
    try:
        sentiment_match = re.search(r'"sentiment"\s*:\s*"(\w+)"', result)
        
        if sentiment_match:
            sentiment = sentiment_match.group(1).capitalize()
    except Exception:
        pass
    
    sides_prompt = f"""
    Analyze the following drug review and extract only the side effects that the reviewer personally experienced.

    Include side effects ONLY if the reviewer clearly states that they had the symptom while taking the medication.

    Do NOT include side effects that the reviewer merely mentions as possibilities, repeats from others, or describes as something they did NOT experience.

    If the reviewer expresses uncertainty (e.g., “I think it caused…”, “Maybe because of the medication…”) you may include the side effect only if it is clear they are referring to their own experience.

    Return the side effects as a clean, comma-separated list.

    Respond in JSON only, like this:
    {{
        "side_effects": "side effect 1, side effect 2, ..."
    }}

    Review: "{review}"
    """
    sides_response = llm.invoke(sides_prompt)
    sides_result = sides_response.content.strip()
    
    Sides = "Not Specified"

    try:
        sides_match = re.search(r'"side_effects"\s*:\s*"([^"]+)"', sides_result)
        
        if sides_match:
            Sides = sides_match.group(1)
    except Exception:
        pass

    return [sentiment, Sides]



def get_side_effects(side_effects: str):
    """Predict sentiment using Groq LLM with confidence score."""
    
    sides_prompt = f"""
    Analyze the following side effects and bring out any mentioned side effects of the medication.

    Respond in JSON only, like this:
    {{
        "side_effects": "side effect 1, side effect 2, ..."
    }}

    Review: "{side_effects}"
    """
    sides_response = llm.invoke(sides_prompt)
    sides_result = sides_response.content.strip()
    
    Sides = "Not Specified"

    try:
        sides_match = re.search(r'"side_effects"\s*:\s*"([^"]+)"', sides_result)
        
        if sides_match:
            Sides = sides_match.group(1)
    except Exception:
        pass

    return  Sides
