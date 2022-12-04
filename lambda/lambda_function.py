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

from utils import recipe_parser

import os
import boto3


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
        speak_output = "Welcome, I'm a recipe bot!! you can say Hello or Hi to know more. Which would you like to try?"

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
        available_recipe = [{"name": "Paneer Tikka Masala", "url": "https://www.allrecipes.com/recipe/240652/paneer-tikka-masala/"},
                            {"name": "Crispy Rosemary Chicken and Fries",
                                "url": "https://www.allrecipes.com/recipe/77489/crispy-rosemary-chicken-and-fries/"},
                            {"name": "Miso Soup",
                                "url": "https://www.allrecipes.com/recipe/13107/miso-soup/"},
                            {"name": "Homemade Mac and Cheese",
                             "url": "https://www.allrecipes.com/recipe/11679/homemade-mac-and-cheese/"},
                            {"name": "Gingerbread Snowflakes",
                             "url": "https://www.allrecipes.com/recipe/8513071/gingerbread-snowflakes/"},
                            {"name": "Quick Beef Stir-Fry",
                             "url": "https://www.allrecipes.com/recipe/228823/quick-beef-stir-fry/"},
                            {"name": "Slow Cooker Beef Stew",
                             "url": "https://www.allrecipes.com/recipe/14685/slow-cooker-beef-stew-i/"},
                            {"name": "Perfect Sushi Rice",
                             "url": "https://www.allrecipes.com/recipe/99211/perfect-sushi-rice/"},
                            {"name": "Best Steak Marinade in Existence",
                             "url": "https://www.allrecipes.com/recipe/143809/best-steak-marinade-in-existence/"},
                            {"name": "Spiced Pear Old-Fashioned",
                             "url": "https://www.allrecipes.com/recipe/8491553/spiced-pear-old-fashioned/"},
                            {"name": "Traditional Filipino Lumpia",
                             "url": "https://www.allrecipes.com/recipe/35151/traditional-filipino-lumpia/"},
                            {"name": "Wine-Roasted Onions",
                             "url": "https://www.allrecipes.com/recipe/8489272/wine-roasted-onions/"},
                            {"name": "Washington Apple Cocktail",
                             "url": "https://www.allrecipes.com/recipe/8511288/washington-apple-cocktail/"},
                            {"name": "Air Fryer Potato Wedges", "url": "https://www.allrecipes.com/recipe/266826/air-fryer-potato-wedges/"}]




        speak_output = f"Hello there! I'm going to help you cook a delicious meal. Do you want to know the avaialble recipes?"

        attr = handler_input.attributes_manager.persistent_attributes
        attr['state'] = 'start'
        attr['available_recipe'] = available_recipe
        handler_input.attributes_manager.persistent_attributes = attr
        handler_input.attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask('add a reprompt if you want to keep the session open for the user to respond')
            .response
        )


