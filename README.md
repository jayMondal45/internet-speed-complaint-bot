# 🐍 Internet Speed Complaint Bot (Fast.com + Twitter Automation)

A Python automation script that checks your internet speed using [Fast.com](https://fast.com) and automatically posts a **complaint tweet** to your Internet Service Provider (like **@JioCare**) if your speed drops below a defined threshold (e.g. 30 Mbps).

Built with **Selenium WebDriver**, it opens a browser, measures your speed, and posts a tweet for you — all while saving your Twitter login session securely in a local Chrome profile.

---

## 🚀 Features

* ✅ Measures actual speed from [Fast.com](https://fast.com)
* ⚡ Automatically detects Mbps or Kbps
* 🧠 Tweets complaint only if speed < threshold
* 🔐 Keeps your Twitter login session using Chrome profile
* 🕵️‍♂️ Includes anti-detection tweaks to avoid automation blocking
* 💬 Fully interactive — lets you confirm before posting

---

## 🧩 Requirements

* Python 3.8 or newer
* Google Chrome installed
* ChromeDriver (auto-installed if you use `webdriver_manager`)
* Twitter (X) account

---

## 📦 Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/<your-username>/internet-speed-complaint-bot.git
   cd internet-speed-complaint-bot
   ```

2. **Install dependencies**

   ```bash
   pip install selenium
   ```

3. **(Optional)** To manage ChromeDriver automatically:

   ```bash
   pip install webdriver-manager
   ```

---

## ⚙️ Configuration

You can adjust the complaint threshold inside the script:

```python
SPEED_THRESHOLD = 30  # Minimum acceptable Mbps
```

If your ISP is different (like Airtel or BSNL), change the tweet text near the bottom:

```python
complaint = f"Hi @Airtel_Presence, ..."
```

---

## ▶️ Usage

Run the script directly:

```bash
python main.py
```

Then follow the on-screen steps:

1. The script will open Fast.com and measure your internet speed.
2. If the speed is below your threshold, it opens Twitter (X).
3. Log in manually once (your session will be saved).
4. Review and post your complaint tweet.

---

## 🧠 Example Tweet

> Hi @JioCare, I'm on the ₹349/month plan but my internet speed is only 5 Mbps instead of the expected 30+ Mbps. Kindly look into this issue and resolve it soon. Thank you. #Jio #InternetIssue

---

## 🧰 Troubleshooting

* If the script says “Login timeout,” just rerun it and log in faster.
* Chrome might open a new profile; allow it to create one.
* You can close the browser manually anytime — nothing harmful is done automatically.

---

## 📄 License

This project is open-source under the **MIT License** — feel free to modify and improve it.

---

## ⭐ Show Your Support

If this bot saved you from slow internet rage 😤 —
Give it a ⭐ on GitHub and share it with others!

---

### Author

👨‍💻 **Joy Mondal**
💬 [GitHub Profile](https://github.com/jaymondal45)
