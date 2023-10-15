
# Deploying Django on Google Cloud Instance

This guide provides steps to deploy a Django application on a Google Cloud instance.

## 1. **Setting Up the Google Cloud Instance**:
- Create a new VM instance in the Google Cloud Console.
- Ensure you select the appropriate region, machine type, and OS (typically, a flavor of Linux like Ubuntu).
- SSH into your instance once it's up and running.

## 2. **Installing Required Packages**:
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip python3-venv nginx
```

## 3. **Set Up Your Project**:
- Transfer your Django project to the instance. You can use `scp`, `rsync`, or even `git clone` if your project is on a Git repository.
- Navigate to your project directory.

## 4. **Set Up a Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. **Install Your Project Dependencies**:
```bash
pip install -r requirements.txt
```

## 6. **Configure Django Settings**:
- Ensure `ALLOWED_HOSTS` in `settings.py` includes your domain name and the IP address of the instance.
- Set `DEBUG = False` for production deployment.
- Confirm your database settings are correct and point to your production database.

## 7. **Database Setup**:
- If using a database, ensure it's set up and accessible from your instance.
- Run migrations:
  ```bash
  python manage.py migrate
  ```

## 8. **Static Files**:
- Collect static files:
  ```bash
  python manage.py collectstatic
  ```

## 9. **Gunicorn Setup**:
- Install Gunicorn in your virtual environment:
  ```bash
  pip install gunicorn
  ```

- Run Gunicorn:
  ```bash
  gunicorn yourproject.wsgi:application --bind 127.0.0.1:8000
  ```

## 10. **Configure Nginx**:
- Create or modify Nginx configuration:
  ```bash
  sudo nano /etc/nginx/sites-available/default
  ```

- Add configuration (modify as per your project):
  ```nginx
  server {
      listen 80;
      server_name yourdomain.com www.yourdomain.com;

      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $host;
          proxy_redirect off;
      }

      location /static/ {
          alias /path/to/your/static/files/;
      }

      location /media/ {
          alias /path/to/your/media/files/;
      }
  }
  ```

- Restart Nginx:
  ```bash
  sudo systemctl restart nginx
  ```

## 11. **Set Up SSL with Certbot**:
- Install Certbot:
  ```bash
  sudo apt install certbot python3-certbot-nginx
  ```

- Obtain and install certificates:
  ```bash
  sudo certbot --nginx
  ```

## 12. **Automate Gunicorn with Systemd**:
- Create a Gunicorn systemd service file:
  ```bash
  sudo nano /etc/systemd/system/gunicorn.service
  ```

- Add configuration (modify as per your project):
  ```ini
  [Unit]
  Description=gunicorn daemon
  After=network.target

  [Service]
  User=username
  Group=groupname
  WorkingDirectory=/path/to/your/django/project
  ExecStart=/path/to/your/venv/bin/gunicorn yourproject.wsgi:application --bind 127.0.0.1:8000

  [Install]
  WantedBy=multi-user.target
  ```

- Start and enable Gunicorn service:
  ```bash
  sudo systemctl start gunicorn
  sudo systemctl enable gunicorn
  ```

## 13. **Final Steps**:
- Open required ports on Google Cloud firewall (e.g., 80, 443).
- Set up regular database backups.
- Monitor server's resources and performance. Adjust the instance type or scale as needed.
