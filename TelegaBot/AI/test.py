import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"

# задаем модель и промпт
model_engine = "text-davinci-003"
# задаем макс кол-во слов
max_tokens = 300



def generate_response(prompt):
    # генерируем ответ
    return openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text



class Operations:
    def __init__(self):
        self.store = {'Евроспар': 'высокого',
                 'Ашан': 'низкого',
                 'Верный': 'низкого',
                 'METRO': 'оптовый',
                 'Перекресток': 'среднего',
                 'Пятерочка': 'низко-среднего',
                 'Дикси': 'низко-среднего'
                 }
        self.store_priority = ''

    def getDiet(self, isVegan=False):
        if isVegan:
            return generate_response(f"Сделай веганский рацион питания на Завтрак, Обед, Полдник (опционально), Ужин")
        return generate_response(f"Сделай рацион питания на Завтрак, Обед, Полдник (опционально), Ужин")


    def setStore(self, store_name):
        self.store_priority=store_name
        return 'Ваш выбор сохранен'
    def getPrice(self, product_name):
        if self.store_priority!='':
            return generate_response(f"Предположи какая цена будет на {product_name} в магазине {self.store[self.store_priority]} класса в рублях")
        return generate_response(f"Предположи какая цена будет на {product_name} в магазине среднего класса в рублях")
    def getSales(self):
        return ["10% off on all fruits", "Buy one, get one free on chicken"]

    def getSchedule(self, time_period):
        return generate_response(f"Предложи план питания на {time_period}")

    def getRandomProduct(self, isVegan=False):
        if isVegan:
            return generate_response(f"Предложи идею для того, чтобы покушать вегану")
        return generate_response(f"Предложи идею для того, чтобы покушать")