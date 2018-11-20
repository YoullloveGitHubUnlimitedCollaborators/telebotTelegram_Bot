first_name = 'UsefulEvrDay'
bot_ame = 'Uzfl_bot'


telegram_token = '658823571:AAGBwNV0kx1UEcXSqU3uL_RMcyh8Hmvk-w0'
weather_token = '&appid=bd10adefbae8b8f09f03d695f271cda3'
telegram_api_url = "https://api.telegram.org/bot{}/"
bank_api_url1 = "http://www.nbrb.by/API/ExRates/Rates?"
bank_api_url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
weather_api_url = "http://api.openweathermap.org/data/2.5/"

telegram_methods = {'updates': 'GetUpdates', 'send': 'sendMessage'}
weather_methods = {'day': 'weather?q=', 'week': 'forecast?q='}
bank_methods = {'today':'&Periodicity=0' , 'onDate':'onDate='}