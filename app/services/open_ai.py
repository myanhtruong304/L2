import re

from openai import OpenAI

from app.core.config import config

client = OpenAI(api_key=config.OPENAI_API_KEY)


# Ensure you have set your OpenAI API key in the environment


async def get_recommendations(country: str, season: str) -> list[str]:
    prompt = f"List three things to do in {country} during the {season} season."
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    recommendations = response.choices[0].text.strip()
    recommendations = re.split(r"\d\.\s+", recommendations)
    recommendations = [rec.strip() for rec in recommendations if rec]

    return recommendations
