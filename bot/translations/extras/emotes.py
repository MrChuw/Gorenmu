class EmoteEmotions:
    def __init__(self, data: dict):
        self.happy = data.get("happy")
        self.pog = data.get("pog")
        self.sad = data.get("sad")
