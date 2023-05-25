import requests


class ChatGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.sessions = {}

    # Функция для взаимодействия с ChatGPT
    def handle(self, channel, _id, message):
        if self.has_session(channel, _id):
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }

            self.sessions[channel][_id].append({'role': 'user', 'content': message})

            data = {
                'model': 'gpt-3.5-turbo',
                'messages': self.sessions[channel][_id]
            }

            response = requests.post(
                'https://api.openai.com/v1/chat/completions', headers=headers, json=data)

            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    answer = data['choices'][0]['message']['content'].strip()
                    self.sessions[channel][_id].append({'role': 'assistant', 'content': answer})
                    return answer
            else:
                return "Произошла ошибка при взаимодействии с ChatGPT."

    def start_session(self, channel, _id):
        if channel not in self.sessions:
            self.sessions[channel] = {}
        self.sessions[channel][_id] = [
            {'role': 'user', 'content': 'Привет, как дела?'},
            {'role': 'system', 'content': 'Вы - пользователь'}
        ]
        return "Сессия создана"

    def has_session(self, channel, _id):
        return channel in self.sessions and _id in self.sessions[channel]

    def stop_session(self, channel, _id):
        if self.has_session(channel, _id):
            self.sessions[channel].pop(_id)
            return "Сессия удалена"
        else:
            return "У вас нет активной сессии ChatGPT"
