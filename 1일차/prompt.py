from openai import OpenAI
client = OpenAI()

# 1. 영어를 한국어로 번역하는 5-shot prompt 를 작성하고 "dog"를 번역해보세요.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Translate from English to Korean."},
        {
            "role": "user",
            "content": "Banana"
        },
        {
            "role": "assistant",
            "content": "바나나"
        },
        {
            "role": "user",
            "content": "Cat"
        },
        {
            "role": "assistant",
            "content": "고양이"
        },
        {
            "role": "user",
            "content": "Monkey"
        },
        {
            "role": "assistant",
            "content": "원숭이"
        },
        {
            "role": "user",
            "content": "Apple"
        },
        {
            "role": "assistant",
            "content": "사과"
        },
        {
            "role": "user",
            "content": "Bird"
        },
        {
            "role": "assistant",
            "content": "새"
        },
        {
            "role": "user",
            "content": "Dog"
        }
    ]
)

print(completion.choices[0].message)

# 2. 영화 리뷰에 대한 sentiment (positive or negative) 를 결정하는 5-shot prompt 를 작성하고 "The storyline was dull and uninspiring." 에 대한 결과를 확인해보세요.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 영화 리뷰에 대한 감정을 분석하는 봇입니다. 사용자의 리뷰를 확인하고 [Positive] 혹은 [Negative] 로 분류하세요."},
        {"role": "user", "content": "1편에 대한 처절한 자기반성, 혹은 1편 속에 숨겨두었던 의미의 재조명."},
        {"role": "assistant", "content": "[Positive]"},
        {"role": "user", "content": "뮤지컬 때문에 집중 흐트러지고, 짜증만 남."},
        {"role": "assistant", "content": "[Negative]"},
        {"role": "user", "content": "1편을 뛰어넘지 못하고 그림자에 잡아먹힌 실망감이 큰 영화"},
        {"role": "assistant", "content": "[Negative]"},
        {"role": "user", "content": "이 영화에 혹평을 쏟는 이 중 조커를 원했고 이와 다름의 대하여 실망한 이들은 영화를 평가할 자격이 없다."},
        {"role": "assistant", "content": "[Positive]"},
        {"role": "user", "content": "이 영화를 보는 사람의 성향마다 다르게 받아들인다는 점이 재밌어서 별 한개 주려다가 두개 드립니다"},
        {"role": "assistant", "content": "[Negative]"},
        {"role": "user", "content": "이 영화에 가장 큰 혹평인 뮤지컬과 노래는 오히려 감독이 적절히 선택한 것 아닌가?"},
    ]
)

print(completion.choices[0].message)

# 3. 자연어를 SQL 쿼리로 바꿔주는 few-shot prompt 를 작성해보세요.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Please write appropriate SQL according to my request."},
        {"role": "user", "content": "Check all employees with salary over 50000"},
        {"role": "assistant", "content": "SELECT * FROM employees WHERE salary > 50000"},
        {"role": "user", "content": "Retrieve the names of students who have a math score greater than 90."},
        {"role": "assistant", "content": "SELECT * FROM products WHERE stock = 0"},
        {"role": "user", "content": "Retrieve the names of students who have a math score greater than 90."},
        {"role": "assistant", "content": "SELECT name FROM students WHERE math_score > 90"},
        {"role": "user", "content": "Retrieve all details from the `orders` table for orders placed within the last 30 days, including today."},
        {"role": "assistant", "content": "SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"},
        {"role": "user", "content": "Retrieve the list of cities from the `customers` table and the count of customers in each city, grouping the results by city."},
        {"role": "assistant", "content": "SELECT city, COUNT(*) FROM customers GROUP BY city"},
        {"role": "user", "content": "Find the average salary of employees in the marketing department."},
    ]
)

print(completion.choices[0].message)
