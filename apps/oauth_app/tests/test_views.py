from django import urls
from django.contrib.auth import get_user_model
import pytest

@pytest.mark.parametrize('param', [
    ('home'),
])
def test_render_views(client,param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200