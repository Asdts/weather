RECOMMANDATION_GENERATION_PROMPT= """
You will be given with weather details based on city name.
Your Goal is to generate a set of Activity to do in this weather.
Follow the steps below:
1. You will be given with a city name and weather details.
2. Generate a set of activity minimum 5.

Here is your weather details for {city}:
{weather}

You should only return an answer in JSON format.
Here is an example of answer:
{{"activity":["don't forget to take umbrella as its raining", "you can go for a walk in the rain as its most romantic thing to do", "you can go for a movie date if you dont have a date I can come with you", "you can go for a long drive with your the one", "you can go for a trekking"]}}
"""