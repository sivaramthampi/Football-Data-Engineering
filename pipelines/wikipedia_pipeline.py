import json
def get_wikipedia_page(url):
    import requests
    print("Getting wikipedia page.......",url)
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"An error occured: {e}")

def get_wikipedia_data(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("table",{"class":"wikitable"})[1]
    table_rows = table.find_all('tr')
    return table_rows

def clean_text(text):
    text = str(text).strip()
    if text.find(' ♦'):
        text = text.replace(' ♦','')
    if text.find('\n'):
        text = text.replace('\n','')
    if text.find('[') != -1:
        text = text.split('[')[0]
    return text.replace('\n','')

def extract_wikipedia_data(**kwargs):
    import pandas as pd
    url = kwargs['url']
    html = get_wikipedia_page(url)
    rows = get_wikipedia_data(html)
    data = []
    for i in range(1, len(rows)):
        tds = rows[i].find_all('td')
        print(tds)
        values = {
            'rank':i,
            'stadium':clean_text(tds[0].text),
            'capacity':clean_text(tds[1].text).replace(',',''),
            'region':clean_text(tds[2].text),
            'country':clean_text(tds[3].text.strip().split('>')[-1]),
            'city':tds[4].text,
            'images':'https://' + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "No Image",
            'home_team':clean_text(tds[6].text)
        }
        data.append(values)
    df = pd.DataFrame(data)
    df.to_csv("data/football_data.csv",index=False)
    json_rows = json.dumps(data)
    kwargs['ti'].xcom_push(key='rows',value=json_rows)
    return "OK"