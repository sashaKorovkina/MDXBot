import os
import csv
import json
import openai
from time import sleep
from dotenv import load_dotenv, dotenv_values, set_key
import io  # Import for in-memory file handling
import time
# Import the get_deadline function from your script


# Load your OpenAI API key from the .env file

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')



def execute_function(function_name, arguments, from_user):
    """
    Execute a function based on the function name and provided arguments.
    """
    # if function_name == 'get_deadline':
    #     username = from_user_id
    #     return get_deadline(username)
    # elif function_name == 'get_status':
    #     username = from_user_id
    #     return get_status(username)
    # else:
    #     return "Function not recognized"
    pass

def process_thread_with_assistant(user_query, assistant_id, model="gpt-4-1106-preview", from_user=None):
    """
    Process a thread with an assistant and handle the response which includes text and images.

    :param user_query: The user's query.
    :param assistant_id: The ID of the assistant to be used.
    :param model: The model version of the assistant.
    :param from_user: The user ID from whom the query originated.
    :return: A dictionary containing text responses and in-memory file objects.
    """
    response_texts = []  # List to store text responses
    response_files = []  # List to store file IDs
    in_memory_files = []  # List to store in-memory file objects
  
    try:
        print("Creating a thread for the user query...")
        thread = openai.Client().beta.threads.create()
        print(f"Thread created with ID: {thread.id}")
        print(thread)
        print("Adding the user query as a message to the thread...")
        file_id = openai.Client().beta.assistants.retrieve(assistant_id).file_ids[0]
        openai.Client().beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query,
            file_ids=[file_id]
        )
        print("User query added to the thread.")

        print("Creating a run to process the thread with the assistant...")
        run = openai.Client().beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id = assistant_id,
            model=model
        )
        time.sleep(10)
        # if not run:
        #     print("waiting....")
            

        print(f"Run created with ID: {run.id}")

        while True:
            print("Checking the status of the run...")
            run_status = openai.Client().beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Current status of the run: {run_status.status}")

            if run_status.status == "requires_action":
                print("Run requires action. Executing specified function...")
                tool_call = run_status.required_action.submit_tool_outputs.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                function_output = execute_function(function_name, arguments, from_user)
                function_output_str = json.dumps(function_output)

                print("Submitting tool outputs...")
                openai.Client().beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": tool_call.id,
                        "output": function_output_str
                    }]
                )
                print("Tool outputs submitted.")

            elif run_status.status in ["completed", "failed", "cancelled"]:
                print("Fetching messages added by the assistant...")
                messages = openai.Client().beta.threads.messages.list(thread_id=thread.id)
                for message in messages.data:
                    if message.role == "assistant":
                        for content in message.content:
                            if content.type == "text":
                                response_texts.append(content.text.value)
                            elif content.type == "image_file":
                                file_id = content.image_file.file_id
                                response_files.append(file_id)

                print("Messages fetched. Retrieving content for each file ID...")
                for file_id in response_files:
                    try:
                        print(f"Retrieving content for file ID: {file_id}")
                        # Retrieve file content from OpenAI API
                        file_response = openai.Client().files.content(file_id)
                        if hasattr(file_response, 'content'):
                            # If the response has a 'content' attribute, use it as binary content
                            file_content = file_response.content
                        else:
                            # Otherwise, use the response directly
                            file_content = file_response

                        in_memory_file = io.BytesIO(file_content)
                        in_memory_files.append(in_memory_file)
                        print(f"In-memory file object created for file ID: {file_id}")
                    except Exception as e:
                        print(f"Failed to retrieve content for file ID: {file_id}. Error: {e}")

                break
            sleep(1)

        return {"text": response_texts, "in_memory_files": in_memory_files}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"text": [], "in_memory_files": []}

# Example usage
def create_assistant():
  assistant_file_path = 'assistant.json'

  # If there is an assistant.json file, load the assistant
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      
      print("Loaded existing assistant ID.")
  else:
    # Create file
    
        

    data = []
    with open("diagnose.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    # Write data to a JSON file
    with open('diagnose.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    
    with open('diagnose.json', 'rb') as file:
        file = openai.Client().files.create(file=file, purpose='assistants')
        file_id = file.id
    # Create the assistant
    assistant = openai.Client().beta.assistants.create(
        instructions= "You are the assistant bot in Medical specific questions. You are the AI Medical knowledge assistant chatbot. You have access to the dianose.csv file. You should analyze user question and answer from the provided file. If you do not find the answer, you can answer on your own knowledge and say that it is not much reliable",
        model="gpt-4-1106-preview",
        tools=[{
            "type": "retrieval"
        }],
        # Assuming file_ids is defined elsewhere in your code
        file_ids=[file_id])
    print(assistant)
    # Print the assistant ID or any other details you need
    print(f"Assistant ID: {assistant.id}")

    # Create a assistant.json file to save OpenAI costs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id

user_query = "Can you tell me about Achalasia's Cell biology"
assistant_id = create_assistant()
from_user_id = "nurekendei"
response = process_thread_with_assistant(user_query, assistant_id, from_user=from_user_id)
print("Final response:", response)

