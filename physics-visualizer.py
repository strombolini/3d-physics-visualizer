## Author : tyb3@cornell.edu
import requests #API req library
import json #Json
import time #Waiting for response
import pyglet
from pyglet.gl import *
from pyglet.window import key
import pyglet.graphics
import pyglet.model #Plotting 3D image
from openai import OpenAI #Dalle API Requests
import os

# Set OpenAI API key
openai_api_key = "PUT YOUR OPEN AI API KEY HERE"
os.environ["OPENAI_API_KEY"] = openai_api_key

# Function to generate image using DALL-E
def generate_image(text):
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url  # Accessing the URL of the first generated image
    return image_url

# Function to send image to Meshy.ai
def send_to_meshy(image_url):
    payload = {
        "image_url": image_url,
        "enable_pbr": True,
    }
    headers = {
        "Authorization": "Bearer PUT YOUR MESHY.AI API KEY HERE"
    }

    response = requests.post(
        "https://api.meshy.ai/v1/image-to-3d",
        headers=headers,
        json=payload,
    )
    return response.json()
# Function to retrieve image from meshy
def retrieve_from_meshy(response_id):
# Extract the hash value associated with the key "result"
    task_id = response_id["result"]

    print (task_id)
    headers = {
        "Authorization": f"Bearer PUT YOUR MESHY.AI API KEY HERE"
    }

    
    response = requests.get(
        f"https://api.meshy.ai/v1/image-to-3d/{task_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


# Main function -- Code is run here
def main():
    physics_problem = input("Enter the physics problem: ")
    print ("DALLE3 is Drawing a 2D image...")
    
    #Enter Primer Prompt Here - May be replaced with ChatGPT call
    primer_prompt = "Simple shapes render, two-dimensional, white background, physics problem:"
    image_url = generate_image(primer_prompt + physics_problem)
    print ("Queueing 3D Render with Meshy.AI ...")
    response = send_to_meshy(image_url)
    print ("Retrieving 3D files...")
    json_response = retrieve_from_meshy(response)
    time_elapsed = 0
    while json_response['status'] != "SUCCEEDED":
        json_response = retrieve_from_meshy(response) #Refresh the batch information
        print("STATUS: " + str(json_response['status']))
        print("PROGRESS: " + str(json_response['progress']) + "%") #Print completion info
        print("TIME ELAPSED (s): " + str(time_elapsed) + " Seconds")
        print("-----------------------------")
        time.sleep(10)
        time_elapsed += 10
    print("SUCCESS - RENDERING IMAGE...")
    glb_url = str(json_response['model_url'])

    # Download the GLB file
    response = requests.get(glb_url)
    glb_data = response.content
    
    # Save the GLB file to disk
    glb_file_path = "physics-visualizer-render.glb"  # You can customize the file path as needed
    with open(glb_file_path, "wb") as f:
        f.write(glb_data)
    
    # Open the GLB file using the default associated application
    os.startfile(glb_file_path)
if __name__ == "__main__":
    main()
