# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

from ask_sdk_model import Response

import os
import boto3
import json

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')

ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(
    table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = f"Hello there! I'm a recipe bot. I'm going to help you cook a delicious meal. Would you like to start cooking?"

        attr = handler_input.attributes_manager.persistent_attributes
        attr['state'] = 'start'
        attr['recipe_id'] = '1'
        handler_input.attributes_manager.persistent_attributes = attr
        handler_input.attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask('add a reprompt if you want to keep the session open for the user to respond')
            .response
        )


class StartCookingIntentHandler(AbstractRequestHandler):
    """Handler for Start Cooking Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('StartCookingIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = json.loads('{"link":"https://www.allrecipes.com/recipe/240652/paneer-tikka-masala/","ingredientList":[{"qty":1,"unit":"cup","name":"plain yogurt"},{"qty":1,"unit":"tablespoon","name":"ground cumin"}],"prepTime:":{"qty":15,"unit":"minutes"},"cookTime:":{"qty":1,"unit":"hour"},"totalTime:":{"qty":50,"unit":"mins"},"servings:":6,"steps":[{"step":0,"text":"In a large bowl, mix together the yogurt and cumin. Add the paneer and toss to coat. Cover and refrigerate for at least 1 hour."},{"step":1,"text":"Preheat the oven to 400 degrees F (200 degrees C)."}],"recipeName":"Paneer Tikka Masala","topYouTubeLink":"https://www.youtube.com/watch?v=hsR0JaD1TyA"}')
        attr = handler_input.attributes_manager.persistent_attributes
        speak_output = f'Okay! You need to select the recipe first!!!'
        if attr['recipe_id']:
            session_attr = {**attr, **data}
            session_attr['step'] = 0
            session_attr['state'] = 'cooking'
            speak_output = f'Great! Let\'s get started. I\'m setting up your recipe now. Please wait. I\'m done setting up your recipe {session_attr["recipeName"]}.  The first step is {session_attr["steps"][0]["text"]}. Would you like to hear the next step?'
            handler_input.attributes_manager.persistent_attributes = session_attr
            handler_input.attributes_manager.save_persistent_attributes()
        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class ContentIntentHandler(AbstractRequestHandler):
    """ Content Intent Handler returns the current step to be done for cooking. It checks the state of cook wok from an external db and return the current step. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('ContentIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr['state'] == 'cooking':
            # Find the step in steps lists
            step = list(filter(lambda step: step['step'] == session_attr['step'], session_attr['steps']))
            if len(step)>0:
                step = step[0]['text']
            speak_output = f"The current step is {step}. Would you like to hear the next step?"
        else:
            speak_output = f"Please select a recipe first."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class NextIntentHandler(AbstractRequestHandler):
    """ Next Intent Handler returns the next step to be done for cooking. It checks the state of cook wok from an external db and return the next step. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NextIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            session_attr["step"] = int(session_attr["step"]) + 1
            if session_attr["step"] == len(session_attr["steps"]):
                speak_output = f"You have completed the recipe. Would you like to start another recipe?"
                session_attr["state"] = "idle"
            else:
                speak_output = f"The next step is {session_attr['steps']int([session_attr['step']])['text']}. Would you like to hear the next step?"
                handler_input.attributes_manager.persistent_attributes = session_attr
                handler_input.attributes_manager.save_persistent_attributes()
        else:
            speak_output = f"Please select a recipe first."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class PreviousIntentHandler(AbstractRequestHandler):
    """ Previous Intent Handler returns the previous step to be done for cooking. It checks the state of cook wok from an external db and return the previous step. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PreviousIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            session_attr["step"] = int(session_attr["step"]) - 1
            if session_attr["step"] == 0:
                speak_output = f"You are at the first step. Would you like to hear the next step?"
            else:
                speak_output = f"The previous step is {session_attr['steps'][session_attr['step']]['text']}. Would you like to hear the next step?"
                handler_input.attributes_manager.persistent_attributes = session_attr
                handler_input.attributes_manager.save_persistent_attributes()
        else:
            speak_output = f"Please select a recipe first."

        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CookingActionIntentHandler(AbstractRequestHandler):
    """Cooking Action Intent Handler takes an input and returns the details of cooking action. For example if the user says stir, it returns the details of stir action. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CookingActionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Stir the ingredients for 2 minutes."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class IngredientIntentHandler(AbstractRequestHandler):
    """Ingredient Intent Handler returns the ingredients required for cooking. It checks the state of cook wok from an external db and return the ingredients. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("IngredientIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You need 2 cups of rice, 1 cup of water, 1 cup of oil, 1 cup of salt, 1 cup of pepper, 1 cup of chicken."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class UtensilIntentHandler(AbstractRequestHandler):
    """Utenstil Intent Handler returns the utensils required for cooking. It checks the state of cook wok from an external db and return the utensils. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("UtensilIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You need a wok, a spoon, a knife."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class TimeIntentHandler(AbstractRequestHandler):
    """Time Intent Handler returns the time required for cooking. It checks the state of cook wok from an external db and return the time. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TimeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "It takes 10 minutes to cook."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class TempreatureIntentHandler(AbstractRequestHandler):
    """Tempreature Intent Handler returns the temperature required for cooking. It checks the state of cook wok from an external db and return the temperature. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TempreatureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "It needs 100 degree celsius to cook."
        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CookingSuggestionIntentHandler(AbstractRequestHandler):
    """Cooking Suggestion Intent Handler returns the suggestions for cooking. It checks the state of cook wok from an external db and return the suggestions. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CookingSuggestionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can add more chicken to the wok."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(StartCookingIntentHandler())
sb.add_request_handler(ContentIntentHandler())
sb.add_request_handler(CookingSuggestionIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(IngredientIntentHandler())
sb.add_request_handler(UtensilIntentHandler())
sb.add_request_handler(TimeIntentHandler())
sb.add_request_handler(TempreatureIntentHandler())
sb.add_request_handler(CookingActionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
