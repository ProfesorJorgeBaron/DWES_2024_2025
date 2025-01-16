import requests

class cliente_ml:
            
    def clasificar(text):
        key = "543401d0-c982-11ee-8c3f-15f879bf0d6e9c43b3af-55a3-4803-8cf8-f424b47f9366"
        url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

        response = requests.get(url, params={ "data" : text })

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()