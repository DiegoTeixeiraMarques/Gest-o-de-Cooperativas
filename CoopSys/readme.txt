Necessário instalar o Python + Pip
Executar os comandos abaixo no CMD
	pip install django
	pip install psycopg2
	pip install serial
	pip install Django==2.0.13
	pip install pyserial
	pip install django-bootstrap-form
	pip install django-jet
	pip install jet
	pip install google-api-python-client==1.4.1
	pip install django-jet2
	pip install xlwt

Tirar o default peso no método pegarpeso()
	

python manage.py migrate jet
	
	
Instruções para conexão com BD

	instala postgres e pgAdmin no servidor

	configura o arquivo pg_hba.conf
		insere o IP da rede + notação /24. Ex.: 192.168.0.0/24
		
	Cria Banco de Dados pelo pgAdmin

	Liberar porta no Firewall, criando regra para entrada e saída

	No arquivo settings do Django insere deixa o DATABASES conforme abaixo:
		
		DATABASES = {
		'default': {
			#'ENGINE': 'django.db.backends.sqlite3',
			#'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': os.environ.get('DB_NAME', 'db_teste'),
			'USER': os.environ.get('DB_USER', 'postgres'),
			'PASSWORD': os.environ.get('DB_PASS', '123'),
			'HOST': '192.168.0.5',
			'PORT': '5432',
			}
		}
		
		
		
Informações

Arquivo "boot" é um script vbs que executa o arquivo start que é .bat para ativar o ambiente virtual e executar a aplicação no localhost
O ideal é criar um atalho do boot na area de trabalho e renomea-lo para "StartService", assim, 
a aplicação começa a rodar em localhost e poderá ser usada através de uma atalho gerado pelo GoogleChrome com o link da aplicação