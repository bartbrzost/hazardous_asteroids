import requests
url = 'http://localhost:5000/results'
r = requests.post(url, json= {'est_diameter_min':0.27,
                              'est_diameter_max': 0.59,
                              'relative_velocity': 73588.73,
                              'miss_distance': 61438126.52,
                              'absolute_magnitude': 20.00})
print(r.json())
