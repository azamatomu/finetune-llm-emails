# finetune-llm-emails
Fine-tune an LLM on email subjects to create better content calendars.

## How to build the Docker image

1. Clone repo
2. Make sure you have the model weights downloaded in the `model` folder
3. If you are using model weights different than `mistral-7b-it-emails`, adjust the model weight path in `Dockerfile`
4. Run `docker build -t $username$/reponame:tag .` to build the Docker image
5. Push the Docker image to your Docker repo

## How to deploy the Docker image on RunPod

1. Register your Docker Artifactory
2. Setup a new serverless endpoint in Runpod
3. Pick at least a 24GB GPU endpoint, model is big
4. Deploy the `$username$/reponame:tag"` image from your Artifactory
5. Enjoy! Example input below

## Example Input

```json
{
    "input": {
        "prompt": "Give me an email-only content calendar for activating users that haven't used my service in more than 3 months. The service is an online marketplace for prospective home buyers to find houses and apartments in the Netherlands. Instructions: for each content idea provided, give me why this is something that makes sense for activating dormant users, and how to adjust the content strategy depending on whether it has been successful at activating the user after each month."
    }
}
```
## What was this model fine-tuned on? 

This mistral-7b-it model has been fine-tuned using QLoRA on a set of instructions for creating email content calendars. The dataset has been derived based on series of actual email subjects from the same sender and pre-processed by GPT-4 to fit into an instruction tuning format. 

Below is an example of one input entry: 
```

[INST]Create a content calendar for an email marketing campaign focused on wine lovers,
that aims to guide them from initial brand engagement to becoming informed and enthusiastic customers by leveraging various relevant themes and incentives.
The campaign should cover an introductory series of 20 emails, aligning each message with a content theme or promotion that resonates with the interests and lifecycle of a wine-loving audience.
Address seasonality, product education, engagement, and sales promotions, suggesting a strategic order for the email subjects provided, considering the elements of timing and context in your reasoning.[/INST]

Based on the email subjects provided, the proposed plan for the content calendar could be as follows:

1. **Welcoming and Education Phase** (Warming up the audience with introductory and informative content)
   - 0th Email: Geniet extra van jouw gekochte wijn met deze tips (Welcome and value-added tips)
   - 1st Email: Hi wijnliefhebber, benieuwd waar jouw wijn vandaan komt? (Product origin education)
   - 2nd Email: Hier vind je de allerbeste wijnspijs tips! (Food pairing suggestions)
   - 3rd Email: Wij hebben deze wijnen voor jou uitgezocht! (Personalized picks for engagement)

2. **Value and Retention Phase** (Offering deals and holiday themes)
   - 4th Email: Speciaal voor jou: €5,- korting op je volgende aankoop! (Incentive to encourage purchase)
   - 5th Email: Een digitaal kerstkaartje voor jou! (Seasonal greeting, building rapport)
   - 6th Email: Dit zijn de beste wijnen voor jouw Oud & Nieuw (New Year recommendations)
   - 7th Email: Fijne jaarwisseling! (Seasonal wishes to maintain connection)
   - 8th Email: Proost ook mee op het nieuwe jaar! (Celebrate the New Year, fostering community)
   - 9th Email: Kom jij proeven dit weekend? (Event invitation for hands-on experience)

3. **Seasonal and Curated Selections** (Highlighting seasonal selections and expert choices)
   - 10th Email: Voor jou geselecteerd: de 5 lekkerste winterwijnen! (Curated winter selections)
   - 11th Email: Wijnliefhebbers opgelet: beste Hongaarse wijnmaker van 2023! (Spotlight on award-winners)
   - 12th Email: Nieuwe proefboxen: samengesteld door onze wijninkoper (Expert-curated tasting boxes)

4. **Engagement and Brand Building Phase** (Content that enriches the wine experience and positions brand authority)
   - 13th Email: Wapen je tegen de kou met deze heerlijke rode wijn! (Engagement with practical themes)
   - 14th Email: Er staan 4 nieuwe video's voor je klaar! (Educational content through multimedia)
   - 15th Email: Deze klassieke Bordeaux wil je proeven! OP = OP (Exclusive offer to create urgency)

5. **Sales and Urgency Phase** (Sustaining momentum with sales and urgency)
   - 16th Email: SALE: kortingen tot 25% (Announcing sales to stimulate purchase)
   - 17th Email: De 6 beste sale wijnen samen in 1 box! (Bundling deals for more value)
   - 18th Email: Dit zijn de lekkerste sale wijnen voor je weekend! (Weekend sales highlight)
   - 19th Email: Laatste kans: SALE! (Urgency to act on sales)
   - 20th Email: Shop alleen dit weekend nog sale! (Final call for sales event)

This calendar flows from welcoming and educating new subscribers to engaging them with relevant seasonal content, then building the brand relationship by offering curated selections and expert knowledge, before finally capitalizing on that relationship with promotional sales and creating a sense of urgency. The emails are sequenced to follow the natural progression of interest and engagement that a new subscriber would experience, while also taking advantage of seasonal moments and sales opportunities.
```
