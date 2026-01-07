# 📌 Projeto Kanban

## 🌐 Sobre o Projeto (About the Project)  
Esse é um projeto de **Quadro Kanban Online** desenvolvido utilizando: **Python**, **Django**, **HTML**, **CSS** e **Bootstrap**. O objetivo é permitir que usuários organizem tarefas em colunas (como "A Fazer", "Em Andamento" e "Concluído") de forma prática e visual.

> This is an **Online Kanban Board** project built using: **Python**, **Django**, **HTML**, **CSS**, and **Bootstrap**. The goal is to allow users to organize tasks into columns (such as "To Do", "In Progress", and "Done") in a practical and visual way.

---

## 📋 Funcionalidades (Features)

- **Cadastro e Login de Usuário**  
  Sistema de autenticação para acesso às tarefas pessoais.

- **Criação de Quadros e Colunas**  
  Possibilidade de criar múltiplos quadros com colunas personalizadas.

- **Gerenciamento de Tarefas**  
  Criação, edição, movimentação e exclusão de tarefas entre colunas.

- **Arrastar e Soltar (Drag and Drop)**  
  Interface intuitiva para reorganizar tarefas com facilidade.

- **Visual Responsivo**  
  Funciona bem em desktop e dispositivos móveis.

> **User Registration and Login**  
  Authentication system for accessing personal tasks.

> **Board and Column Creation**  
  Ability to create multiple boards with custom columns.

> **Task Management**  
  Create, edit, move, and delete tasks across columns.

> **Drag and Drop Interface**  
  Intuitive interface for easily reorganizing tasks.

> **Responsive Layout**  
  Works well on desktop and mobile devices.

---

## 🛠️ Tecnologias Utilizadas (Technologies Used)

- **Python**: lógica principal do projeto.
- **Django**: gerenciamento de usuários, tarefas e quadros.
- **HTML & CSS**: estrutura e visual da aplicação.
- **Bootstrap**: estilização rápida e responsiva.
- **JavaScript**: funcionalidades de interação como drag-and-drop.

> **Python**: main logic of the project.  
> **Django**: managing users, tasks, and boards.  
> **HTML & CSS**: structure and visual layout.  
> **Bootstrap**: quick and responsive styling.  
> **JavaScript**: interactive features like drag-and-drop.

---

## 🎨 Design do Projeto (Project Design)

A interface do sistema Kanban é inspirada em ferramentas modernas de produtividade. Cada quadro pode ser personalizado conforme o estilo de trabalho do usuário, permitindo controle visual claro das tarefas.

> The Kanban system interface is inspired by modern productivity tools. Each board can be customized to fit the user’s workflow, allowing a clear visual control of tasks.
---

## 📥 Como Baixar e Executar o Projeto (How to Download and Run the Project)

### Português

#### Pré-requisitos
- **Python 3.8+** instalado no seu computador
- **Git** instalado (para clonar o repositório)
- **pip** (gerenciador de pacotes Python)

#### Passos para executar:

1. **Clone o repositório:**
   ```bash
   git clone <https://github.com/leovieirad/Projeto-Kanban.git>
   cd Projeto-Kanban
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor:**
   ```bash
   python manage.py runserver
   ```

8. **Acesse a aplicação:**
   Abra seu navegador e vá para `http://127.0.0.1:8000/`

---

### English

#### Prerequisites
- **Python 3.8+** installed on your computer
- **Git** installed (to clone the repository)
- **pip** (Python package manager)

#### Steps to run:

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/leovieirad/Projeto-Kanban.git>
   cd Projeto-Kanban
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`
