import json
import queue
import faiss  # your IDE might complain about missing args.
import socket
#import anthropic
import debugging
import numpy as np
from os import path
from time import sleep as wait
from tkinter import messagebox as msgbox
from openai import OpenAI, APIConnectionError

DIMENSIONS = 256 # size of a the embedding matrix - depends on what model you're using
EMBEDDING_MODEL = "text-embedding-3-small"

db = debugging.Debug()
client = None
corp = 0
embedding_index_db = faiss.IndexFlatL2(DIMENSIONS)
embedding_text_db = []

config_file_path = path.join(path.expanduser('~'), "clipycards.config")
log_file_path = path.join(path.expanduser('~'), "clipycards.log")

config = {}
default_config = {
    "about":"version: 1.0 | dev: mohsilas | default themes: light, dark, rose-pine | need help with this config, or creating themes? visit clipycards.com",
    #"anthropic(1)-or-openai(0)?": 1, # abandend, half-baked, feature (complicates the UX)
    "key":"<your_api_key>",
    "role": "system",
    "main-model": "gpt-3.5-turbo",
    "sys_prompt":"you are a system that generates Q&As from provided info. Here is a general idea about the info you will be provided:<br><study_topic_context><br>Here're some pervious interactions to improve your responses:<br><similar_context><br>keeping with the previous context, turn the following info into a Q&A in the exact format of \"question? | answer\". If multiple Q&As were generated, separate them by an empty line.",
    "temp": 1,
    "top_p": 1,
    "context_length": 4, # number of previous interactions loaded into the prompt
    "backend_thread_clipboard_queue_timeout": 4, # wait's n seconds for the queue instead of busy waiting. the higher n is, the lower cpu usage.
    "frontend_cards_export_format_separator": " | ",
    "theme": "light",
    "internet_ping_server": ["8.8.8.8", 53]
}

# ----------------------------------------------------------- clipycards config create/validate/patch -------------------------------------------------------

def backend_config_file_validate(app, dialog_gui_class, loaded_config):
    global config
    #print("\nLoaded Config -->\n", loaded_config)
    if loaded_config != None:
        missing_keys = set(default_config) - set(loaded_config)
        if len(missing_keys):
            db.log_critm(__name__, f"Missing key(s) from config file: {missing_keys} -- you can either restore the missing key(s), or copy your OpenAI API key and then delete the whole config file, clipycards will help create a new file.")
            return False
        config = loaded_config
        return True
    else:
        api_dialog = dialog_gui_class(app, msg="Please provide an Openai API key.", geo="400x300", h=150,w=380)
        app.wait_window(api_dialog)
        api_key = api_dialog.result
        #corp = backend_api_key_test(api_key)
        if not api_key:
            db.log_warn(__name__, "No API key was provided -- asked for a key")
            exit()
        with open(config_file_path, "x") as fo:
            default_config["key"] = api_key
            # default_config["anthropic(1)-or-openai(0)?"] = corp #abandend half-baked feature (complicates the UX)
            config = default_config
            json.dump(default_config, fo, indent=4)
        return True

#def backend_api_key_test(key):
    # half-baked feature, need to integrate another text embedding model which isn't worth it (two API keys).
    # I just left this half-baked code so you don't have to implement it from scratch
    # also, if anthropic made their own embedding model, then it'd be a lot less complicated for the user (one API key).
    #client = openai.OpenAI(api_key=api_key)
    #try:
    #    client.models.list()
    #except openai.AuthenticationError:
    #    return 1
    #else:
    #    return 0

# -------------------------------------------------- talking to Openai's API / keeping context --------------------------------------------------------
# all funcs can be refactored into one, but i don't care anymore!

def backend_api_object_create():
    global client #, corp
    try:
        #corp = config["anthropic(1)-or-openai(0)?"]
        if corp:
            pass
            #client = anthropic.Anthropic(api_key=config["key"])
        else:
            client = OpenAI(api_key=config["key"])
    except Exception as e:
        db.log_crit(__name__, e, "Problem creating Openai client")
        exit()

def backend_card_generate_from_data(request, study_topic_context):
    request_embedding = backend_embedding_generate(request) #text embeddings for vector search
    similar_context = "\n".join(back_endembedding_index_db_search_similar(request_embedding))

    sys_query=str(config["sys_prompt"]).replace("<study_topic_context>", study_topic_context).replace("<similar_context>", similar_context).replace("<br>", "\n")
    # print(f"\n\n \x1b[38;5;83m{sys_query}\x1b[0m \n\n")
    result = backend_api_response_get(request, sys_query)
    card_prompt = f"{sys_query}{request}"
    interaction = F"info: {request}\nQ&A: {result}"
    backend_embedding_index_db_add(interaction)
    return [result, card_prompt]

