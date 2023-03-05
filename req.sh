#!/bin/sh
curl -X GET 'localhost:5000/predict?prompt=cute,brain'
# curl -X POST -H "Content-Type: application/json" -d '{"text":"田中"}' 'http://localhost:5000/make_image'
