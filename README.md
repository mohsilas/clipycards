<div align="center">
  <img src="https://github.com/user-attachments/assets/eed501b7-9b49-42a7-8e55-707df713c63e" width="300" />
</div>
<br>
<div align="center">
  <img/ src="https://github.com/user-attachments/assets/480ddebe-2404-4a67-abe6-e3768e8224ee" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/69c67088-dcaf-4074-aa70-8fc42cb5f018" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/beef504c-1753-47f2-93b6-a266ab265090" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/80d8a92d-04bb-4829-9073-85232107e4a3" height="25">
</div>
<br>


> A tiny app that automatically creates flashcards from the clipbaord using GPT.
> <p>Wanna turn <mark>this</mark> into a flashcard? Control+C... Done.</p>

# 📖 Table of Contents
* [Intro](#-intro)
* Installation
* [Build/dependancies](#-builddependancies)
* [Usage](#-usage)
* [Config](#-config)
* [Themes](#-themes)
* [Documentation](#-documentation)
* [License](#-license)
## 📑 Intro
It is a truth universally acknowledged, at least among med students, that creating flashcards consumes time. And so, with the advent of AI, it became possible to delegate such a task to a semantically intellegent machine. This however, posed new problems, namely; the price of services, model hallucinations, and the fact that turning your entire lecture sheet into flashcards generates a lot of redundancy.

**Price**: ClipyCards solves the problem of price by allowing you to use your own API key, currently OpenAI's. You can turn the entire Harry Potter series into falshcards (yes, including the last book) with GPT3.5 at $2, or the new 4o-mini at $0.75. You can also use beefier models like GPT4. Oh, and APIs are a per-use charge, not a monthly subscription.

**Hallucinations**: ClipyCards uses retrieval augmented generation (RAG), meaning that it keeps the context of your study session and generates cards from and around that context. When you copy a chunk of text, the app feeds this text, along with relevant context from its temporary study session database, into GPT and then retrieves the generated card with its prompt (in case you wanted to regenerate or modify the prompt).

**Redundancy**: You can just copy your entire lecture sheet, or copy the parts that needs remembering, thus generating specific cards.

**Don't want flashcards?** You can configure ClipyCards' prompt to generate bulletins, TLDR cards, QA sheets, etc,

## 🛠️ Installation

## 🧱 Build/dependancies
### dependancies
* OpenAI (used version 1.30.3)
```
pip install openai
```
* FIASS (used version 1.8.0)
```
pip install faiss-cpu
```
* Pyperclip (used version 1.8.2)
```
pip install pyperclip
```
* Customtkinter (used version 5.2.2)
```
pip install customtkinter
```
* numpy (used version 1.22.0)
```
pip install numpy
```

### Building on MacOS/Windows
After cloning or downloading the src file, there're many ways to build the python app. Here we use py2app/py2exe.
1. install py2app with pip for MacOS
```
pip install py2app
```
  1.5 install py2exe if you're using windows
```
pip install py2exe
```
2. navigate to the src file
3. run the build command (for Windows, replace py2app with py2exe)
```
python setup.py py2app -O2 -S --semi-standalone
```
This builds a relatively small app that depends on having python installed on machine, flags:
  * -O2 : optimize = 2.
  * --semi-standalone : don't copy the python framework into the app. Removing this flag will result in a standalone app that can run on any machine (of the same OS), but the app's size will be large... very large.

## 🎠 Usage
<details>
<summary>0. provide an OpenAI API key</summary>
  
When you first run the app, it requires an API key to run. You can get it by signing up or loging with your free OpenAI account into [OpenAI Platform](https://platform.openai.com/account/api-keys) Remember to store it somewhere safe (like in a password manager). Then copy to ClipyCards welcome window as shown below (this is just an example of how an API key looks like):
  
<img width="512" alt="Screenshot 2024-07-23 at 5 49 28 PM" src="https://github.com/user-attachments/assets/951db6f4-d977-40bf-8882-4608c601462c">

</details>

<details>
<summary>1. Give a study context </summary>

In order to keep the study session's general context, you have to provide a study context. i,e title of the topic and/or some overview snipt of the topic.
Here, I just provided a title.

<img width="712" alt="Screenshot 2024-07-23 at 5 53 25 PM" src="https://github.com/user-attachments/assets/dd7be026-0564-45dd-8b65-e8557aec0c99">

</details>
<details>
<summary>2. Want a flashcard? Control+C... Done </summary>
  
Now you just study, and control+C whatever piece of info you want clipycards to generate a flashcard from. In This case, some info about kidney failure (I'm a medico!).

<img width="932" alt="Screenshot 2024-07-23 at 5 58 16 PM" src="https://github.com/user-attachments/assets/59e83527-119b-4284-8bd0-0da0f221f2c4">

</details>
<details>
<summary> Buttons' manual </summary>

* gear icon: pops up a menu for regenrating, re-prompting, or editing a card.
* Pause/Resume: pauses the card generation, in case you want to copy something without clipycards turning it into a card.
* New context: create new context for a new study topic, you can also clear the cards and generate new ones.
* export: export cards into text or sheet files, which is all you need because most apps (including Anki) can import such formats.
</details>


## ⚓ Config
You can configure clipycards using a config file located in your home directory. This is the default config file:
  
```json
{
    "about": "version: 1.0 | dev: mohsilas | default themes: light, dark, rose-pine | need help with this config, or creating themes? visit clipycards.com",
    "key": "<your-api-key-is-stored-here!",
    "role": "system",
    "main-model": "gpt-3.5-turbo",
    "sys_prompt": "you are a system that generates Q&As from provided info. Here is a general idea about the info you will be provided:<br><study_topic_context><br>Here're some pervious interactions to improve your responses:<br><similar_context><br>keeping with the previous context, turn the following info into a Q&A in the exact format of \"question? | answer\". If multiple Q&As were generated, separate them by an empty line.",
    "temp": 1,
    "top_p": 1,
    "context_length": 3,
    "backend_thread_clipboard_queue_timeout": 4,
    "frontend_cards_export_format_separator": " | ",
    "theme": "rose-pine",
    "internet_ping_server": ["8.8.8.8", 53]
}
```
Now, let's break it down :).

* key: your OpenAI API key is stored here, I know it's practice to store it in an env, but if an adversary has access to your home dir, an API key is the least of your worries.
* role: a model paramater that you shouldn't touch :)
* main-model: the underlying AI that generates the cards' text. [Models list](https://platform.openai.com/docs/models)
* sys_prompt: the prompt used to generate the cards, \<br> is a line break.  <study_topic_context> is a general study context,  <similar_context> is replaced with the relevant context from previous cards.
* temp: A value between 0.2 and 0.8 can be effective. Lower values (e.g., 0.2) produce more focused and deterministic responses, while higher values (e.g., 0.8) allow for more randomness. [souce](https://medium.com/nerd-for-tech/model-parameters-in-openai-api-161a5b1f8129)
* top_p: Higher values (e.g., 0.9) make the model consider a broader range of possibilities, while lower values (e.g., 0.3) make it more selective. [souce](https://medium.com/nerd-for-tech/model-parameters-in-openai-api-161a5b1f8129)
*  context_length: number of context chunks (previous cards/copied info) used to generate a single card.
*  backend_thread_clipboard_queue_timeout: for those with some programming experience, this basically makes the backend thread wait n seconds for a new queue (new clipboard data).
*  frontend_cards_export_format_separator: in accordince with the prompt, allows parsing the cards into a csv format. (i.e. question | answer = column1: question | column2: answer)
*  theme: there are three default themes (light, dark, rose-pine), you can also create your own theme and insert the path here (e.g. "my\theme\path\mytheme.json").
*  internet_ping_server: the IP and port of the internet server clipyCards pings to check connectivity, this one is google's.

> [!TIP]
> to find your home dir, type this on your terminal/cmd:
```
cd ~
```
## 🪣 Themes
There are three default themes: light, dark, rose-pine.
To use your own theme, open the config file and replace the default theme with a path to your theme file (json file).

<details>
<summary>Click to see the default rose-pine theme json</summary>
  
```json
{
        "sys-mode": "dark",
        "main-fg-color": "#191723",

        "subwn-txt-color": "#E0DEF2",
        "subwn-fg-color": "#191723",
        "subwn-btn-color": "#BFA8E3",
        "subwn-cancel-btn-color": "#BFA8E3",
        "subwn-btn-txt-color": "#440000",
        "subwn-btns-hover-color": "#E0DEF2",
        "subwn-tarea-fg": "#191723",

        "title-font": ["Times", 22],
        "title-text-color": "white",
        "title-fg-color": "#191723",
        "title-corner-radius": 0,

        "mframe-fg-color": "#191723",
        "mframe-corner-radius": 0,
        "mframe-border-width": 0,
        "mframe-border-color": "white",
        "mframe-scrlbar-fg-color": "#191723",
        "mframe-scrlbar-hover-color": "#E0DEF2",
        "mframe-scrlbar-btn-color": "#191723",

        "cards-alt-colors": ["#252337", "#191723"],
        "cards-corner-radius": 20,
        "cards-font": ["Helvetica", 15],
        "cards-txt-pady": 5,
        "cards-txt-padx": 5,
        "cards-txt-color": "#E0DEF2",
        "card-btns-txt-color": "#E0DEF2",
        "card-btns-hover-color": "#BFA8E3",
        "card-btn-opts-icon": "⚙︎",
        "cards-btn-icon-font": ["Helvetica", 20],

        "footer-fg-color": "#191723",
        "footer-corner-radius": 0,
        "footer-border-width": 0,
        "footer-border-color": "white",

        "btn-export-txt-color": "#440000",
        "btn-export-fg-color": "#BFA8E3",
        "btn-export-hover-color": "#E0DEF2",
        "btn-export-corner-radius": 5,
        "btn-export-border-width": 1,
        "btn-export-border-color": "#BFA8E3",

        "btn-pause-txt-color": "#440000",
        "btn-pause-fg-color": "#BFA8E3",
        "btn-pause-hover-color": "#E0DEF2",
        "btn-pause-corner-radius": 5,
        "btn-pause-border-width": 1,
        "btn-pause-border-color": "#BFA8E3",

        "btn-ncontext-txt-color": "#440000",
        "btn-ncontext-fg-color": "#BFA8E3",
        "btn-ncontext-hover-color": "#E0DEF2",
        "btn-ncontext-corner-radius": 5,
        "btn-ncontext-border-width": 0,
        "btn-ncontext-border-color": "#BFA8E3",

        "optsmenu-fg-color": "#BFA8E3",
        "optsmenu-text-color": "#440000",
        "optsmenu-btn-color": "#BFA8E3",
        "optsmenu-btn-hover-color": "#E0DEF2",
        "optsmenu-btn-padding-color": "#BFA8E3",
        "optsmenu-corner-radius": 5,
        "optsmenu-border-width": 1,
        "optsmenu-border-color": "#BFA8E3",

        "wait-animation": ["⠁", "⠂", "⠄", "⡀", "⡈", "⡐", "⡠", "⣀", "⣁", "⣂", "⣄", "⣌", "⣔", "⣤", "⣥", "⣦", "⣮", "⣶", "⣷", "⣿", "⡿", "⠿", "⢟", "⠟", "⡛", "⠛", "⠫", "⢋", "⠋", "⠍", "⡉", "⠉", "⠑", "⠡", "⢁"]
        }
```
</details>

## 📘 Documentation
This is a fairly tiny app, hence the docs are selective.
### Docs table
<details>
<summary>Overview: how clipycards works</summary>
  
The following psudocode represents the general structure of the app.
```python
frontend_clipboard_listener():
  if new_clipboard_data != old_clipboard_data:
    clipboard_queue.push(new_clipboard_data)
    old_clipboard_data = new_clipboard_data
    frontend_clipboard_listener() # I don't actualy use raw recursion, but the concept is the same.

frontend_new_card_generated_listener():
  if new_card_generated_queue.has_data():
    gui.update.add_new_card(text=new_card_generated_queue.text)
    frontend_new_card_generated_listener()

backend_start_api_caller_theard():
  while(thread_is_active.is_set()):
    if clipboard_queue.has_data():
      new_card_generated_queue.push(api.response(request=prompt+queue.get_data()))

main():
  frontend_clipboard_listener()
  frontend_newcards_from_api_listener()
  thread = backend_start_api_caller_theard()
  thread.start()
```
</details>

<details>
<summary>The frontend (clipycards.py) </summary>

I used [Customtkinter](https://customtkinter.tomschimansky.com/) for the GUI (which wasn't a great idea btw), and tkinter for the popup menu element. The theme (GUI color palatte) is either loaded from a dictionary in the theme.py module, or from a .json file.

The frontend is the main module, and when it's executed, it runs a bunch of checks before starting the main window. If any of them failed, it exits(), popping an error msg and leaving some info in a log file.
The checks are:
* is the config file loaded and validated?
* did the GUI initiate successfuly?
* is there an internet connection?
* does the api key work?
* did the user provide a study context?

There're three classes in the frontend:
* BridgeSharedHandles: holds the queues, vars, and thread events to allow communication with the backend (as pointed in the overview).
* GuiAppMain: ctk class for the main window.
* LargeTextInputDialog: ctk class for secondary windows.

</details>

<details>
<summary>The backend </summary>
  
The backend uses backend_api_response_get(str)->str to get response from OpenAI's API, or other APIs in the future, as such it is called by two functions:
```python
backend_card_generate_from_data(str: request, str:study_topic_context) -> [str, str] # this generates the card according to the sys_prompt, and also outputs the context+prompt used
backend_study_context_title_generate(str: study_topic_context) -> str # this takes in the study context and provides a title
```

With every API call, the functions responsible for keeping the context are also called (because LLMs don't have memory, so you'd have to feed them context with every API call). These context-keeping funcions use methods from [FAISS library](https://faiss.ai/) and the [OpenAI's text embedding model](https://openai.com/index/introducing-text-and-code-embeddings/).
```python
backend_embedding_generate(str: text) -> embd # embd is a 1x256 np array of 32floats, not a real datatype btw. This one calls the embedding model.
backend_embedding_index_db_add(str: text) -> None # calls backend_embedding_generate() to generate embedding and store it in a FIASS database, and appends the str to embedding_text_db (simple list).
back_endembedding_index_db_search_similar(embd: text_embedding) -> list # searches the FAISS database for similar embeddings, gets their indexes, and uses the indexes to return a list of similar texts from embedding_text_db (something like, [embedding_text_db[i] for index in indexes]).
```

</details>

## 🎫 License
This project falls under the [GNU general public license.](https://github.com/mohsilas/clipycards/blob/main/LICENSE)