def backend_study_context_title_generate(study_topic_context):
    try:
        sys_q = "Your task is to generate a short title from the text you'll be provided. remember to not put the generated title in qoutes."
        result = backend_api_response_get(study_topic_context, sys_q)
    except APIConnectionError:
        msgbox.showerror("Context updating failed", "Clipycards can't connect to OpenAI's servers. Please check your internet connection")
        bridge_shared_handles.backend_api_connection_error_event.set()
        internet_status = "Online" if backend_internet_is_connected() else "Offline"
        db.log_critm(__name__, f"APIConnectionError --internet status: {internet_status}")
        result = " "
    except Exception as e:
        msgbox.showerror("Context updating failed", f"Please check {log_file_path} for more info")
        db.log_warn(__name__, f"Update context error: {e}")
        result = " "
    return result

def backend_api_response_get(r, sys_q="", sys_role_enabled=1):
    if corp:
        return backend_api_anthropic_response_get(r, sys_q)
    else:
        return backend_api_openai_response_get(r, sys_q, sys_role_enabled)


def backend_api_openai_response_get(r, sys_q, sys_role_enabled=1):
    messages_ = [{"role": config["role"], "content": sys_q}, {"role": "user", "content": r}] if sys_role_enabled else [{"role": "user", "content": r}]
    response = client.chat.completions.create( # if your editor is panicing cuz client/chat is type "None", ignore it.
    model=config["main-model"],
    messages=messages_,
    temperature=config["temp"],
    top_p=config["top_p"]
    )
    return response.choices[0].message.content

def backend_api_anthropic_response_get(r, sys_q="", sys_role_enabled=1):
    message = client.messages.create(
        model= "claude-3-opus-20240229",#config["main-model"],
        temperature= 1,#config["temp"],
        system=sys_q,
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": r
                    }
                ]
            }
        ]
    )
    return message.content
# -------------------------------------------------------- text embedding and all that crap! ----------------------------------------------------
# refactor with another embedding model if you wanna implement the anthropic API feature. This code is currently using openai's.

def backend_embedding_generate(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text, encoding_format="float")
    return np.array([response.data[0].embedding[:DIMENSIONS]], dtype=np.float32) # faiss expects a float32 np matrix of size n-by-d, in this case 1x256

def backend_embedding_index_db_add(text):
    embedding_text_db.append(text)
    embedding_index_db.add(backend_embedding_generate(text))

def back_endembedding_index_db_search_similar(embd):
    _, indexes = embedding_index_db.search(embd, config["context_length"])
    indexes = indexes.flatten()
    return [(embedding_text_db[i] if i > 0 else "") for i in indexes]

# ---------------------------------------------------------------- simple check functions -------------------------------------------------------
def backend_internet_is_connected(): 
    try:
        socket.create_connection((config["internet_ping_server"][0], config["internet_ping_server"][1]))
        return True
    except Exception as e:
        db.log_critm(__name__, f"Problem checking internet connection: {e} -- changing the pinged server might resolve this")
        return False

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------backend main --------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def backend_thread_main(bridge_shared_handles, kiwi): # Thread(args=) in main.py must be an iterable, hence kiwi
    #print("backend thread started!")
    bridge_shared_handles.frontend_cards_export_format_separator = config["frontend_cards_export_format_separator"]
    while not bridge_shared_handles.backend_thread_stop_event.is_set():
        bridge_shared_handles.backend_thread_running_event.wait()
        try:
            clipboard_data = bridge_shared_handles.clipboard_data_queue.get(timeout=config["backend_thread_clipboard_queue_timeout"]) # waits n seconds for the queue, thus significantly reducing cpu usage :)
            if clipboard_data == "BACKEND_SIGTERM":
                break
            bridge_shared_handles.backend_thread_new_card_is_generating_event.set()
            new_card = backend_card_generate_from_data(clipboard_data, bridge_shared_handles.study_topic_context)
            bridge_shared_handles.backend_thread_new_card_is_generating_event.clear()
            bridge_shared_handles.new_card_data_queue.put(new_card)
            bridge_shared_handles.backend_thread_created_card_is_ready_event.set()
        except queue.Empty:
            pass
        except APIConnectionError:
            msgbox.showerror("Card Generation Failed", "clipycards can't connect to OpenAI's servers. Press Pause, check your internet connection, and then press Resume")
            bridge_shared_handles.backend_api_connection_error_event.set()