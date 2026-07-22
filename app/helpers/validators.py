"""
==========================================================
Validators
==========================================================
"""


def validate_prompt(prompt):

    prompt = prompt.strip()

    if not prompt:

        raise ValueError("Please enter a prompt.")

    if len(prompt) < 5:

        raise ValueError(
            "Prompt is too short."
        )

    if len(prompt) > 5000:

        raise ValueError(
            "Prompt is too long."
        )

    return prompt