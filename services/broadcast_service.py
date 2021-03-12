import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
import os
import requests
import json
import subprocess
import logging
from shutil import copyfile, copytree, rmtree
import uuid
import names
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet

logger = logging.getLogger(__name__)

'''
Manages broadcast entity.
'''
class BroadcastService:
    def __init__(self):
        # nltk init
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

        # load configuration
        self.PUBLISH_API_BASE_URL = os.getenv('PUBLISH_API_BASE_URL', 'http://localhost:5000')

        self.snapshot = {}
        self.broadcast_name = ''
        self.broadcast_id = ''
        self.broadcast_full_name_with_id = ''
        self.broadcast_output_folder = ''

    """
    Main processing chain of broadcast bot publishing.
    Prepares NLU / domain based on captured FAQs, and trains a replica of broadcast with that training data.
    """
    def publish_snapshot(self, snapshot):
        logger.info('Got snapshot: ' + snapshot['id'])
        self.snapshot = snapshot
        items = snapshot['topics']

        logger.info('Publishing started.')
        self.check_output_folder()

        # enrich NLU data with dummy examples
        items_with_variations = self.generate_dummy_examples(items)

        # publish NLU data
        nlu_output_file = self.generate_nlu(items_with_variations)

        # publish domain data
        domain_output_file = self.generate_domain(items_with_variations)

        # create a copy of a broadcast bot by template
        broadcast_output = self.clone_broadcast()

        # copy generated NLU / domain to the copy of broadcast bot
        self.enrich_broadcast(nlu_output_file, domain_output_file, broadcast_output)

        # train broadcast bot
        self.train_broadcast(broadcast_output)

        # update snapshot
        self.notify_master()
    
    def check_output_folder(self):
        COACH_OUTPUT = os.getenv("COACH_OUTPUT")
        if not os.path.exists(COACH_OUTPUT):
            os.makedirs(COACH_OUTPUT)

    """
    Generates Rasa NLU based on a template and on provided user's input.
    """
    def generate_nlu(self, items):
        logger.info('Generating NLU training data.')

        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        # make a copy of NLU template
        COACH_NLU_TEMPLATE = os.getenv("COACH_NLU_TEMPLATE")
        COACH_NLU_OUTPUT = os.getenv("COACH_NLU_OUTPUT")

        try:
            copyfile(COACH_NLU_TEMPLATE, COACH_NLU_OUTPUT)
        except OSError as err:
            logger.error("Error: % s" % err)
        logger.info('Copied NLU template.')

        # open copied template and load YAML
        with open(COACH_NLU_OUTPUT, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the end of the YAML document
        logger.info('Enriching template with variations.')
        for item in items:
            # add original question
            examples = '- ' + item['question'] + '\n'

            # concatenate question variations
            for question_variation in item['question_variations']:
                examples += '- ' + question_variation + '\n'

            # prepare a new intent element
            faq_intent = {
                'intent': 'faq/' + item['topic_id'],
                'examples': pss(examples)
            }

            # add intent to the doc
            documents['nlu'].append(faq_intent)

        # save intents back to the output YAML file
        logger.info('Saving NLU training data.')
        with open(COACH_NLU_OUTPUT, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return COACH_NLU_OUTPUT

    """
    Generates variations of user's questions by enriching with synonims.
    """
    def generate_dummy_examples(self, items):

        # go through all faq examples and tokenze each question
        for item in items:
            # Word tokenizers is used to find the words
            # and punctuation in a string
            tokenized_word_list = nltk.word_tokenize(item['question'])

            # removing stop words from wordList
            stop_words = set(stopwords.words('english'))
            tokenized_word_list_non_stop = [
                w for w in tokenized_word_list if not w in stop_words]

            # Using a Tagger. Which is part-of-speech
            # tagger or POS-tagger.
            tagged_word_list = nltk.pos_tag(tokenized_word_list_non_stop)

            # go through tokenized and tagged words and get synonims for nounds and verbs
            supported_tags = ['JJ', 'NN', 'VB']
            tag_to_synset_map = {'JJ': 'a', 'NN': 'n', 'VB': 'v'}
            question_variations = []

            for tagged_word in tagged_word_list:
                word = tagged_word[0]
                tag = tagged_word[1]

                # check if the tag is supported
                if tag in supported_tags:
                    # if supported, get synonims
                    synonyms = []

                    # map word part to synset type
                    # TODO: revise this part to support wider variation set
                    word_synset_key = word + '.' + tag_to_synset_map[tag] + '.01'

                    # get synset by word
                    synset = wordnet.synset(word_synset_key)

                    # go through found lemmas, and to synonim list
                    for lemma in synset.lemmas():
                        synonyms.append(lemma.name())

                    # go through each synonim
                    for synonim in synonyms:
                        # skip the word itself
                        if word != synonim:
                            # add question variation with a synonim
                            question_variation = item['question'].replace(
                                word, synonim)
                            question_variations.append(question_variation)

            # enrich original example with question variations
            item['question_variations'] = question_variations

        return items

    """
    Generates Rasa domain based on a template and on provided user's input.
    """
    def generate_domain(self, items):
        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        # make a copy of domain template
        COACH_DOMAIN_TEMPLATE = os.getenv("COACH_DOMAIN_TEMPLATE")
        COACH_DOMAIN_OUTPUT = os.getenv("COACH_DOMAIN_OUTPUT")
        try:
            copyfile(COACH_DOMAIN_TEMPLATE, COACH_DOMAIN_OUTPUT)
        except OSError as err:
            logger.error("Error: % s" % err)

        # open copied template and load YAML
        with open(COACH_DOMAIN_OUTPUT, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the responses section of the YAML document
        for item in items:
            # prepare a new intent element
            intent = 'utter_faq/' + item['topic_id']
            text = [{'text': item['answer']}]

            # add response to the doc
            documents['responses'][intent] = text

        # save intents back to the output YAML file
        with open(COACH_DOMAIN_OUTPUT, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return COACH_DOMAIN_OUTPUT


    """
    Creates a replica of a Broadcast bot
    """
    def clone_broadcast(self):
        # get broadcast template and output config
        COACH_BROADCAST_BOT_TEMPLATE = os.getenv("COACH_BROADCAST_BOT_TEMPLATE")
        COACH_BROADCAST_BOT_OUTPUT = os.getenv("COACH_BROADCAST_BOT_OUTPUT")

        # generate broadcast clone name
        logger.info('Cloning broadcast bot.')

        self.broadcast_name = names.get_full_name()
        logger.info('Broadcast name: ' + self.broadcast_name)

        self.broadcast_id = uuid.uuid4().hex
        logger.info('Broadcast ID: ' + self.broadcast_id)

        self.broadcast_full_name_with_id = self.broadcast_name.replace(
            " ", "_") + "_" + self.broadcast_id
        self.broadcast_output_folder = COACH_BROADCAST_BOT_OUTPUT + \
            "/" + self.broadcast_full_name_with_id

        # make a copy of template broadcast folder
        try:
            copytree(
                COACH_BROADCAST_BOT_TEMPLATE, self.broadcast_output_folder)
        except OSError as err:
            logger.error("Error: % s" % err)

        logger.info('Cloned broadcast bot to folder: ' + self.broadcast_output_folder)

        # return copied folder path
        return self.broadcast_output_folder


    """
    Updates replica of a Broadcast bot with generated NLU and domain
    """
    def enrich_broadcast(self, broadcast_nlu_file, broadcast_domain_file, broadcast_output_folder):
        # copy published NLU file to the target broadcast clone
        COACH_BROADCAST_BOT_NLU_OUTPUT = os.getenv(
            "COACH_BROADCAST_BOT_NLU_OUTPUT")
        broadcast_nlu_target_path = broadcast_output_folder + COACH_BROADCAST_BOT_NLU_OUTPUT
        try:
            copyfile(broadcast_nlu_file, broadcast_nlu_target_path)
        except OSError as err:
            logger.error("Error: % s" % err)

        # copy published file to the target broadcast clone
        COACH_BROADCAST_BOT_DOMAIN_OUTPUT = os.getenv(
            "COACH_BROADCAST_BOT_DOMAIN_OUTPUT")
        broadcast_domain_target_path = broadcast_output_folder + \
            COACH_BROADCAST_BOT_DOMAIN_OUTPUT
        try:
            copyfile(broadcast_domain_file, broadcast_domain_target_path)
        except OSError as err:
            logger.error("Error: % s" % err)


    """
    Trains Rasa model within Broadcast bot replica
    """
    def train_broadcast(self, broadcast_output):
        logger.info('Broadcast bot training starting.')
        
        # prepare Rasa training command
        broadcast_train_command = [
            "rasa",
            "train",
            "--force",
            "--verbose",
            "--debug"
        ]

        # create a subprocess for rasa train command, setting current working directory to the broadcast's directory
        process = subprocess.Popen(broadcast_train_command,
                                cwd=broadcast_output,
                                stdout=subprocess.PIPE,
                                universal_newlines=True
                                )

        # run broadcast bot training
        while True:
            output = process.stdout.readline()
            logger.info(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    logger.info(output.strip())
                    logger.info('Broadcast bot training completed.')
                break

        logger.info('Broadcast bot is ready.')
    
    def notify_master(self):
        # prepare request
        request_url = f"{self.PUBLISH_API_BASE_URL}/user/{self.snapshot['user_id']}/snapshot/{self.snapshot['id']}"
        payload = {
            'broadcast_name': self.broadcast_name
        }

        # call publish API
        try:
            response = requests.put(request_url, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code == 201 and response.json():
            body = response.json()
            return body.get('id', '')

