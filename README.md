# 카카오톡 리다이렉트 서비스

카카오톡 인앱 브라우저에서 외부 링크로 안전하게 리다이렉트하기 위한 Flask 기반 웹 서비스입니다.

## 주요 기능

- 카카오톡 인앱 브라우저에서 외부 링크 열기
- iOS/Android 디바이스 자동 감지
- URL 프래그먼트(#) 처리 지원
- 
## 설치 방법

1. Python 3.6 이상 설치
2. 필요한 패키지 설치:
```bash
pip install flask
```

## 실행 방법

```bash
python app.py
```
서버가 `http://0.0.0.0:80`에서 실행됩니다.

## 사용 방법

1. 기본 URL에 리다이렉트하고 싶은 주소를 추가하여 접속
   - 예시: `http://your-domain.com/https://target-site.com`

2. URL에 프래그먼트(#)가 포함된 경우 자동으로 처리됩니다.

## 주의사항

- 80번 포트를 사용하므로 관리자 권한이 필요할 수 있습니다.
- 프로덕션 환경에서는 `debug=True` 설정을 제거하세요.
- HTTPS 사용을 권장합니다.

## 라이선스

MIT License
