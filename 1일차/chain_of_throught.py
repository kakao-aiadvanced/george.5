from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "넌 수학 선생님이야. 내가 주어준 문제를 풀어줘."},
        {
            "role": "user",
            "content": "23+47"
        },
        {
            "role": "assistant",
            "content": "1단계: 숫자를 자리별로 분리하기. 23은 20+3으로 분리됩니다. 47은 40+7으로 분리됩니다. 2단계: 각 자리의 숫자를 더하기. 십의 자리: 20+40=60. 일의 자리: 3+7=10. 3단계: 두 값을 더하기. 60+10=70. 정답은 70입니다."
        },
        {
            "role": "user",
            "content": "345 + 678 - 123"
        },
    ]
)

print(completion.choices[0].message)
