# Hippocratic AI Coding Assignment – Bedtime Story Generator

This project extends the provided Python skeleton to generate bedtime stories for children ages 5–10 using prompting and an LLM-based judge to improve quality.

The system uses the same OpenAI model provided in the skeleton and does not hard-code any API keys.

---

## System Design Overview

The system uses a single LLM in two distinct roles:

1. **Storyteller** – generates an initial bedtime story based on the user's request.
2. **Judge** – evaluates the story for age appropriateness, tone, structure, and clarity.

If the judge determines that the story quality is below a defined threshold, the system performs a refinement pass to improve the output.

---

## High-Level Flow

1. User provides a short description of the bedtime story they want.
2. The Storyteller prompt generates an initial story suitable for ages 5–10.
3. The Judge prompt reviews the story and returns structured JSON feedback.
4. If the judge score is below a threshold, the story is rewritten using the judge’s feedback.
5. The final story is printed to the user.

---

## Block Diagram

```text
User Request
    ↓
Storyteller Prompt
    ↓
Initial Story
    ↓
Judge Prompt (LLM Critic)
    ↓
Judge Feedback (score + issues)
    ↓
If score < threshold
    ↓
Refined Story
    ↓
Output to User
