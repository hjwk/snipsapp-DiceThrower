#!/usr/bin/env python3

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology.dialogue.intent import IntentMessage

import random
from util import *

CONFIG_INI = "config.ini"
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class DiceThrower(object):
    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        self.start_blocking()

    def HeadsOrTailsCallback(self, hermes: Hermes, intent_message: IntentMessage):
        hermes.publish_end_session(intent_message.session_id, "")

        heads = random.randint(0, 1)
        answer = "Face" if heads == 1 else "Pile"

        hermes.publish_start_session_notification(intent_message.site_id, answer, "")

    def ThrowDiceCallback(self, hermes: Hermes, intent_message: IntentMessage):
        hermes.publish_end_session(intent_message.session_id, "")

        answer = ""
        numberOfDices = extractSlot(intent_message.slots, "numberOfDices")
        diceType = extractSlot(intent_message.slots, "diceType")
        for _ in range(numberOfDices):
            result = random.randint(0, diceType)
            answer += "{}, ".format(result)

        hermes.publish_start_session_notification(intent_message.site_id, answer, "")

    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent("hjwk:HeadsOrTails", self.HeadsOrTailsCallback)
            h.subscribe_intent("hjwk:ThrowDice", self.ThrowDiceCallback)
            h.loop_forever()

if __name__ == "__main__":
    DiceThrower()
