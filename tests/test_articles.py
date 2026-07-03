from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
# testing the public GET /articels route
def test_get_articles():
    response = client.get ("/articles")
    assert response.status_code == 200
    # adding an assertion to check if the response is a list
    assert isinstance (response.json(), list)

# test to create an article without a token : expected failure
def test_create_article_unauthorized():
    response = client.post("/articles",json={"title":"Test", "content":"Test Content"})
    assert response.status_code == 401

#test to create an article with a token : expected success
def test_create_article_authorized():
    #passing the header exactly as the api is expecting it
    headers = {"admin_token":"secret_token"}
    payload = {"title":"my test post", "content":"this is a test post content"}
    response = client.post("/articles",json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()['title'] == "my test post"
    