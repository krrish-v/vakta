from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock

import speech_recognition as sr
import time
import pickle
from elevenlabs import generate, play, set_api_key

from books_recommend import get_pdf
from news import fetch_news_by_category, find_category

set_api_key('<API KEY>')

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

# set memory buffer window to 1 to avoid passing excessive tokens-->
memory = ConversationBufferWindowMemory(k=1) # stores previous k conversations between Ai and human

llm = ChatOpenAI(temperature=0.0,openai_api_key="<API KEY>")
memory = ConversationBufferWindowMemory(k=1)
conversation = ConversationChain(
    llm=llm,
    memory = memory,
    verbose=False
)

f= open('model1.hy', 'rb')
nlp = pickle.load(f)
f.close()

def extract_entities(text):
    doc = nlp(text)
    
    entities = ''
    for ent in doc.ents:
        if ent.label_ in ["NORP", "ORG", "GPE", "PERSON", "BOOK", "WORK_OF_ART"]:  # Filter relevant entities like nationalities, organizations, geopolitical entities, and person names
            entities+=ent.text +' '
    
    return entities



# Define the KivyMD KV language string
KV = """
<MainScreen>:
    orientation: 'vertical'
    padding: 10
    
    MDBoxLayout:
        orientation: 'vertical'
        size_hint: 1, 0.9

        MDIconButton:
            icon: "microphone"
            id: voice
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            icon_size: "200sp"
            md_bg_color: 'green'
    
    MDBoxLayout:

        MDLabel:
            id: words
            size_hint: 0.5, 0.01
            halign: 'center'
            valign: 'middle'
            text: 'Open Source Software | Hackathon 2023'
            font_size: 15

"""

# Create the main screen class
class MainScreen(BoxLayout):
    count = 0
    
    def engine(self, dt):
        self.r = sr.Recognizer()
        # self.r.energy_threshold()

        with sr.Microphone() as source:
            
            self.speaker('Speak now')
            self.r.adjust_for_ambient_noise(source,duration=1)
            self.audio= self.r.listen(source, timeout=0)

            Clock.schedule_once(self.on_voice, 0.1)


    def recog(self, dts):
        try:
            self.text = self.r.recognize_google(self.audio) # google is used a recognisor

            if self.count == 0:
                Clock.schedule_once(lambda x: self.display(self.text), 0.1)
            else:
                Clock.schedule_once(lambda x: self.read_doc(self.text), 0.1)

        except:
            self.speaker('Unable to recognise your voice Try again')
            time.sleep(1)
            Clock.schedule_once(self.engine, 0.1)
            

    # Define the callback for the voice icon press
    def on_voice(self, dt):
        self.speaker('Please wait for the response')
        self.ids.voice.md_bg_color = 'red'

        Clock.schedule_once(self.recog, 0.1)

    def display(self, sent):
        
        if 'exit' in sent:
            self.speaker('Exiting the program')
            exit()
            
        elif 'download' in sent and 'book' in sent:

            subjects = extract_entities(sent)
            if subjects != '':
                self.speaker(f'Downloading a book {subjects} form internet')
                self.doc_text = get_pdf(subjects)

                if self.doc_text is not None:
                    Clock.schedule_once(lambda x: self.read_doc(text=''), 0.1)
                else:
                    self.speaker(f'Unable to find the book {subjects} you asked for, try for some another book')
                    self.ids.voice.md_bg_color = 'green'
                    Clock.schedule_once(self.engine, 0.1)
            else: 
                self.speaker(f'Unable to get the name of a book you asked')
                self.ids.voice.md_bg_color = 'green'
                Clock.schedule_once(self.engine, 0.1)

        elif 'news' in sent or 'search' in sent:
            catg = find_category(sent)
            if catg is not None:
                news = fetch_news_by_category(catg)

                if news is not None:
                    for key, value in news.items():
                        self.speaker(f'Headline    {key}')
                        self.speaker(value)

            else: self.speaker(f'Unable to find the news of {catg}')

            self.ids.voice.md_bg_color = 'green'
            Clock.schedule_once(self.engine, 0.1)

        else:
            output = conversation.predict(input=sent)

            self.speaker(output)
            self.ids.voice.md_bg_color = 'green'            
            Clock.schedule_once(self.engine, 0.1)


    def read_doc(self, text):
        
        try:
            if 'stop' in text:
                self.count = 0
                self.speaker('Stoped reading file')
                self.ids.voice.md_bg_color = 'green'
                Clock.schedule_once(self.engine, 0.1)
            
            else:
                self.speaker(f'Starting the phase {self.count}    ' +self.doc_text[self.count])
                self.speaker(self.doc_text[self.count])
                self.count+=1
                self.ids.voice.md_bg_color = 'green'
                Clock.schedule_once(self.engine, 0.1)
        except:
            self.speaker('End of the file')


    def speaker(self, sent):
        audio = generate(
            text=sent,
            voice="Daniel",
            model="eleven_monolingual_v1"
        )

        play(audio)

    def start(self, dt):
        time.sleep(1)
        #self.speaker('Starting up the program')
        Clock.schedule_once(self.engine, 0.1)

# Create the main app class
class GUIApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Vakta VoiceBot'
        self.theme_cls.theme_style = 'Dark'

        Builder.load_string(KV)
        self.screen = MainScreen()

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return self.screen

    def on_start(self):
        # Start the engine after the app is loaded
        Clock.schedule_once(self.screen.start, 0.1)

app = GUIApp()

if __name__ == "__main__":
    app.run()
