import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_email_config():
    """Load email configuration from environment variables"""
    # Check if email is enabled
    email_enabled = os.getenv('EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
    
    if not email_enabled:
        print("❌ Email notifications are disabled in your .env file")
        print("💡 Set EMAIL_NOTIFICATIONS=true to enable email testing")
        return None
    
    # Check for required email environment variables
    email_vars = ['SMTP_SERVER', 'SMTP_PORT', 'FROM_EMAIL', 'EMAIL_PASSWORD', 'TO_EMAIL']
    missing_vars = [var for var in email_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required email configuration in .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📋 Please add these variables to your .env file:")
        print("   SMTP_SERVER=smtp.gmail.com")
        print("   SMTP_PORT=587")
        print("   FROM_EMAIL=your-email@gmail.com")
        print("   EMAIL_PASSWORD=your-gmail-app-password")
        print("   TO_EMAIL=your-email@gmail.com")
        return None
    
    try:
        email_config = {
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT')),
            'from_email': os.getenv('FROM_EMAIL'),
            'password': os.getenv('EMAIL_PASSWORD'),
            'to_email': os.getenv('TO_EMAIL')
        }
        return email_config
    except ValueError:
        print("❌ Invalid SMTP_PORT value in .env file (must be a number)")
        return None

def test_email_notification():
    """Test the email notification functionality"""
    
    print("🧪 Testing email notification...")
    
    # Load email configuration
    email_config = load_email_config()
    if not email_config:
        return False
    
    print(f"📧 Sending test email to: {email_config['to_email']}")
    
    try:
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = email_config['from_email']
        msg['To'] = email_config['to_email']
        msg['Subject'] = "🧪 Pokémon Stock Monitor - Test Email"
        
        test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        product_url = os.getenv('PRODUCT_URL', 'No URL configured')
        
        body = f"""
        ✅ SUCCESS! Your email notifications are working correctly.
        
        This is a test email from your Pokémon Center stock monitor script.
        
        Test sent at: {test_time}
        Monitoring URL: {product_url}
        
        🎉 When your monitored product comes back in stock,
        you'll receive a notification just like this one!
        
        Your stock monitor is ready to go! 🚀
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send the email
        print("🔄 Connecting to SMTP server...")
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        
        print("🔐 Logging in...")
        server.login(email_config['from_email'], email_config['password'])
        
        print("📤 Sending test email...")
        server.send_message(msg)
        server.quit()
        
        print("✅ SUCCESS! Test email sent successfully!")
        print("📱 Check your inbox for the test notification.")
        print("🎯 Your stock monitor email notifications are working perfectly!")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ AUTHENTICATION ERROR!")
        print("🔑 This usually means:")
        print("   1. You're using your regular Gmail password instead of an App Password")
        print("   2. 2-Factor Authentication isn't enabled")
        print("   3. App Password is incorrect")
        print("\n📋 To fix this:")
        print("   1. Go to myaccount.google.com")
        print("   2. Security → 2-Step Verification (enable if needed)")
        print("   3. App passwords → Generate new password for 'Mail'")
        print("   4. Update EMAIL_PASSWORD in your .env file with the 16-character app password")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP ERROR: {e}")
        print("🌐 This could be a network or server issue. Try again in a moment.")
        return False
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("🔧 Please check your email configuration in the .env file.")
        return False

def test_stock_alert_format():
    """Send a test email that looks exactly like the stock alert"""
    
    email_config = load_email_config()
    if not email_config:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email_config['from_email']
        msg['To'] = email_config['to_email']
        msg['Subject'] = "Pokémon Center Stock Alert!"  # Same as real alert
        
        product_url = os.getenv('PRODUCT_URL', 'https://www.pokemoncenter.com/product/example')
        
        # This is what the real stock alert will look like
        body = f"""
        Good news! The product you're monitoring is now available:
        
        🎉 Pokémon product is BACK IN STOCK!
        
        Product URL: {product_url}
        
        Hurry and grab it before it sells out again!
        
        (This is a test email - the product may not actually be in stock)
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['from_email'], email_config['password'])
        server.send_message(msg)
        server.quit()
        
        print("✅ Stock alert test email sent!")
        print("📱 Check your inbox - this is exactly what you'll receive when the item restocks!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending stock alert test: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has basic structure"""
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        print("\n📋 To set up your configuration:")
        print("1. Copy .env.example to .env:")
        print("   cp .env.example .env")
        print("2. Edit .env with your actual values:")
        print("   nano .env")
        print("3. Run this test again")
        return False
    
    # Check if required variables exist
    required_vars = ['FROM_EMAIL', 'EMAIL_PASSWORD', 'TO_EMAIL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️  Your .env file exists but is missing some email configuration:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== POKÉMON STOCK MONITOR EMAIL TEST ===\n")
    
    # Check if .env file is set up
    if not check_env_file():
        exit(1)
    
    # Test 1: Basic email functionality
    print("TEST 1: Basic Email Functionality")
    print("-" * 40)
    success = test_email_notification()
    
    if success:
        print("\n" + "="*50)
        print("TEST 2: Stock Alert Preview")
        print("-" * 40)
        
        response = input("\n🎯 Would you like to send a test stock alert email? (y/n): ").lower()
        if response in ['y', 'yes']:
            test_stock_alert_format()
            
        print("\n🚀 Your email notifications are ready!")
        print("💡 You can now run the main stock monitor script with confidence.")
    else:
        print("\n🔧 Please fix the email configuration issues above before running the stock monitor.")
        print("💡 Make sure your .env file has all the required email settings.")