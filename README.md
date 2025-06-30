# Sistema de Controle de Estoque - Chácara das Flores

## Descrição

Sistema completo desenvolvido em Django para gerenciamento de estoque de materiais do condomínio Chácara das Flores. O sistema permite controlar materiais de escritório, limpeza e manutenção com sistema de autenticação por senha.

## Funcionalidades

### 🔐 Autenticação e Segurança
- Sistema de login com usuário e senha
- Controle de acesso restrito a funcionários autorizados
- Proteção CSRF para segurança das transações

### 📦 Gestão de Materiais
- Cadastro completo de materiais com categorização
- Controle de quantidade atual e mínima
- Alertas automáticos para estoque baixo
- Informações de fornecedor e localização
- Controle de preços e valor total do estoque

### 📊 Controle de Estoque
- Movimentações de entrada, saída e ajuste
- Histórico completo de todas as movimentações
- Rastreabilidade por usuário e data
- Motivos e observações para cada movimentação

### 🛒 Solicitações de Compra
- Sistema de solicitação de materiais
- Fluxo de aprovação/rejeição
- Justificativas e observações
- Controle de status das solicitações

### 📈 Relatórios e Dashboard
- Dashboard com estatísticas em tempo real
- Relatórios completos de estoque
- Filtros por categoria e status
- Exportação para CSV
- Função de impressão

### 🎨 Interface Moderna
- Design responsivo e profissional
- Tema verde inspirado no nome "Chácara das Flores"
- Interface intuitiva e fácil de usar
- Navegação clara com sidebar e menu superior

## Tecnologias Utilizadas

- **Backend**: Django 5.2.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)
- **Framework CSS**: Bootstrap 5.3
- **Ícones**: Bootstrap Icons
- **Python**: 3.11

## Estrutura do Projeto

```
condominio_estoque/
├── condominio_estoque/          # Configurações do projeto
│   ├── settings.py              # Configurações principais
│   ├── urls.py                  # URLs principais
│   └── wsgi.py                  # Configuração WSGI
├── materiais/                   # App principal
│   ├── models.py                # Modelos de dados
│   ├── views.py                 # Views/Controllers
│   ├── forms.py                 # Formulários
│   ├── admin.py                 # Interface administrativa
│   ├── urls.py                  # URLs do app
│   └── templates/materiais/     # Templates HTML
├── db.sqlite3                   # Banco de dados
├── manage.py                    # Script de gerenciamento Django
└── README.md                    # Esta documentação
```

## Modelos de Dados

### Categoria
- Nome, tipo (escritório/limpeza/manutenção), descrição

### Material
- Nome, categoria, descrição, unidade de medida
- Quantidade atual/mínima, preço unitário
- Fornecedor, localização, status ativo

### MovimentacaoEstoque
- Material, tipo (entrada/saída/ajuste), quantidade
- Motivo, observações, usuário, data

### SolicitacaoCompra
- Material, quantidade solicitada, justificativa
- Status, solicitante, aprovador, datas

### Fornecedor
- Nome, CNPJ, contato, endereço

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou copie o projeto**
```bash
# Se usando Git
git clone <repositorio>
cd condominio_estoque

# Ou extraia o arquivo ZIP fornecido
```

2. **Instale o Django**
```bash
pip install django
```

3. **Execute as migrações**
```bash
python manage.py migrate
```

4. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

5. **Inicie o servidor**
```bash
python manage.py runserver 0.0.0.0:8000
```

6. **Acesse o sistema**
- URL: http://localhost:8000
- Admin: http://localhost:8000/admin

## Dados de Exemplo

O sistema já vem com dados de exemplo pré-carregados:

### Usuário Administrador
- **Usuário**: admin
- **Senha**: admin123

### Categorias
- Escritório - Papelaria
- Limpeza - Produtos de Limpeza  
- Manutenção - Ferramentas

### Materiais de Exemplo
- **Escritório**: Papel A4, Caneta Azul, Grampeador
- **Limpeza**: Detergente, Papel Higiênico
- **Manutenção**: Chave de Fenda, Parafuso Phillips

## Como Usar

### 1. Login
- Acesse a página inicial
- Digite usuário e senha
- Clique em "Entrar"

### 2. Dashboard
- Visualize estatísticas gerais
- Veja materiais com estoque baixo
- Acompanhe últimas movimentações

### 3. Gerenciar Materiais
- **Listar**: Menu "Materiais"
- **Adicionar**: Botão "Novo Material"
- **Editar**: Ícone de lápis na lista
- **Ver Detalhes**: Ícone de olho na lista

### 4. Movimentar Estoque
- Acesse detalhes do material
- Clique em "Movimentar Estoque"
- Escolha tipo: Entrada/Saída/Ajuste
- Informe quantidade e motivo

### 5. Solicitações de Compra
- Menu "Solicitações" → "Nova Solicitação"
- Selecione material e quantidade
- Justifique a necessidade
- Aguarde aprovação

### 6. Relatórios
- Menu "Relatórios"
- Filtre por categoria se necessário
- Use "Imprimir" ou "Exportar CSV"

## Configurações Importantes

### Segurança
- Altere a SECRET_KEY em produção
- Configure ALLOWED_HOSTS adequadamente
- Use HTTPS em produção
- Configure backup do banco de dados

### Banco de Dados
- Para produção, considere PostgreSQL ou MySQL
- Configure backup automático
- Monitore espaço em disco

### Performance
- Configure cache se necessário
- Otimize consultas para grandes volumes
- Configure servidor web (nginx/Apache)

## Manutenção

### Backup
```bash
# Backup do banco de dados
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

### Logs
- Monitore logs de erro do Django
- Configure logging em produção
- Acompanhe uso de recursos

### Atualizações
- Mantenha Django atualizado
- Teste em ambiente de desenvolvimento
- Faça backup antes de atualizações

## Suporte

Para dúvidas ou problemas:

1. Consulte esta documentação
2. Verifique logs de erro
3. Teste em ambiente de desenvolvimento
4. Entre em contato com o desenvolvedor

## Licença

Sistema desenvolvido especificamente para o Condomínio Chácara das Flores.

---

**Desenvolvido para o Condomínio Chácara das Flores**

*Sistema de Controle de Estoque - Versão 1.0*

*Tempunus Mind Computer*

