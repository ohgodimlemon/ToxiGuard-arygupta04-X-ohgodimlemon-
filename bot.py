import os
import discord
from dotenv import load_dotenv
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
import numpy as np
import pandas as pd



# This function loads environment variables from .env
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
MAX_FEATURES = 200000 # number of words in the vocab


# Create an Intents object with the necessary permissions
intents = discord.Intents.default()
intents.messages = True  # Enable event handling for messages
intents.message_content = True  # Allow access to message content

client = discord.Client(intents=intents)

# Load the toxicity model 
model = tf.keras.models.load_model('toxicity.h5')



######## For preprocessing #############
df = pd.read_csv('jigsaw-toxic-comment-classification-challenge/train.csv')

X = df['comment_text']

vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=1800,
                               output_mode='int')
vectorizer.adapt(X.values)
#######################################


def score_comment(comment):
    """
    Scores a given comment by predicting its attributes using a model.

    Args:
        comment (str): The comment to be scored.

    Returns:
        str: A formatted string with the prediction results.
    """
    # Vectorize the comment
    vectorized_comment = vectorizer([comment])
    
    # Predict results using the model
    results = model.predict(vectorized_comment)
   
    text = ""
    
    # Iterate through the columns to format predictions
    for idx, col in enumerate(df.columns[2:]):

        if results[0][idx] > 0.5:
            text += f"{col} "
            

    return text





# This event is triggered when the bot successfully connects to Discord
@client.event
async def on_ready():
    # client.user refers to the bot
    print(f'{client.user} has connected to Discord!')

    # This refers to the general channel
    channel_id = 1326432814593343613
    channel = client.get_channel(channel_id)

    if channel:
        await channel.send("Hello!")



###
toxicity_threshold = 0.5  # Default threshold


# This event is triggered when a message is sent in a channel the bot can access
@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return


    feedback = score_comment(message.content)
    if feedback != "":
        await message.delete()

        await message.author.send(
            f"Your message in `{message.channel.name}` was flagged as {feedback}. "
            "Please adhere to the community guidelines and maintain a positive environment."
        )
        
client.run(TOKEN)
