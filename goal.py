from users import *

class Goal:

    def __init__(self,value_needed: int, description: str, user: User):
        self.__value_needed = value_needed
        self.__description = description

        user.add_investment_goal(self)

    #getters
    def get_value_needed(self) -> int:
        return self.__value_needed

    def get_description(self) -> str:
        return self.__description
    
    #setters
    def set_value_needed(self, new_value: int):
        self.__value_needed = new_value

    def set_description(self, new_description: str):
        self.__description = new_description

    def add_value(self,user,value: float):

        user.set_balance(user.get_balance() - value, withdraw=True)
        self.__value_needed -= value

        if(self.__value_needed <= 0):
            print("🎉 Congratulations! You've achieved your investment goal!")
            user.get_investments_goals().remove(self)
