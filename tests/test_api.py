from fastapi.testclient import TestClient

from app.main import app, provider


client = TestClient(app)


def test_health_mode_mock():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["mode"] == "mock"


def test_detection_francais():
    response = client.post(
        "/detect-language",
        json={"text": "Je ne peux plus acceder a mon compte."},
    )

    assert response.status_code == 200
    assert response.json()["language"] == "fr"


def test_detection_arabe():
    response = client.post(
        "/detect-language",
        json={"text": "لا أستطيع الدخول إلى حسابي"},
    )

    assert response.status_code == 200
    assert response.json()["language"] == "ar"


def test_texte_trop_court_rejete():
    response = client.post(
        "/detect-language",
        json={"text": "ab"},
    )

    assert response.status_code == 422


def test_champ_text_absent_rejete():
    response = client.post(
        "/detect-language",
        json={},
    )

    assert response.status_code == 422


def test_fournisseur_indisponible(monkeypatch):
    def simulated_failure(text):
        raise RuntimeError("Simulated provider failure")

    monkeypatch.setattr(
        provider,
        "detect_language",
        simulated_failure,
    )

    response = client.post(
        "/detect-language",
        json={"text": "This is valid text."},
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Service d'inference indisponible"
    }