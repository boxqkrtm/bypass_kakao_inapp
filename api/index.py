from flask import Flask, request
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def escape_kakao_help():
    return f'''리다이렉트할 주소를 입력해주세요'''

@app.route('/<path:url>', methods=['GET', 'POST'])
def escape_kakao(url):
    # URL 파싱
    parsed_url = urlparse(url)
    
    # 스키마(http:// 또는 https://)가 없는 경우 https:// 추가
    if not parsed_url.scheme:
        redirect_url = f'https://{url}'
    else:
        redirect_url = url

    return f'''
    페이지 이동 중입니다.
    <script>
    const userAgent = navigator.userAgent.toLowerCase();
    let finalUrl = '{redirect_url}';
    let needClose = true;
    if (/android/.test(userAgent)) {{
        location.href = 'kakaotalk://web/openExternal?url=' + encodeURIComponent(finalUrl);
        needClose = false;
    }} else if (/ipad|iphone|ipod/.test(userAgent)) {{
        location.href = 'kakaotalk://web/openExternal?url=' + encodeURIComponent(finalUrl);
    }} else {{
        needClose = false;
        location.href = finalUrl;
    }}
    if(needClose){{
        document.addEventListener("visibilitychange", () => {{
        if(document.visibilityState == "visible") {{
            location.href = /ipad|iphone|ipod/.test(userAgent)
                ? 'kakaoweb://closeBrowser'
                : 'kakaotalk://inappbrowser/close';
        }}
        }});
    }}
    </script>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
