# coding=utf-8
from flask import Flask, render_template, request, jsonify
#import aiml
import os
import random
import shelve

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, "../")
import cnaiml

app = Flask(__name__)

# db = shelve.open("session.db", "c", writeback=True)
# try:
#     sessionId = dict(db).keys()[0]
# except IndexError:
#     sessionId = str(int(random.uniform(10000, 50000)))  # 随机生成一个sessionId
#     db.sync()

if os.path.isfile("session.db"):
    db = shelve.open("session.db", "c", writeback=True)
    kernel = cnaiml.Kernel(sessionStore=db)
    sessionId = dict(db).keys()[0]
else:
    sessionId = str(int(random.uniform(10000, 50000)))#随机生成一个sessionId
    print sessionId
    db = shelve.open("session.db", "c", writeback=True)
    kernel = cnaiml.Kernel(sessionStore=db)
    kernel.respond('hi', sessionId)
    db.sync()

print db
print sessionId

#设置大脑
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

@app.route("/")
def hello():

    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    global db
    message = str(request.form['messageText'])

    # kernel now ready for use
    while True:
        if message == "quit":
            exit()
            return jsonify({'status': 'OK', 'answer': "和您聊天非常愉快~"})
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
            try:
                print "name"+kernel.getPredicate(name="name",sessionID=sessionId)
            except KeyError:pass
            return jsonify({'status':'OK','answer':"保存成功！"})
        elif message == "reset":
            kernel.resetBrain()
        else:
            bot_response = kernel.respond(message, sessionId)

            try:
                age = kernel.getPredicate(name="age", sessionID=sessionId)
                driveyear = kernel.getPredicate(name="driveyear", sessionID=sessionId)
                print age
                print driveyear
                if int(age)<int(driveyear):
                    kernel.setPredicate(name="driveyear", value=0, sessionID=sessionId)
                    print kernel.getPredicate(name="driveyear", sessionID=sessionId)
                    bot_response = kernel.respond("ASK DRIVE YEAR2", sessionId)
            except ValueError:pass

            db.sync()
            return jsonify({'status':'OK','answer':bot_response})
        message = ''

@app.route("/model", methods=['GET'])
def model():
    name = kernel.getPredicate(name="name",sessionID=sessionId)
    age = kernel.getPredicate(name="age", sessionID=sessionId)
    car = kernel.getPredicate(name="car", sessionID=sessionId)
    driveyear = kernel.getPredicate(name="driveyear", sessionID=sessionId)
    data = jsonify({"name":name,"age":age,"car":car,"driveyear":driveyear})
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
