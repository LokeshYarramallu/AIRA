import http.client
import json

def scrap_profile(profile_url):
    print("Url received :", profile_url)

    conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "a23c7ac966msh40d4cda7ff1c48ep1045a7jsnbe95efbb4f7f",
        'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
    }
    conn.request("GET", f"/get-profile-data-by-url?url={profile_url}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
