import requests
from celery_app.urls import headers_vk, url_vk


def request_vk(username: str):
    response = requests.get(
        url=url_vk.format(username),
        headers=headers_vk
    ).json()
    response_vk = response.get("response")
    if not response_vk:
        raise ValueError("Учетки не существует")
    likes = response_vk.get("items")[0].get("likes").get("count")
    profile = response_vk.get("profiles")
    if len(profile) == 1:
        followers = profile[0].get("followers_count")
    else:
        followers = profile[1].get("followers_count")
    return followers, likes
