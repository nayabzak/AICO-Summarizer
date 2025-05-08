# test_summary.py
from src.agent_setup import summarize_webpage

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Hassan_Nawaz_(cricketer)'
    summary = summarize_webpage(url)
    print('Summary:')
    print(summary)