# LLM API Pipeline — Классификация отзывов с OpenRouter AI


##  Описание проекта

Скрипт автоматически классифицирует отзывы пользователей с помощью LLM (Large Language Model) через API OpenRouter AI. Для каждого отзыва определяется:
- **Тональность** (positive/negative/neutral)
- **Тема** отзыва (например, "customer service", "product quality", "battery life")

Результаты сохраняются в структурированном JSON-формате.


##  Цель работы

Разработать рабочий API-пайплайн, который:
1. Читает входные данные из CSV-файла
2. Отправляет запросы к LLM через OpenRouter API
3. Получает структурированный JSON-ответ
4. Сохраняет результаты в JSON-файл


##  Технологии

- **Python 3.14** - язык программирования
- **OpenRouter API** - доступ к LLM
- **Pandas 3.0.3** - обработка CSV файлов
- **OpenAI SDK 2.36.0** - для взаимодействия с API


##  Структура проекта

```

Data2sem/
├── README.md # Документация проекта
├── requirements.txt # Зависимости Python
├── script.py # Основной скрипт пайплайна
├── input_reviews.csv # Входные данные (отзывы)
├── output_result.json # Результаты работы (создается автоматически)
└── env.example # Конфигурация с API-ключом (нужно переименовать и вставить свой API key)

```


##  Установка и запуск

### 1. Скачайте проект из репозитория

### 2. Установка зависимостей
```

pip install -r requirements.txt

```

### 3. Настройка API ключа OpenRouter

>  **Важно**: для регистрации и получения ключа потребуется VP*, далее в OpenRouter будет использоваться Deepseek V4 flash, поэтому при работе скрипта VP* не потребуется.

1. **Зарегистрируйтесь** на платформе [OpenRouter.ai](https://openrouter.ai)
<img width="1895" height="564" alt="Снимок экрана 2026-05-13 171517" src="https://github.com/user-attachments/assets/1fbe58c2-3254-44ca-8702-0d4918ec0984" />

2. **Перейдите** в раздел **Get API key**: https://openrouter.ai/keys
3. Нажмите **New Key** и дайте название ключу.
<img width="632" height="250" alt="Снимок экрана 2026-05-13 171544" src="https://github.com/user-attachments/assets/293b7b9b-0370-4304-9088-d688e7e76f3a" />
 <img width="521" height="566" alt="Снимок экрана 2026-05-13 171600" src="https://github.com/user-attachments/assets/1ea63cf6-8512-42c7-9a83-ef0e63a01178" />

4. Скопируйте **ключ** вида sk-or-v1-xxx...
<img width="519" height="332" alt="Снимок экрана 2026-05-13 171626" src="https://github.com/user-attachments/assets/8286bfc4-ebad-4700-baa9-be15da67bdd5" />

5. Вставьте ключ в файл env.example, затем переименуйте его в .env


### 4. Подготовка входных данных

Файл input_reviews.csv должен содержать колонки:

    • id - уникальный идентификатор отзыва

    • review_text - текст отзыва

Пример:

```

id,review_text
1,"The product is amazing! Works perfectly and fast delivery."
2,"Not worth the money. Broke after 2 days."

```


### 5. Запустите script.py

### 6. Выходные данные (output_result.json)

```

{
  "statistics": {
    "total_reviews": 3,
    "sentiment_counts": {
      "positive": 1,
      "negative": 1,
      "neutral": 1,
      "error": 0
    },
    "positive_percentage": 33.33,
    "negative_percentage": 33.33,
    "neutral_percentage": 33.33
  },
  "reviews": [
    {
      "id": "1",
      "review": "The product is amazing! Works perfectly and fast delivery.",
      "classification": {
        "sentiment": "positive",
        "topic": "product quality"
      }
    },
    {
      "id": "2",
      "review": "Not worth the money. Broke after 2 days.",
      "classification": {
        "sentiment": "negative",
        "topic": "durability"
      }
    },
    {
      "id": "3",
      "review": "It's okay. Nothing special but does the job.",
      "classification": {
        "sentiment": "neutral",
        "topic": "performance"
      }
    }
  ]
}

```


## Настройка модели

### По умолчанию используется модель **deepseek/deepseek-v4-flash**. Вы можете изменить её в файле script.py:

Deepseek доступен из России, при запуске скрипта не требуется включать никаких обходов блокировок

```

MODEL = "openai/gpt-5.4-mini"
MODEL = "deepseek/deepseek-v4-flash"

```

Работоспособность скрипта будет зависеть от API: количество токенов, регион, VP*.

Список доступных моделей: https://openrouter.ai/models
<img width="1050" height="171" alt="Снимок экрана 2026-05-13 180313" src="https://github.com/user-attachments/assets/de3f3e14-4278-4725-94a7-f5b31c14f3ac" />



## Обработка ошибок

Скрипт корректно обрабатывает:

    • Отсутствие API-ключа

    • Проблемы с чтением CSV файла

    • Ошибки сети/API

    • Некорректные JSON-ответы от LLM

    • Пустые или некорректные отзывы

При ошибках:

    • В консоль выводится сообщение об ошибке

    • В результатах отображается "sentiment": "error" и "topic": "api_failed"



## Устранение неполадок

### **Ошибка: OPENROUTER_API_KEY not found**

**Решение:** Убедитесь, что:

    - Файл .env существует в корне проекта

    - В файле прописано OPENROUTER_API_KEY=ваш_ключ


### **Ошибка: input_reviews.csv not found**

**Решение**: Проверьте, что файл находится в той же папке, что и script.py

### **Ошибка аутентификации API**
**Решение:**

    - Проверьте правильность API-ключа

    - Убедитесь, что API работает

