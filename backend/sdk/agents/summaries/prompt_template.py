SUMMARY_GENERATION_PROMPT= """
You will be given with weather details based on city name.
Your Goal is to generate a summary of the weather details.
Follow the steps below:
1. You will be given with a city name and weather details.
2. Generate a best flirty summary of the weather details with the city name and good quote for the weather.

Here is your weather details for {city}:
{weather}

You should only return an answer in JSON format.
Here is an example of answer:
{{"flirt_summary":"The weather is hot here isn't it? It's like you, hot and sunny." , "quote":"The best thing one can do when it's hot to eat ice cream."}}
"""