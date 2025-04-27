GENERATE_REFINED_INFO = """
You are a professional content writer specializing in adapting marketing content for specific audiences and tones.

Original Content:
```
{previous_script}
```

Adaptation Requirements:
- Target Audience: {new_target_audience}
- Desired Tone: {new_tone}
- Language: {language}

Your task is to rewrite the original content to better appeal to the specified target audience, using the desired tone and language.
Maintain the key selling points of the product while adapting the language, style, and approach to better resonate with the target audience.

1. Adapt vocabulary and references to match the target audience's preferences and knowledge
2. Adjust the tone to match the requested style (e.g., professional, casual, enthusiastic, etc.)
3. Ensure the content uses appropriate expressions and conventions for the specified language
4. Keep the message concise and impactful

Please provide the refined content that accomplishes these goals.

{format_instructions}
"""