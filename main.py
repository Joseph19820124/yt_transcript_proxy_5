import functions_framework
import requests
import os
from flask import jsonify, abort

@functions_framework.http
def transcript_proxy(request):
    """
    HTTP Cloud Function.
    Expects POST with JSON: { "url": "YouTube影片URL" }
    """
    if request.method != "POST":
        abort(405)

    try:
        data = request.get_json()
        yt_url = data.get("url")
        if not yt_url:
            return jsonify({"error": "Missing URL"}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "detail": str(e)}), 400

    # 從環境變數取得 RapidAPI 金鑰
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return jsonify({"error": "Missing RAPIDAPI_KEY env"}), 500

    params = {
        "url": yt_url,
        "flat_text": "true",
        "lang": "en"
    }
    api_url = "https://youtube-transcript3.p.rapidapi.com/api/transcript-with-url"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "youtube-transcript3.p.rapidapi.com"
    }
    try:
        r = requests.get(api_url, headers=headers, params=params)
        return (r.text, r.status_code, {"Content-Type": r.headers.get("Content-Type", "application/json")})
    except Exception as e:
        return jsonify({"error": "Proxy fetch failed", "detail": str(e)}), 500