class AvailableRecipeIntentHandler(AbstractRequestHandler):
    """Handler for Available Recipe Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AvailableRecipeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.persistent_attributes
        available_recipe = attr['available_recipe']
        speak_output = f"Here are the available recipes: "
        for recipe_index in range(len(available_recipe)):
            speak_output += f"{recipe_index + 1}. {available_recipe[recipe_index]['name']}. "
        ask_output = "Which recipe would you like to try?"
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(ask_output)
            # .ask('add a reprompt if you want to keep the session open for the user to respond')
            .response
        )

class SelectRecipeIntentHandler(AbstractRequestHandler):
    """Handler for Select Recipe Intent."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SelectRecipeIntent")(handler_input)

    def handle(self, handler_input):
        ordinal_number_map = {
            'first': 1,
            'second': 2,
            'third': 3,
            'fourth': 4,
            'fifth': 5,
            'sixth': 6,
            'seventh': 7,
            'eighth': 8,
            'ninth': 9,
            'tenth': 10,
            'eleventh': 11,
            'twelfth': 12,
            'thirteenth': 13,
            'fourteenth': 14,
            'fifteenth': 15,
            'sixteenth': 16,
            'seventeenth': 17,
            'eighteenth': 18,
            'nineteenth': 19,
            'twentieth': 20,
        }
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.persistent_attributes
        available_recipe = attr['available_recipe']
        selected_recipe = handler_input.request_envelope.request.intent.slots['count'].value
        selected_recipe = int(selected_recipe) - 1
        speak_output = f"You have selected {available_recipe[selected_recipe]['name']}. Would you like to start cooking?"

        attr['state'] = 'start_cooking'
        attr['selected_recipe'] = available_recipe[selected_recipe]
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
        attr = handler_input.attributes_manager.persistent_attributes
        selected_recipe = attr['selected_recipe']
        recipe = recipe_parser(selected_recipe['url'])
        speak_output = f"Here are the ingredients: "
        for ingredient in recipe['ingredients']:
            speak_output += f"{ingredient}. "
        #  Add preparation time and cooking time
        if recipe['prep_time'] is not None and recipe['cook_time'] is not None:
            speak_output += f"Preparation time is {recipe['prep_time']}. Cooking time is {recipe['cook_time']}."
        
        if attr['state'] == 'start_cooking':
            session_attr = {**recipe}
            session_attr['selected_recipe'] = attr['selected_recipe']
            session_attr['step'] = 0
            session_attr['state'] = 'cooking'
            speak_output = f'Great! Let\'s get started. I\'m setting up your recipe now. Please wait. I\'m done setting up your recipe {session_attr["recipeName"]}. {speak_output}'
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
            step = list(filter(
                lambda step: step['step'] == session_attr['step'], session_attr['steps']))
            if len(step) > 0:
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
                speak_output = f"The next step is {session_attr['steps'][session_attr['step']]['text']}. Would you like to hear the next step?"
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
            if session_attr["step"] > 0:
                session_attr["step"] = int(session_attr["step"]) - 1
                speak_output = f"The previous step is {session_attr['steps'][session_attr['step']]['text']}. Would you like to hear the next step?"
            elif session_attr["step"] == 0:
                speak_output = f"You are at the first step. The step is {session_attr['steps'][session_attr['step']]['text']}. Would you like to hear the next step?"
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
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            cooking_action_lexicon = {
                "stir": "Stir the ingredients together.",
                "mix": "Mix the ingredients together.",
                "bake": "Bake the ingredients in the oven.",
                "boil": "Boil the ingredients in a pot.",
                "fry": "Fry the ingredients in a pan.",
                "saute": "Saute the ingredients in a pan.",
                "grill": "Grill the ingredients on a grill.",
                "roast": "Roast the ingredients in the oven.",
                "steam": "Steam the ingredients in a pot.",
                "whisk": "Whisk the ingredients together.",
                "blend": "Blend the ingredients together.",
                "chop": "Chop the ingredients.",
                "dice": "Dice the ingredients.",
                "grate": "Grate the ingredients.",
                "mince": "Mince the ingredients.",
                "peel": "Peel the ingredients.",
                "slice": "Slice the ingredients.",
                "stir fry": "Stir fry the ingredients in a pan.",
                "simmer": "Simmer the ingredients in a pot.",
                "poach": "Poach the ingredients in a pot.",
                "broil": "Broil the ingredients in the oven.",
                "baste": "Baste the ingredients in a pan.",
                "caramelize": "Caramelize the ingredients in a pan.",
                "glaze": "Glaze the ingredients in a pan.",
                "marinate": "Marinate the ingredients in a pan.",
                "reduce": "Reduce the ingredients in a pan.",
                "shred": "Shred the ingredients.",
                "sift": "Sift the ingredients.",
                "soak": "Soak the ingredients.",
                "squeeze": "Squeeze the ingredients.",
                "stirring": "Stir the ingredients together.",
                "mixing": "Mix the ingredients together.",
                "baking": "Bake the ingredients in the oven.",
                "boiling": "Boil the ingredients in a pot.",
                "frying": "Fry the ingredients in a pan.",
                "sauteing": "Saute the ingredients in a pan.",
                "grilling": "Grill the ingredients on a grill.",
                "roasting": "Roast the ingredients in the oven.",
                "steaming": "Steam the ingredients in a pot.",
                "whisking": "Whisk the ingredients together.",
                "blending": "Blend the ingredients together.",
                "chopping": "Chop the ingredients.",
                "dicing": "Dice the ingredients.",
                "grating": "Grate the ingredients.",
                "mincing": "Mince the ingredients.",
                "peeling": "Peel the ingredients.",
                "slicing": "Slice the ingredients.",
                "stir frying": "Stir fry the ingredients in a pan.",
                "simmering": "Simmer the ingredients in a pot.",
                "poaching": "Poach the ingredients in a pot.",
                "broiling": "Broil the ingredients in the oven.",
                "basting": "Baste the ingredients in a pan.",
                "caramelizing": "Caramelize the ingredients in a pan.",
                "glazing": "Glaze the ingredients in a pan.",
                "marinating": "Marinate the ingredients in a pan.",
                "reducing": "Reduce the ingredients in a pan.",
                "shredding": "Shred the ingredients.",
                "sifting": "Sift the ingredients.",
                "soaking": "Soak the ingredients.",
                "squeezing": "Squeeze the ingredients.",
            }
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            for word in step:
                if word in cooking_action_lexicon:
                    speak_output.append(
                        f'{word}-{cooking_action_lexicon[word]} ')
            speak_output = " ".join(speak_output)
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
        ingredient_list = []
        session_attr = handler_input.attributes_manager.persistent_attributes
        for ingredient in session_attr["ingredients"]:
            ingredient_list.append(ingredient["name"].lower())
        if session_attr["state"] == "cooking":
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            for word in step:
                if word in ingredient_list:
                    speak_output.append(word)
            speak_output = ", ".join(speak_output)
            if speak_output == "":
                speak_output = "No ingredients found in this step."
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
        utensil_lexicon = {
            "bowl": "Bowl",
            "baking pan": "Baking Pan",
            "baking sheet": "Baking Sheet",
            "baking dish": "Baking Dish",
            "baking tray": "Baking Tray",
            "baking tin": "Baking Tin",
            "baking mold": "Baking Mold",
            "baking mould": "Baking Mould",
            "baking form": "Baking Form",
            "saucepan": "Saucepan",
            "pot": "Pot",
            "frying pan": "Frying Pan",
            "grill": "Grill",
            "oven": "Oven",
            "microwave": "Microwave",
            "blender": "Blender",
            "food processor": "Food Processor",
            "mixer": "Mixer",
            "whisk": "Whisk",
            "spatula": "Spatula",
            "tongs": "Tongs",
            "ladle": "Ladle",
            "sieve": "Sieve",
            "strainer": "Strainer",
            "colander": "Colander",
            "sifter": "Sifter",
            "measuring cup": "Measuring Cup",
            "measuring jug": "Measuring Jug",
            "measuring spoon": "Measuring Spoon",
            "measuring stick": "Measuring Stick",
            "pan": "Pan",
            "skillet": "Skillet",
            "wok": "Wok",
            "griddle": "Griddle",
            "grill pan": "Grill Pan",
            "grill plate": "Grill Plate",
            "grill rack": "Grill Rack",
            "grill tray": "Grill Tray",
            "grill basket": "Grill Basket",
        }
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            for word in step:
                if word in utensil_lexicon:
                    speak_output.append(
                        f'{word}-{utensil_lexicon[word]} ')
            speak_output = " ".join(speak_output)

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
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            # find time in step
            for word in step:
                if word in ["minutes", "minute", "mins", "min"]:
                    # find the number of mins before the minutes, if any
                    index = step.index(word)
                    if index > 0:
                        if step[index-1].isdigit():
                            speak_output.append(
                                f'{step[index-1]} minutes ')
                if word in ["hours", "hour", "hrs", "hr"]:
                    # find the number of mins before the minutes, if any
                    index = step.index(word)
                    if index > 0:
                        if step[index-1].isdigit():
                            speak_output.append(
                                f'{step[index-1]} hours ')

            speak_output = " ".join(speak_output)
            if speak_output == "":
                speak_output = "No time found in this step."

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
        tempreature_lexicon = {'cool oven': '200 °F or 90 °C',
                     'very slow oven': '250 °F or 120 °C',
                     'slow oven': '300-325 °F or 150-160 °C',
                     'moderate oven': '350-375 °F or 180-190 °C',
                     'moderately hot': '375-400 °F or 190-200 °C',
                     'hot oven': '400-450 °F or 200-230 °C',
                     'very hot oven': '450-500 °F or 230-260 °C',
                     'fast oven': '450-500 °F or 230-260 °C',
                     'moderately slow': '325-350 °F or 160-180 °C'
                     }
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            # find time in step
            for word in step:
                if word in ["degrees", "degree", "deg", "celsius", "celcius", "c"]:
                    # find the number of mins before the minutes, if any
                    index = step.index(word)
                    if index > 0:
                        if step[index-1].isdigit():
                            speak_output.append(
                                f'{step[index-1]} degrees celsius ')
                if word in ['fahrenheit', 'f']:
                    # find the number of mins before the minutes, if any
                    index = step.index(word)
                    if index > 0:
                        if step[index-1].isdigit():
                            speak_output.append(
                                f'{step[index-1]} degrees fahrenheit ')
                if word in ['hot', 'warm', 'cold', 'cool', 'room temperature', 'very hot', 'very cold']:
                    speak_output.append(
                        f'{word} ')
                if word in ['low', 'medium', 'high']:
                    speak_output.append(
                        f'{word} heat ')
                if word in tempreature_lexicon:
                    speak_output.append(
                        f'{word} ')


            speak_output = " ".join(speak_output)
            if speak_output == "":
                speak_output = "No temperature found in this step."
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
        session_attr = handler_input.attributes_manager.persistent_attributes
        if session_attr["state"] == "cooking":
            step = session_attr['steps'][session_attr['step']]['text']
            step = step.lower()
            step = step.split()
            speak_output = []
            # find time in step
            for word in step:
                if word in ["suggestion", "suggestions", "tip", "tips"]:
                    # find the number of mins before the minutes, if any
                    index = step.index(word)
                    if index > 0:
                        if step[index-1].isdigit():
                            speak_output.append(
                                f'{step[index-1]} suggestions ')

            speak_output = " ".join(speak_output)
            if speak_output == "":
                speak_output = "No suggestions found in this step."
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
sb.add_request_handler(AvailableRecipeIntentHandler())
sb.add_request_handler(SelectRecipeIntentHandler())
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
