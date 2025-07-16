# FinTrack - Team Member Search System

A realistic business application demonstrating team member management with search functionality. This Docker image contains a complete web application built with Flask and MySQL.

## Quick Start

```bash
# Pull the image
docker pull cyberctf/extract_data_without_columns_name:latest

# Run the application
docker run -d -p 3206:5000 --name fintrack-app cyberctf/extract_data_without_columns_name:latest

# Access the application
open http://localhost:3206
```

## Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/cyberctf/extract_data_without_columns_name.git
cd extract_data_without_columns_name

# Start all services
docker-compose up -d

# Access the application
open http://localhost:3206
```

## Features

- **Team Member Dashboard**: Search and manage team members
- **Modern UI**: Dark theme with glassmorphism design
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Search**: Instant search functionality
- **Business-Oriented**: Professional interface for team management

## Technical Stack

- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Database**: MySQL 5.7
- **Containerization**: Docker, Docker Compose

## Port Configuration

- **Web Application**: Port 3206
- **Database**: Port 3306 (internal)

## Environment Variables

- `MYSQL_HOST`: Database host (default: db)
- `MYSQL_USER`: Database user (default: fintrack_user)
- `MYSQL_PASSWORD`: Database password (default: fintrack_pass)
- `MYSQL_DATABASE`: Database name (default: fintrack_db)

## Default Credentials

The application comes with pre-configured team members:
- **Admin**: admin@fintrack.com
- **Manager**: jane.smith@fintrack.com
- **Users**: Various team members across different departments

## Support

For issues and questions, please visit our GitHub repository or contact our support team.

## License

This project is for educational purposes only. Use responsibly and only on systems you own or have explicit permission to test. 