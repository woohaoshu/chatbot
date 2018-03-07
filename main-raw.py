#import aiml
import os

import sys
sys.path.insert(0, "../")
import cnaiml

kernel = cnaiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
    # kernel.saveBrain("bot_brain.brn")

# kernel now ready for use
while True:
    message = raw_input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    elif message == "name":
        print kernel.getPredicate(name="name")
    else:
        bot_response = kernel.respond(message)
        print bot_response

