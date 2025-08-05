# Email Configuration for Campus Skill-Swap

## Current Setup

The application automatically chooses between two email backends:

1. **File-based Email Backend (Default/Development)**
   - Emails are saved as files in the `sent_emails/` directory
   - No external setup required
   - Good for development and testing

2. **SMTP Email Backend (Production)**
   - Emails are sent via SMTP (Gmail by default)
   - Requires email credentials
   - Used when `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` environment variables are set

## Setting Up Real Email Sending

### Option 1: Gmail (Recommended)

1. Create a `.env` file in the project root (copy from `.env.example`)
2. Set up Gmail App Password:
   - Go to your Google Account settings
   - Enable 2-factor authentication if not already enabled
   - Go to "App passwords" and generate a new app password
   - Copy the 16-character app password

3. Update your `.env` file:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   ```

### Option 2: Other Email Providers

Update the email settings in `settings.py`:

**Yahoo:**
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
```

**Outlook/Hotmail:**
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
```

**Custom SMTP:**
```python
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True
```

## Testing Email Functionality

### With File Backend (Default)
1. Perform an action that sends an email (register, password reset, etc.)
2. Check the `sent_emails/` directory for generated email files
3. Open the files to verify email content

### With SMTP Backend
1. Set up email credentials as described above
2. Perform an action that sends an email
3. Check the recipient's email inbox

## Email Features in the Application

The following features send emails:

1. **Welcome Email** - Sent when a user registers
2. **OTP Verification** - Sent during password reset
3. **Request Notifications** - Sent when skill swap requests are made
4. **Session Notifications** - Sent for session updates

## Troubleshooting

### Common Issues:

1. **"Authentication failed" error**
   - Make sure you're using an App Password, not your regular password
   - Verify 2-factor authentication is enabled
   - Check that the email and password are correct

2. **"Connection refused" error**
   - Check your internet connection
   - Verify the SMTP server and port settings
   - Some networks block SMTP ports

3. **Emails not appearing in inbox**
   - Check spam/junk folder
   - Verify the recipient email address
   - Check email server logs for delivery issues

### For Development:
If you don't want to set up real email sending, the file-based backend is perfectly functional for development and testing. Simply check the `sent_emails/` directory to see what emails would have been sent.