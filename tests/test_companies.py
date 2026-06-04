from conftest import make_company

def test_create_company_success(client):
    r= client.post("/companies/",json={"name":"testComp","email":"test@co.com"})
    assert r.status_code == 201
    data = r.json()
    assert data ["name"]=="testComp"
    assert "id" in data
    assert data["is_active"]==True


def test_create_company_duplicate_email(client):
    make_company(client,"testComp","test01@gmail.com")
    r=client.post("/companies/",json={"name":"testComp2","email":"test01@gmail.com"})
    assert r.status_code==409
    assert "error" in r.json()

def test_get_company_not_found(client):
    r=client.get("/companies/999999")
    assert r.status_code==404
    assert r.json()["type"]=="CompanyNotFoundError"

def test_create_company_invalid_email(client):
    r=client.post("/companies/",json={"name":"testComp","email":"not-a-mail"})
    assert r.status_code==422

def test_company_pagination_list(client):
    for i in range(5):
        make_company(client,name=f"co{i}",email=f"co{i}@gmail.com")

    r=client.get("/companies/?limit=2&skip=0")
    assert r.status_code==200
    assert len(r.json()["rows"])==2
    