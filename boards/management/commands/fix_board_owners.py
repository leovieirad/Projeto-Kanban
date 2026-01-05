from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from boards.models import Board


class Command(BaseCommand):
    help = 'Atribui um owner padrão para quadros sem proprietário'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nome de usuário que será definido como owner dos quadros sem proprietário',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        boards_without_owner = Board.objects.filter(owner__isnull=True)
        count = boards_without_owner.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('Não há quadros sem proprietário.'))
            return
        
        if not username:
            self.stdout.write(self.style.WARNING(f'Encontrados {count} quadros sem proprietário:'))
            for board in boards_without_owner:
                self.stdout.write(f'  - {board.id}: {board.title}')
            self.stdout.write(self.style.WARNING('\nExecute novamente com --username=<nome_de_usuario> para atribuir um proprietário.'))
            return
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário "{username}" não encontrado.'))
            return
        
        boards_without_owner.update(owner=user)
        self.stdout.write(self.style.SUCCESS(f'✅ {count} quadros atualizados com owner: {user.username}'))
