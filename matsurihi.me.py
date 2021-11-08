import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import itertools
import sys

def get_images_link(url):
    return_list = list()
    r = requests.get(url)
    if r.status_code == 200:
       json_data_list = r.json()
       for json_data in json_data_list:
           if (json_data["rarity"] == 4) and (json_data["extraType"] == 0 or json_data["extraType"] == 4 or json_data["extraType"] == 14):
               return_list.append(f"https://storage.matsurihi.me/mltd/card_bg/{json_data['resourceId']}_0.png")
               return_list.append(f"https://storage.matsurihi.me/mltd/card_bg/{json_data['resourceId']}_1.png")
    else:
        sys.stderr.write(f"{r.text}\n")
    return return_list    

if __name__ == "__main__":
    url_list = [ f"https://api.matsurihi.me/mltd/v1/cards?idolId={x}" for x in range(1,53) ]
    with ThreadPoolExecutor(max_workers=1) as executor:
        results = list(tqdm(executor.map(get_images_link, url_list), total=len(url_list), desc="Querying matsurihi.me API"))   
    final_results = list(itertools.chain.from_iterable(results))
    for result in final_results:
        print(result)
