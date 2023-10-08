# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Text, Union
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sqlite3

class ActionAskBusinessName(Action):
    def name(self):
        return "action_ask_business_name"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_ask_user_business")
        return []

class ActionAskBusinessType(Action):
    def name(self):
        return "action_ask_business_type"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_buy_or_rent")
        return []

class ActionCompanyInfo(Action):
    def name(self):
        return "action_company_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_company_info")
        return []

class ActionPaymentMethod(Action):
    def name(self):
        return "action_payment_method"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_payment_method")
        return []
    
class ActionMakeAppointment(Action):
    def name(self):
        return "action_make_appointment"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Of course, you can make an appointment to see the house. Please tell me the time and date that is convenient for you, and we will arrange someone to accompany you to see the house.")
        return []
    
class ActionBuyProcess(Action):
    def name(self):
        return "action_buy_process"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_buy_process")
        return []


class ActionRentProcess(Action):
    def name(self):
        return "action_rent_process"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_rent_process")
        return []
    
class ActionBuyContract(Action):
    def name(self):
        return "action_buy_contract"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_buy_contract")
        return []

class ActionRentContract(Action):
    def name(self):
        return "action_rent_contract"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_rent_contract")
        return []

        
class ActionPropertyManagement(Action):
    def name(self):
        return "action_property_management"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_property_management")
        return []


class ActionAskHouseCode(Action):
    def name(self):
        return "action_ask_house_code"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Sure! Could you please provide the house code you want to inquire about?")
        return []


class ActionShowHouseInfo(Action):
    def name(self):
        return "action_show_house_info"

    def run(self, dispatcher, tracker, domain):
        house_code = tracker.get_slot("house_code")
        if house_code:
            conn = sqlite3.connect('houses.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM houses WHERE id=?", (house_code,))
            house_info = cursor.fetchone()
            conn.close()

            if house_info:
                id, area, sale_price, rent_price, location = house_info
                dispatcher.utter_message(f"The house with code {id} has the following information:\n"
                                       f"Area: {area}\n"
                                       f"Sale Price: {sale_price}\n"
                                       f"Rent Price: {rent_price}\n"
                                       f"Location: {location}")
            else:
                dispatcher.utter_message("Sorry, I couldn't find information for that house code.")
        else:
            dispatcher.utter_message("I'm not sure which house you're asking about. Can you please provide the house code?")
        return []
    
class ActionAskSearchCondition(Action):
    def name(self):
        return "action_ask_search_condition"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Please provide the area range, price range and location of the house you want to search for.")
        return []
    
class FormExecuteCondition(FormValidationAction):
    def name(self) -> Text:
        return "form_execute_condition"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["area_range", "price_range", "location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "area_range": [self.from_entity(entity="number", role="area")],
            "price_range": [self.from_entity(entity="number", role="price")],
            "location": [self.from_entity(entity="location")]
        }

    def validate(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        errors = []

        area_range = tracker.get_slot('area_range')
        if area_range:
            try:
                min_area, max_area = map(float, area_range.split('-'))
            except ValueError:
                errors.append({"name": "area_range", "message": "请按照'min-max'的格式提供面积范围。"})
        else:
            errors.append({"name": "area_range", "message": "请按照'min-max'的格式提供面积范围。"})

        price_range = tracker.get_slot('price_range')
        if price_range:
            try:
                min_price, max_price = map(float, price_range.split('-'))
            except ValueError:
                errors.append({"name": "price_range", "message": "请按照'min-max'的格式提供价格范围。"})
        else:
            errors.append({"name": "price_range", "message": "请按照'min-max'的格式提供价格范围。"})

        location = tracker.get_slot('location')
        if not location:
            errors.append({"name": "location", "message": "请提供地点。"})

        if errors:
            return {"validation_errors": errors}

        return [SlotSet("area_range", area_range), SlotSet("price_range", price_range), SlotSet("location", location)]
    

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        min_area, max_area = map(float, tracker.get_slot('area_range').split('-'))
        min_price, max_price = map(float, tracker.get_slot('price_range').split('-'))
        location = tracker.get_slot('location')

        # Database Query
        conn = sqlite3.connect('houses.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM houses WHERE area BETWEEN ? AND ? AND sale_price BETWEEN ? AND ? AND location=?", (min_area, max_area, min_price, max_price, location))
        houses = cursor.fetchall()
        conn.close()

        if houses:
            dispatcher.utter_message(text="Here are the houses based on your criteria:")
            for house in houses:
                id, area, sale_price, rent_price, location = house
                dispatcher.utter_message(text=f"House ID: {id}, Area: {area} sq.m, Sale Price: {sale_price}, Rent Price: {rent_price}, Location: {location}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any houses that match your criteria.")

        return []
    

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I'm sorry, I don't understand. You are being transferred to a human customer service for further assistance.")
        return []


 

    

    
        
        

 
 
    
 

