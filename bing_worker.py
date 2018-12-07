def images_links(query):
    config = {}
    with open('.config') as config_file:
        for line in config_file.readlines():
            eq = line.split('=')
            config[eq[0]] = eq[1].strip()
    subscription_key = config['subscription_key']
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    search_term = query

    import requests

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:30]]

    return thumbnail_urls

if __name__ == "__main__":
    print(images_links("панда"))
