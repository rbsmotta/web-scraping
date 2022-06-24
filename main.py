# imports
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

def access_weather():
    """
    Creating a function where:
        - Connect to the page;
        - Get and merge the data;
        - Create a dataframe with the information.
    """
    # url of page
    url = 'https://tempo.cptec.inpe.br/rj/niteroi'

    # HTTP requisition with get method
    response = get(url)

    # object creation and response status
    soup = BeautifulSoup(response.text, 'html.parser')

    if(response.status_code==200):
        print('Query successful!\n')
    else:
        print('Query failed.\n')

    # creating empty lists to append de data
    complete_date, week_day, minimun_teperature, maximum_temperature, rain_probability, uv_indices = [], [], [], [], [] ,[]

    # searching for all containers DIV that contains the class 'proximos dias'
    next_days = soup.find_all("div", class_="proximos-dias")

    for dia in next_days:
        dates = dia.find("small")
        day_of_week = dia.find("span", class_="font-weight-bold text-uppercase").text
        min_temp = dia.select_one('span[alt="Temperatura Mínima"]')
        max_temp = dia.select_one('span[alt="Temperatura Máxima"]')
        rain_prob_uv = dia.find("div", class_= "d-flex justify-content-around mt-1")\
            .find_all("div",class_="d-flex justify-content-center")

        # appending in the lists
        complete_date.append(dates.text)
        week_day.append(str(day_of_week))
        minimun_teperature.append(int(min_temp.text.replace("°","")))
        maximum_temperature.append(int(max_temp.text.replace("°","")))
        uv_indices.append(int(rain_prob_uv[0].span.text))
        rain_probability.append(int(rain_prob_uv[1].span.text.replace("%",""))) 
    
    # creating dataframe
    df = pd.DataFrame({
    'date': complete_date,
    'day_of_week': week_day,
    'min_temp': minimun_teperature,
    'max_temp': maximum_temperature,
    'rain_prob(%)': rain_probability,
    'uv_indices': uv_indices
    })

    print(df)

if __name__ == '__main__':
    access_weather()