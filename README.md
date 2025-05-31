# 🎮 Pokémon Center Stock Monitor

A Python script that monitors Pokémon Center products for stock availability and sends notifications when items come back in stock.

## ✨ Features

- 🔍 **Smart Stock Detection** - Monitors specific button elements for accurate stock status
- 📧 **Email Notifications** - Get instant alerts when products restock
- ⚙️ **Customizable** - Configure any Pokémon Center product URL
- 🕐 **Flexible Timing** - Set custom check intervals
- 🛡️ **Robust** - Handles network errors and continues monitoring

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pokemon-stock-monitor.git
cd pokemon-stock-monitor
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv pokemon_monitor

# Activate virtual environment
# Mac/Linux:
source pokemon_monitor/bin/activate
# Windows:
pokemon_monitor\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 5. Run the Monitor
```bash
python stock_monitor.py
```

## ⚙️ Configuration

### Required Configuration

Edit your `.env` file with these required settings:

```bash
# Product URL to monitor
PRODUCT_URL=https://www.pokemoncenter.com/product/YOUR-PRODUCT-URL-HERE

# Check interval in seconds (90 = 1.5 minutes)
CHECK_INTERVAL=90
```

### Optional Email Notifications

To enable email notifications, add these to your `.env` file:

```bash
# Email settings (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
TO_EMAIL=your-email@gmail.com
EMAIL_NOTIFICATIONS=true
```

#### Gmail Setup
1. Enable 2-Factor Authentication on your Google Account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an App Password for "Mail"
4. Use the 16-character app password in your `.env` file

## 🎯 Supported Products

This monitor works with any Pokémon Center product page that uses their standard button structure:

- Elite Trainer Boxes
- Booster Packs
- Plushies
- Figures
- Collectibles

Simply replace the `PRODUCT_URL` in your `.env` file with any Pokémon Center product URL.

## 🖥️ Running in Background

### Using Screen (Recommended for Mac/Linux)
```bash
# Start screen session
screen -S pokemon_monitor

# Run the script
python stock_monitor.py

# Detach from screen (Ctrl+A, then D)
# Script continues running in background
```

### Using nohup
```bash
nohup python stock_monitor.py > stock_monitor.log 2>&1 &
```

## 🧪 Testing

Test your email configuration:
```bash
python test_email.py
```

## 📁 Project Structure

```
pokemontracker/
├── stock_monitor.py      # Main monitoring script
├── test_email.py         # Email testing script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🛠️ Troubleshooting

### Common Issues

**Email Authentication Error:**
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that all email settings in `.env` are correct

**Stock Detection Issues:**
- The script is designed for current Pokémon Center website structure
- If button classes change, the script may need updates

**Network Errors:**
- Script will automatically retry after network failures
- Check your internet connection if errors persist

### Debug Mode

Enable debug logging by modifying the script:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```
