class Strategy:

    def __init__(self, name, priority_list, conditions, modifiers):
        self.name = name
        self.priority_list = priority_list
        self.conditions = conditions

        for key in modifiers.keys():
            setattr(self, key, modifiers[key])