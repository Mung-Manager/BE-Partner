# 멍매니저 사장님 BE
## 간단한 소개 글
- 강아지 유치원 사장님의 `일정/등원 관리`의 리소스를 효율적으로 줄여주는 서비스

<details>
  <summary> 서비스 소개서</summary>
  
![image](https://github.com/mung-manager/partner-be/assets/104830931/b231115e-1b0d-4099-ba1d-55689c828ebc)
![image](https://github.com/mung-manager/partner-be/assets/104830931/5bcc53d4-8058-40f8-a767-4471d05aa2c5)
![image](https://github.com/mung-manager/partner-be/assets/104830931/2a6435fe-6fac-415e-9632-8e4a219782e4)
![image](https://github.com/mung-manager/partner-be/assets/104830931/d4d174a4-3ae7-4ab2-ae2d-64dd824800ee)
![image](https://github.com/mung-manager/partner-be/assets/104830931/7ef168ee-c880-48b4-950c-a6511302a2d9)
![image](https://github.com/mung-manager/partner-be/assets/104830931/f6865dcf-7056-4de4-88fb-47d04cd9bfa6)
![image](https://github.com/mung-manager/partner-be/assets/104830931/ce560a58-c90d-4842-87c8-46339381ad3d)
![image](https://github.com/mung-manager/partner-be/assets/104830931/4c4908d8-6b4a-45ad-b2de-813296e03f2d)

</details>

## 기술 스택
- Language: Python 3.11
- Backend: Django 5.0, Django Rest Framework, Celery, Celery-beats 
- DB: Postgresql16.0, PostGis
- Infra: AWS, Docker, Docker Compose, Nginx, Redis
- Management: Git, Github, Github Actions
- Swagger: drf-spectacular
- Monitoring: Sentry
- Code Style: black, isort, flake8, autoflake, bandit, mypy
- Communication: Slack, Notion
- Test: pytest, factory-boy, faker



## 컨벤션 규칙
[그라운드 룰](https://hiallen.notion.site/Ground-Rule-c2a808cbf2fb479eaa56ded4fe617e7b?pvs=4)

[Git 브랜치 컨벤션](https://hiallen.notion.site/Git-Branch-6314f735522e441d830f774553b4a401?pvs=4)

[Git 커밋 컨벤션](https://hiallen.notion.site/Commit-Rule-001cdacdd0464530a02888bf8ca322bd?pvs=4)

[PR 및 이슈 컨벤션](https://hiallen.notion.site/PR-Issue-Bug-Convention-7f02a8337ea0441689f63be2d4c1ce71?pvs=4)

[주석 컨벤션](https://hiallen.notion.site/Comment-Convention-5dd546ebadaa4dacae4a2f2510574bfc?pvs=4)

[테스트 작성 컨벤션](https://hiallen.notion.site/5c7d9fbede43426fb466ea30151bc194?pvs=4)

- 프로젝트는 Layered 아키텍처로 진행하고 있습니다. 대략적인 구조 및 가이드는 아래 문서를 참조합니다.
  - [Django Style Guide](https://github.com/HackSoftware/Django-Styleguide)
  - [Django Style Guide Example](https://github.com/HackSoftware/Django-Styleguide-Example)
 
- 그외 팀 내에서 정한 규칙
  - [Selector / Service 네이밍 규칙](https://hiallen.notion.site/Selector-Service-632ba6c6a67d49e0ac7520484d74b343?pvs=4)
 
- 그외 읽어보면 좋을 글
  - [Django Layered 아키텍처](https://medium.com/athenaslab/django%EC%99%80-layered-architecture-%EC%82%AC%EC%9D%B4%EC%97%90%EC%84%9C-%ED%83%80%ED%98%91%EC%A0%90-%EC%B0%BE%EA%B8%B0-70769c13ef9d)

## 실행방법
- env는 팀원에게 부탁해주십시오!

### docker 환경

[docker 설치](https://docs.docker.com/engine/install/)
[docker compose 설치](https://docs.docker.com/compose/install/)

```bash
# 프로젝트 경로로 이동
docker login # 로그인을 진행

# docker compose 실행
docker compose up -d --build

# docker 재실행
docker compose restart <컨테이너 이름>
```

### 로컬 환경
```bash
# python 가상환경
python -m venv venv

# 가상환경 실행
source ./venv/bin/activate # mac
source ./venv/scripts/activate # window

# poetry 설치
pip install poetry

# 패키지 설치
poetry install

# 서버 실행
make start

# 데이터베이스 마이그레이트
make migrate
```
- 실행 전에 PostGIS를 사용하기에 [GEOS, GDAL](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/geolibs/)를 설치해야합니다.
- PostgreSQL은 [PostGIS](https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.PostGIS.html)를 설치해야합니다.

## 모듈 사용
- 저희는 코드 스타일을 맞추기 위해 코드 포맷팅을 사용하고 있습니다.

```bash
# 커밋 직전에 코드 스타일을 맞추기 위한 도구입니다.
pre-commit install

git add .
git commit

check yaml...............................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
check for added large files..............................................Passed
check for merge conflicts................................................Passed
flake8...................................................................Passed
black....................................................................Passed
autoflake................................................................Passed
isort....................................................................Passed
bandit...................................................................Passed
mypy.....................................................................Passed
```

- mypy를 개별 사용하고 싶다면 아래 명령어를 입력하십시오
```bash
make mypy
```

## [ERD](https://www.erdcloud.com/d/KPTiwH5kMJdJbw3ne)
![image](https://github.com/mung-manager/partner-be/assets/104830931/55b78151-ccb7-416e-9eaa-bdc8789ae1cc)

## 아키텍처

### 어플리케이션 아키텍처
- 작성 중
### 인프라 아키텍처
- 작성 중
