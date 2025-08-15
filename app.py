import os
from flask import Flask, request, jsonify, render_template
from opensearchpy import OpenSearch
from faker import Faker
import random

app = Flask(__name__)
fake = Faker()

OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST', 'localhost')
OPENSEARCH_PORT = int(os.getenv('OPENSEARCH_PORT', 9200))

client = OpenSearch(
    hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
    http_auth=None,
    use_ssl=False,
    verify_certs=False,
)

INDEX_NAME = 'documents'
INDEX_MAPPING = {
    'mappings': {
        'properties': {
            'title': {'type': 'text'},
            'content': {'type': 'text'},
            'content_type': {'type': 'keyword'}
        }
    }
}

def create_index():
    """Создание индекса если он не существует"""
    try:
        exists = client.indices.exists(INDEX_NAME)
        print(f"Проверка существования индекса {INDEX_NAME}: {exists}")
        if not exists:
            print(f"Создание индекса {INDEX_NAME}")
            result = client.indices.create(INDEX_NAME, body=INDEX_MAPPING)
            print(f"Результат создания индекса: {result}")
            return True
        return True
    except Exception as e:
        print(f"Ошибка при создании индекса: {e}")
        return False

def generate_sample_data():
    """Генерация тестовых данных"""
    content_types = ['article', 'blog', 'news', 'review']
    documents = [
        {
            'title': 'Новые технологии в разработке ПО',
            'content': 'Современные технологии разработки программного обеспечения постоянно развиваются. Искусственный интеллект и машинное обучение становятся неотъемлемой частью процесса.',
            'content_type': 'article'
        },
        {
            'title': 'Обзор популярных фреймворков',
            'content': 'React, Vue и Angular остаются самыми востребованными фреймворками для веб-разработки. Каждый имеет свои преимущества и особенности.',
            'content_type': 'review'
        },
        {
            'title': 'Технологические тренды 2025',
            'content': 'Квантовые вычисления и блокчейн технологии продолжают привлекать внимание крупных компаний. Инвестиции в эти направления растут.',
            'content_type': 'news'
        },
        {
            'title': 'Мой опыт с микросервисами',
            'content': 'Использование микросервисной архитектуры позволило нам значительно улучшить масштабируемость проекта. Делюсь опытом внедрения.',
            'content_type': 'blog'
        },
        {
            'title': 'Безопасность в современных приложениях',
            'content': 'Обеспечение безопасности веб-приложений становится все более важным. Рассмотрим основные принципы и технологии защиты данных.',
            'content_type': 'article'
        }
    ]
    
    print("Генерация тестовых документов")
    for doc in documents:
        print(f"Создан документ: {doc}")
    
    print("Индексация документов")
    for i, doc in enumerate(documents):
        try:
            result = client.index(
                index=INDEX_NAME,
                body=doc,
                id=str(i+1),
                refresh=True
            )
            print(f"Документ {i+1} проиндексирован: {result}")
        except Exception as e:
            print(f"Ошибка при индексации документа {i+1}: {e}")

def search_documents(keyword, content_type=None):
    """Поиск документов по ключевому слову и типу контента"""
    query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': keyword,
                            'fields': ['title', 'content']
                        }
                    }
                ]
            }
        }
    }
    
    if content_type:
        query['query']['bool']['must'].append({
            'term': {'content_type': content_type}
        })

    try:
        response = client.search(
            body=query,
            index=INDEX_NAME
        )
        
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            results.append({
                'title': source['title'],
                'snippet': source['content'][:50] + '...',
                'content_type': source['content_type']
            })
        
        return results
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    content_type = request.args.get('content_type', None)
    
    if not keyword:
        return jsonify([])
    
    results = search_documents(keyword, content_type)
    return jsonify(results)

@app.route('/init', methods=['POST'])
def initialize():
    success = create_index()
    if success:
        generate_sample_data()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
