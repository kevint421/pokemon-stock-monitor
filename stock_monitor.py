import requests
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PokemonStockMonitor:
    def __init__(self, url, email_config=None):
        self.url = url
        self.email_config = email_config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def check_stock(self):
        """Check if the product is in stock by looking for the specific button elements"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the specific IN STOCK button pattern:
            # <button class="add-to-cart-button--PZmQF btn--ICBoB btn-secondary--mtUol" type="button">Add to Cart</button>
            in_stock_button = soup.find('button', {
                'class': lambda x: x and 'add-to-cart-button--PZmQF' in x and 'btn-secondary--mtUol' in x,
                'type': 'button'
            })
            
            # Also check for the text content to be sure
            if in_stock_button and in_stock_button.get_text().strip() == 'Add to Cart':
                in_stock = True
                button_status = "IN STOCK - 'Add to Cart' button found"
            else:
                # Look for the specific OUT OF STOCK button pattern:
                # <button class="add-to-cart-button--PZmQF btn--ICBoB btn-tertiary--_2uKVi disabled--vkECP" disabled="">Unavailable</button>
                out_of_stock_button = soup.find('button', {
                    'class': lambda x: x and 'add-to-cart-button--PZmQF' in x and 'disabled--vkECP' in x,
                    'disabled': ''
                })
                
                # Also check for any button with "Unavailable" text and disabled attribute
                unavailable_button = soup.find('button', {'disabled': ''}, string='Unavailable')
                
                if out_of_stock_button or unavailable_button:
                    in_stock = False
                    button_status = "OUT OF STOCK - 'Unavailable' button found"
                else:
                    # Fallback: look for any add to cart button without the disabled class
                    fallback_cart_button = soup.find('button', string='Add to Cart')
                    if fallback_cart_button and not fallback_cart_button.get('disabled'):
                        in_stock = True
                        button_status = "IN STOCK - Fallback 'Add to Cart' button found"
                    else:
                        in_stock = False
                        button_status = "UNKNOWN STATE - No recognizable button pattern found"
            
            # Log current button state for debugging
            current_time = datetime.now().strftime("%H:%M:%S")
            logging.debug(f"[{current_time}] {button_status}")
            
            return in_stock, response.status_code
            
        except requests.RequestException as e:
            logging.error(f"Error checking stock: {e}")
            return False, None
    
    def send_notification(self, message):
        """Send email notification if configured"""
        if not self.email_config or not self.email_config.get('enabled', True):
            print(f"\n🚨 STOCK ALERT: {message}")
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = "Pokémon Center Stock Alert!"
            
            body = f"""
            Good news! The product you're monitoring is now available:
            
            {message}
            
            Product URL: {self.url}
            
            Hurry and grab it before it sells out again!
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['from_email'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logging.info("Email notification sent successfully!")
            
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            print(f"\n🚨 STOCK ALERT: {message}")
    
    def monitor(self, check_interval=300):
        """Start monitoring the product"""
        logging.info(f"Starting to monitor: {self.url}")
        logging.info(f"Check interval: {check_interval} seconds")
        
        while True:
            try:
                in_stock, status_code = self.check_stock()
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if status_code:
                    if in_stock:
                        message = f"🎉 Pokémon product is BACK IN STOCK!"
                        logging.info(message)
                        self.send_notification(message)
                        break  # Stop monitoring once in stock
                    else:
                        logging.info(f"[{current_time}] Still out of stock (Status: {status_code})")
                else:
                    logging.warning(f"[{current_time}] Failed to check stock")
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logging.info("Monitoring stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(check_interval)

def load_config():
    """Load configuration from environment variables"""
    # Check if required environment variables are set
    required_vars = ['PRODUCT_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📋 Please:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your configuration values")
        print("3. Run the script again")
        return None, None
    
    # Get product URL
    url = os.getenv('PRODUCT_URL')
    
    # Get check interval (default: 90 seconds)
    try:
        check_interval = int(os.getenv('CHECK_INTERVAL', '90'))
    except ValueError:
        check_interval = 90
        print("⚠️  Warning: Invalid CHECK_INTERVAL value, using default (90 seconds)")
    
    # Email configuration (optional)
    email_config = None
    email_enabled = os.getenv('EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
    
    if email_enabled:
        email_vars = ['SMTP_SERVER', 'SMTP_PORT', 'FROM_EMAIL', 'EMAIL_PASSWORD', 'TO_EMAIL']
        missing_email_vars = [var for var in email_vars if not os.getenv(var)]
        
        if missing_email_vars:
            print("⚠️  Warning: Email notifications disabled - missing email configuration:")
            for var in missing_email_vars:
                print(f"   - {var}")
            print("💡 To enable email notifications, add these to your .env file")
        else:
            try:
                email_config = {
                    'smtp_server': os.getenv('SMTP_SERVER'),
                    'smtp_port': int(os.getenv('SMTP_PORT')),
                    'from_email': os.getenv('FROM_EMAIL'),
                    'password': os.getenv('EMAIL_PASSWORD'),
                    'to_email': os.getenv('TO_EMAIL'),
                    'enabled': True
                }
            except ValueError:
                print("⚠️  Warning: Invalid SMTP_PORT value, email notifications disabled")
    
    return url, email_config, check_interval

def main():
    print("🎮 Pokémon Center Stock Monitor")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    if config[0] is None:  # URL is required
        return
    
    url, email_config, check_interval = config
    
    # Create monitor instance
    monitor = PokemonStockMonitor(url, email_config=email_config)
    
    # Display configuration
    print(f"🔗 Monitoring URL: {url}")
    print(f"⏰ Check interval: {check_interval} seconds ({check_interval/60:.1f} minutes)")
    
    if email_config:
        print(f"📧 Email notifications: Enabled ({email_config['to_email']})")
    else:
        print("📧 Email notifications: Disabled (console only)")
    
    print("🚀 Starting monitor... (Press Ctrl+C to stop)")
    print("-" * 40)
    
    # Start monitoring
    monitor.monitor(check_interval=check_interval)

if __name__ == "__main__":
    main()