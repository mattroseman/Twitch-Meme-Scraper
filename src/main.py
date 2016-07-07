from bots import DataBot

# read from database to get list of channels to watch
# create thread and instantiate each object to listen to the each channel
# below is example code to instantiate
myBot = DataBot.DataBot("#esl_csgo")
myBot.log_chat()
