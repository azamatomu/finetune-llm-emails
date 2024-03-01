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
