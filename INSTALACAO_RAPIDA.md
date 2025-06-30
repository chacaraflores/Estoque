# 🚀 Instalação Rápida - Sistema de Estoque Chácara das Flores

## ⚡ Início Rápido (5 minutos)

### 1. Pré-requisitos
- Python 3.11+ instalado
- Acesso ao terminal/prompt de comando

### 2. Instalação Express

```bash
# 1. Navegue até a pasta do projeto
cd condominio_estoque

# 2. Instale o Django
pip install django

# 3. Execute as migrações
python manage.py migrate

# 4. Inicie o servidor
python manage.py runserver 0.0.0.0:8000
```

### 3. Acesso Imediato
- **URL**: http://localhost:8000
- **Usuário**: admin
- **Senha**: admin123

## 🎯 Primeiros Passos

### Após o Login:
1. **Dashboard** - Veja o resumo geral
2. **Materiais** - Explore os materiais cadastrados
3. **Novo Material** - Adicione seus próprios materiais
4. **Movimentar** - Teste entrada/saída de estoque
5. **Relatórios** - Gere relatórios completos

## 🔧 Configuração Básica

### Criar Novo Usuário:
```bash
python manage.py createsuperuser
```

### Acessar Admin:
- URL: http://localhost:8000/admin
- Use as credenciais do superusuário

## 📱 Funcionalidades Principais

✅ **Controle de Estoque**
- Materiais de escritório, limpeza e manutenção
- Alertas de estoque baixo
- Histórico de movimentações

✅ **Solicitações de Compra**
- Criar solicitações
- Aprovar/rejeitar pedidos
- Controle de status

✅ **Relatórios**
- Dashboard em tempo real
- Relatórios detalhados
- Exportação CSV

✅ **Interface Moderna**
- Design responsivo
- Fácil navegação
- Tema profissional

## 🆘 Problemas Comuns

### Erro de Porta Ocupada:
```bash
python manage.py runserver 0.0.0.0:8001
```

### Erro de Migração:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Esqueceu a Senha:
```bash
python manage.py changepassword admin
```

## 📞 Suporte Rápido

**Problema**: Não consegue fazer login
**Solução**: Use admin/admin123 ou crie novo usuário

**Problema**: Página não carrega
**Solução**: Verifique se o servidor está rodando

**Problema**: Erro 500
**Solução**: Verifique logs no terminal

---

## 🎉 Pronto para Usar!

O sistema está configurado com dados de exemplo e pronto para uso imediato. Explore todas as funcionalidades e personalize conforme suas necessidades.

**Dica**: Comece pelo Dashboard para ter uma visão geral do sistema!

