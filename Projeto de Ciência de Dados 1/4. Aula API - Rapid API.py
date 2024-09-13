import requests

url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"

querystring = {"query":"brasilia"}

headers = {
	"x-rapidapi-key": "a113dc5f7cmsh64ff3fb1d103533p197fd7jsnfd87e26b8999",
	"x-rapidapi-host": "tripadvisor16.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())