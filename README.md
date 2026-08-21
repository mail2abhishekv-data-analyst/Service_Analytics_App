# Service Analytics App

A Streamlit-based Service Analytics Dashboard designed for automotive service businesses to manage and analyze customers, vehicles, invoices, service history, and business activity.

## 📊 Overview

The Service Analytics App provides a centralized dashboard for viewing service-business data and managing operational information through a user-friendly Streamlit interface.

The application is connected to a SQL Server database and supports real-time data access and updates.

## 🚀 Features

- 📊 Service Analytics Dashboard
- 👥 Partners' Choice — customer and vehicle analytics
- 🚗 Entry Panel for authorized users
- 📋 Database Tables
- 👤 User Management
- 📈 KPI-based business overview
- 📊 Interactive charts and analytics
- 🔐 Role-based access control
- 🗄️ SQL Server database integration
- 🎨 Custom Ferrari-themed user interface
- 🖥️ Windows EXE application support

## 🛠️ Technology Stack

- Python
- Streamlit
- SQL Server Express
- SQLAlchemy
- PyODBC
- Plotly
- Git & GitHub
- PyInstaller

## 📁 Project Structure

```text
Service_Analytics_App/
│
├── app/
│   └── auth.py
│
├── assets/
│   ├── Ferrari_logo.avif
│   └── ferrari.webp
│
├── database/
│   └── connection.py
│
├── pages/
│   ├── dashboard.py
│   ├── entry_panel.py
│   ├── partners_choice.py
│   ├── tables.py
│   └── user_management.py
│
├── create_admin.py
├── main.py
├── run_app.py
├── VermaCarServiceAnalytics.spec
├── .gitignore
└── README.md


🗄️ Database

The application uses Microsoft SQL Server for persistent data storage.

The database connection is configured through a local config.py file.

For security and portability, the local config.py file is excluded from the GitHub repository.

▶️ Running the Application

Install the required Python packages and configure the SQL Server connection.

Then run:streamlit run main.py
The application can also be packaged as a Windows executable using PyInstaller.

🔐 Security

Local configuration files containing environment-specific database settings are excluded from version control.

The repository does not contain database passwords, API keys, or other sensitive credentials.

💻 Application

The project has been packaged and tested as a Windows executable (.exe) for easier deployment on compatible Windows systems.

📌 Project Purpose

This project demonstrates the development of a complete business analytics application using Python, Streamlit, SQL Server, database integration, authentication, data visualization, and Windows application packaging.

Developed using Python, Streamlit and SQL Server.
