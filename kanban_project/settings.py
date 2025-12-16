"""
Configurações Django para o projeto kanban_project.

Gerado por 'django-admin startproject' usando Django 5.2.4.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/5.2/topics/settings/

Para a lista completa de configurações e seus valores, veja
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Caminhos do projeto (ex.: BASE_DIR / 'subdir').
BASE_DIR = Path(__file__).resolve().parent.parent


# Configurações rápidas para desenvolvimento - não adequadas para produção
# Veja https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha a chave secreta usada em produção em sigilo!
SECRET_KEY = 'django-insecure-uo0e9g3^gcefcfm5)qfx4ep$6-(14i@w8fucwzk!n4e*g-dmeq'

# AVISO DE SEGURANÇA: não execute com DEBUG ativado em produção!
DEBUG = True

ALLOWED_HOSTS = [
    ".app.github.dev",
    "localhost",
    "127.0.0.1"
]


# Definição das aplicações

CSRF_TRUSTED_ORIGINS = [
    "https://automatic-system-v6q796jqvvqh6976-8000.app.github.dev"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'boards.apps.BoardsConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kanban_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kanban_project.wsgi.application'


# Banco de dados
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validação de senhas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalização
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Arquivos estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Tipo de campo padrão para chave primária
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Redirecionamento de autenticação
LOGIN_URL = 'boards:login'
LOGIN_REDIRECT_URL = 'boards:list'
LOGOUT_REDIRECT_URL = 'boards:login'