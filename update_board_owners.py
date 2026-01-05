import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanban_project.settings')
django.setup()

from boards.models import Board
from django.contrib.auth.models import User

# Buscar quadros sem owner
boards_without_owner = Board.objects.filter(owner__isnull=True)
count = boards_without_owner.count()

print(f"\n🔍 Encontrados {count} quadros sem proprietário:")
for board in boards_without_owner:
    print(f"  - ID {board.id}: {board.title}")

if count > 0:
    print("\n📝 Atribuindo proprietários aos quadros...")
    
    # Tentar encontrar o primeiro usuário ativo ou criar um padrão
    first_user = User.objects.filter(is_active=True).first()
    
    if first_user:
        boards_without_owner.update(owner=first_user)
        print(f"✅ {count} quadros atualizados com owner: {first_user.username}")
    else:
        print("❌ Nenhum usuário ativo encontrado no sistema!")
else:
    print("\n✅ Todos os quadros já possuem proprietário!")
