from flask import Flask, request
from urllib.parse import urlparse, urlunparse, unquote

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def escape_kakao_help():
    return '''리다이렉트할 주소를 입력해주세요'''

@app.route('/<path:url>', methods=['GET', 'POST'])
def escape_kakao(url):
    # 원래 URL에 포함된 쿼리 문자열을 포함하여 request.full_path를 사용
    full_url = unquote(request.full_path[len('/'):])  # 첫 '/' 제거

    # JavaScript에서 전달된 프래그먼트 값 받기
    fragment = request.args.get('fragment', '')

    # URL 파싱
    parsed_url = urlparse(full_url)
    
    # 스키마(http:// 또는 https://)가 없는 경우 https:// 추가
    if not parsed_url.scheme:
        redirect_url = urlunparse(('https', parsed_url.netloc, parsed_url.path, '', parsed_url.query, fragment))
    else:
        redirect_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', parsed_url.query, fragment))

    # JavaScript에 전달하기 위해 URL을 이스케이프 처리
    redirect_url_js = redirect_url.replace("'", "\\'")  # 작은 따옴표를 이스케이프 처리

    print(redirect_url)  # 콘솔에 출력하여 확인
    
    return f'''
    페이지 이동 중입니다. (이동할 주소: {redirect_url})
    <script>
    const userAgent = navigator.userAgent.toLowerCase();
    let fragment = location.hash.substring(1); // # 제거한 프래그먼트 값
    let finalUrl = '{redirect_url_js}';
    
    // 프래그먼트가 존재하는 경우 서버에 추가 요청
    if (fragment) {{
        finalUrl += (finalUrl.includes('?') ? '&' : '?') + '#' + encodeURIComponent(fragment);
    }}
    {{
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
    }}
    </script>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
