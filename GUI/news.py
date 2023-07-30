import requests
import nltk
import string

def find_category(input_string):
    categories = {
    "sport": ["sports", "sport", "fitness", "exercise", "games", "athletics", "soccer", "basketball", "running"],
    "space": ["astronomy", "cosmology", "space exploration", "NASA", "planets", "galaxies", "rocket"],
    "technology": ["computers", "software", "hardware", "programming", "AI", "innovation", "gadgets"],
    "food": ["cooking", "recipes", "cuisine", "restaurants", "nutrition", "baking", "chefs"],
    "travel": ["adventure", "tourism", "vacation", "destinations", "exploration", "backpacking"],
    "history": ["historical events", "ancient civilizations", "world wars", "monarchs", "archaeology"],
    "science": ["biology", "chemistry", "physics", "scientific discoveries", "research"],
    "music": ["musicians", "instruments", "concerts", "genres", "songwriting", "bands"],
    "art": ["painting", "sculpture", "drawing", "photography", "artists", "exhibitions"],
    "health": ["wellness", "meditation", "yoga", "nutrition", "mental health", "fitness"],
    "nature": ["wildlife", "conservation", "ecosystems", "environment", "natural wonders"],
    "finance": ["investing", "stocks", "economics", "business", "budgeting", "financial planning"],
    "literature": ["books", "authors", "novels", "poetry", "classics", "literary awards"],
    "fashion": ["clothing", "designers", "trends", "style", "fashion shows", "accessories"],
    "education": ["learning", "teaching", "schools", "universities", "online courses", "education technology"],
    "movies": ["film", "directors", "actors", "genres", "blockbusters", "film festivals"],
    "science fiction": ["aliens", "time travel", "robots", "alternate realities", "extraterrestrial life"],
    "politics": ["government", "elections", "policies", "political leaders", "international relations"],
    "comedy": ["stand-up", "sketches", "comedy shows", "funny videos", "satire"],
    "environment": ["climate change", "sustainability", "renewable energy", "pollution", "conservation"],
    "animals": ["wild animals", "pets", "endangered species", "zoology", "animal behavior"],
    "technology trends": ["blockchain", "augmented reality", "virtual reality", "Internet of Things"],
    "space exploration": ["space missions", "spacecraft", "astronauts", "Mars exploration", "space telescopes"],
    "self-improvement": ["personal development", "motivation", "goal setting", "habits"],
    "gaming": ["video games", "board games", "e-sports", "gaming industry"],
    "architecture": ["architectural design", "urban planning", "landscaping", "historical buildings"],
    "healthcare": ["medical advancements", "healthcare technology", "public health", "disease prevention"],
    "social media": ["Facebook", "Twitter", "Instagram", "social networking", "online communities"],
    "green living": ["sustainable living", "eco-friendly practices", "zero waste", "organic gardening"],
    "education technology": ["e-learning", "EdTech", "online learning platforms", "digital classrooms"],
    "cryptocurrency": ["Bitcoin", "Ethereum", "decentralized finance", "crypto mining"],
    "space science": ["cosmic phenomena", "black holes", "dark matter", "astronomical research"],
    "diversity and inclusion": ["equality", "equity", "inclusivity", "cultural diversity"],
    "business startups": ["entrepreneurship", "startup culture", "venture capital", "innovation"],
    "mindfulness": ["meditation", "mindful living", "stress reduction", "mind-body practices"],
    "parenting": ["raising children", "child development", "parenting tips", "family dynamics"],
    "green energy": ["solar power", "wind energy", "hydroelectric power", "clean energy solutions"],
    "AI and Machine Learning": ["artificial intelligence", "machine learning", "deep learning", "neural networks"],
    "cryptocurrencies": ["altcoins", "cryptocurrency trading", "NFTs", "blockchain technology"],
    "productivity": ["time management", "organization", "efficiency", "task management"],
    "mental health": ["anxiety", "depression", "stress management", "therapy", "mental wellness"],
    "cooking and recipes": ["baking", "cooking techniques", "international recipes", "culinary"],
    "virtual events": ["webinars", "virtual conferences", "online workshops", "hybrid events"],
    "cybersecurity": ["data breaches", "cyber threats", "information security", "network protection"],
    "augmented reality": ["AR applications", "AR gaming", "AR in education", "AR development"],
    "psychology": ["human behavior", "cognitive psychology", "emotional intelligence", "psychotherapy"],
    "creative writing": ["poetry", "short stories", "novel writing", "writing prompts", "fiction"],
    "green technology": ["environmentally friendly tech", "eco-friendly innovations", "green gadgets"],
    "home improvement": ["DIY projects", "interior design", "home renovations", "gardening"],
    "comics and graphic novels": ["comic book characters", "comic conventions", "comic strips"],
    "fitness trends": ["HIIT", "wearable fitness tech", "functional training", "group workouts"],
    "science communication": ["popular science", "science journalism", "science outreach"],
    "parenting tips": ["positive parenting", "child discipline", "parenting strategies"],
    "futurism": ["emerging technologies", "future predictions", "sci-fi concepts", "technology visions"],
    "social issues": ["inequality", "human rights", "social justice", "civil rights"],
    "motorsports": ["Formula 1", "NASCAR", "rally racing", "motocross"],

    }


    # Convert the input string to lowercase for case-insensitive comparison
    input_string_lower = input_string.lower()

    # Initialize variables to store the best category match and its score
    best_category = None
    best_score = 0

    # Iterate through each category and its related keywords
    for category, keywords in categories.items():
        score = sum(keyword in input_string_lower for keyword in keywords)
        if score > best_score:
            best_category = category
            best_score = score

    return best_category


def remove_unwanted_symbols(input_string):
    # Remove punctuation symbols using string.punctuation
    clean_string = input_string.translate(str.maketrans('', '', string.punctuation))
    return clean_string


def fetch_news_by_category(category, max_description_length=100):

    news = {}

    base_url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': '<API KEY>',
        'category': category,
        'pageSize': 2,  # You can adjust the number of articles you want to fetch
        'language': 'en',  # Fetch only English news
        'sortBy': 'publishedAt'  # Sort by latest published articles
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['status'] == 'ok':
            articles = data['articles']
            for article in articles:
                
                #print(f"Source: {article['source']['name']}")

                # limiting the description size to max_description_length
                description = article['description']
                truncated_description = ""
                if description is not None:
                    truncated_description = description[:max_description_length] if len(description) > max_description_length else description
                    news[remove_unwanted_symbols(article['title'])] = remove_unwanted_symbols(truncated_description)
                
                # print(f"URL: {article['url']}")
            return news

        else:
            print("Error while fetching news data.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
