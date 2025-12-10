import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

"""
If I had 2 more hours, I would:
- Add multiple refinement loops until a quality threshold is met
- Add safety classification (e.g. bedtime vs adventurous vs silly)
- Add structured metrics logging for judge scores
- Allow user feedback to guide regeneration
"""

STORYTELLER_PROMPT = """
You are a kind, imaginative children's storyteller.
You write bedtime stories for children ages 5–10.

Rules:
- Use simple, clear language.
- Avoid anything scary, violent, or upsetting.
- Keep a gentle bedtime tone.
- Use a clear beginning, middle, and happy ending.
- Include a soft lesson about kindness, courage, or friendship.
"""

JUDGE_PROMPT = """
You are a children's book reviewer.

Evaluate the following story for:
- Age appropriateness (5–10)
- Language clarity
- Story structure
- Bedtime tone
- Positive lesson

Return your response as JSON with:
- score (1–10)
- problems (list)
- suggestions (string)
"""


def call_model(prompt, temperature=0.7):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # DO NOT CHANGE
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def generate_story(user_request):
    prompt = STORYTELLER_PROMPT + "\n\nStory request:\n" + user_request
    return call_model(prompt, temperature=0.9)


def judge_story(story):
    prompt = JUDGE_PROMPT + "\n\nStory:\n" + story
    response = call_model(prompt, temperature=0.1)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "score": 5,
            "problems": ["Judge response was not valid JSON"],
            "suggestions": response,
        }


def refine_story(original_story, feedback):
    prompt = f"""
Rewrite the following story to fix these issues:
{feedback}

Story:
{original_story}

Keep it gentle, age-appropriate, and suitable for bedtime.
"""
    return call_model(prompt, temperature=0.8)


def main():
    user_input = input("What kind of story do you want to hear? ")

    story = generate_story(user_input)
    feedback = judge_story(story)

    if feedback.get("score", 0) < 8:
        story = refine_story(story, feedback)

    print("\nFinal Story:\n")
    print(story)


if __name__ == "__main__":
    main()
