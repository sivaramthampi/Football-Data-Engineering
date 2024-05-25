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
    table = soup.find_all("table",{"class":"wikitable sortable sticky-header jquery-tablesorter"})[0]
    table_rows = table.find_all('tr')
    return table_rows

def extract_wikipedia_data(url):
    url = url
    html = get_wikipedia_page(url)
    rows = get_wikipedia_data(html)
    data = []
    for i in range(1, len(rows)):
        tds = rows[i].find_all('td')
        values = {
            'rank':i,
            'stadium':tds[0].text,
            'capacity':tds[1].text,
            'region':tds[2].text,
            'country':tds[3].text,
            'city':tds[4].text,
            'images':tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "No Image",
            'home_team':tds[6].text
        }
        data.append(values)
    print(data)
    return data