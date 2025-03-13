from flask import Flask, request, render_template
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
    redirect_url = redirect_url.replace("'", "\\'").replace("///", "//")
    
    return render_template('template.html', redirect_url=redirect_url, redirect_url_js=redirect_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
