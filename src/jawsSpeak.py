import comtypes.client
def speak(text: str):
    jaws = comtypes.client.CreateObject("FreedomSci.JawsAPI")
    jaws.SayString(text)
