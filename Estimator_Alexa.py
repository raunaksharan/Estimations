"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function



# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # print("event.session.application.applicationId=" +
    #       event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # if event['session']['new']:
    #     on_session_started({'requestId': event['request']['requestId']},
    #                        event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    # elif event['request']['type'] == "SessionEndedRequest":
    #     return on_session_ended(event['request'], event['session'])


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    # print("on_intent requestId=" + intent_request['requestId'] +
    #       ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetEstimate":
        return getEstimate(intent)
    # elif intent_name == "WhatsMyColorIntent":
    #     return get_color_from_session(intent, session)
    # elif intent_name == "AMAZON.HelpIntent":
    #     return get_welcome_response()
    # elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
    #     return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")    

def getEstimate(intent):
    session_attributes = {}
    if "key" in intent["slots"]:
        spoken_jira_key = intent["slots"]["key"]["value"]
    list_json = []
    session_attributes={}
    import os
    from boto.s3.connection import S3Connection
    import subprocess
    AWS_KEY = ''
    AWS_SECRET = ''
    aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
    bucket = aws_connection.get_bucket('koios')
    #for file_key in bucket.list():
    #    print(bucket.get_key(file_key))
    key=bucket.get_key('testnssp.zip')
    os.chdir('/tmp')
    subprocess.call('rm -rf /tmp/*', shell=True)
    key.get_contents_to_filename('a.zip')
    subprocess.call(['unzip','a.zip'])
    subprocess.call('rm -rf /tmp/a.zip', shell=True)
    import sys
    sys.path.insert(0, '/tmp')
    import numpy as np
    import requests
    import pandas as pd
    import re
    stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    maxResults =  814
    total = 814
    url = "https://app.jira.ensono.com/rest/api/2/search?jql=Team=Gateway&maxResults=" + str(maxResults)
    response = requests.get(url , auth = ('RestApiUser','password@123'))
    df = response.json()
    for i in range(total):
        jira_key = df["issues"][i]["key"]
        acceptance_criteria = df["issues"][i]["fields"]["customfield_10010"]
        user_story = df["issues"][i]["fields"]["customfield_10009"]
        story_points = df["issues"][i]["fields"]["customfield_10006"]
        list_json.append([jira_key,acceptance_criteria,user_story,story_points])
    arr = np.array(list_json)
    check_list = []
    for i in range(len(arr)):
        check_list.append(arr[i][0])
#     print(check_list)
    input = 'GTWY-'+ spoken_jira_key
    index=0
    if input in check_list:
        index=check_list.index(input)
        if (arr[index][3] is not None) and (arr[index][3] != 0.0):
            print('l')
            card_title = "enter"
            speech_output = "This key has an estimate already of  " +str(arr[index][3])
            reprompt_text = "i am re-prompting "
            should_end_session = False
            return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))
    else:
        print("no")
        card_title = "enter"
        speech_output = "I am sorry ! You are not eligible to become the King in the North"
        reprompt_text = "i am re-prompting "
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    def removePunctuations(input):
        clean_words = re.sub('[^a-zA-Z]', ' ', input)
        return clean_words
    def removeStopWords(input):
    #select english stopwords
        cachedStopWords = set(stopwords)
    #add custom words
        input = input.lower()
        cachedStopWords.update(('as','i','want','so','that','scenario','given','when','then'))
    #remove stop words
        new_str = ' '.join([word for word in input.split() if word not in cachedStopWords]) 
        return new_str
    def word_cleaner(df):
        l = []
        for i, row in df.iterrows():
            temp=''
            x = removePunctuations(df['merged'][i])
            x = removeStopWords(x)
        #print(type(x))
            words = x.replace("ensono","")
            temp+=words
            l.append(temp)
        return l
    def createTrainCorpus(input_list):
        dframe = pd.DataFrame(input_list, columns = ['jira key' , 'acceptance criteria' , 'user story' , 'story points'])
        dframe = dframe[['user story','acceptance criteria' ,'story points']]
        dframe = dframe.dropna(axis = 0 , how='any')
        dframe = dframe[(dframe['story points'] != 0.0)]       
        X = pd.DataFrame(dframe[['user story','acceptance criteria']].apply(lambda x: ' \n'.join(x),axis=1))
        X.columns = ["merged"]
        #y = np.asarray(dframe['story points'].values , dtype="|S6")
        y=dframe['story points'].values
        y=y.ravel()
        y = np.char.mod('%f', y)
        return X,y
    def naiveBayes_countvect_predict(X,y,Z):
        count_vect = CountVectorizer()
        X = count_vect.fit_transform(X).toarray()
        clf = MultinomialNB().fit(X,y)
        X_new_counts = count_vect.transform(Z)
        y_pred = clf.predict(X_new_counts)
        return y_pred
    def listTest(list_json):
        l=[]
        l.append( arr[index][1] + arr[index][2])
        return l
    X,y = createTrainCorpus(list_json)
    l = listTest(list_json)
    returned_list = word_cleaner(X)
    result=naiveBayes_countvect_predict(returned_list,y,l)
    print(result)
    card_title = "enter"    
    speech_output = "I went to Mars and talked to Lex. We predict the estimate for " + str(spoken_jira_key) + " to be " + str(result)
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the JIRA key for the Gateway team"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # print("on_launch requestId=" + launch_request['requestId'] +
    #       ", sessionId=" + session['sessionId'])
    # # Dispatch to your skill's launch
    return get_welcome_response()        


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to koios. Let the games begin. To predict the estimate, tell me the JIRA key for the Gateway teamm and I am sure I can help you !" 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the JIRA key for the Gateway team"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }





# def handle_session_end_request():
#     card_title = "Session Ended"
#     speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
#                     "Have a nice day! "
#     # Setting this to true ends the session and exits the skill.
#     should_end_session = True
#     return build_response({}, build_speechlet_response(
#         card_title, speech_output, None, should_end_session))







# # --------------- Events ------------------

# def on_session_started(session_started_request, session):
#     """ Called when the session starts """

#     print("on_session_started requestId=" + session_started_request['requestId']
#           + ", sessionId=" + session['sessionId'])








# def on_session_ended(session_ended_request, session):
#     """ Called when the user ends the session.

#     Is not called when the skill returns should_end_session=true
#     """
#     print("on_session_ended requestId=" + session_ended_request['requestId'] +
#           ", sessionId=" + session['sessionId'])
#     # add cleanup logic here

