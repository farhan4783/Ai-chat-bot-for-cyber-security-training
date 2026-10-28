import json
from pathlib import Path

DATASET = {
    "version": "2.0",
    "description": "Comprehensive Cybersecurity Awareness Training Dataset for Local AI CyberBot",
    "intents": [
        {
            "tag": "greeting",
            "patterns": [
                "Hi", "Hello", "Hey", "Hey there", "Good morning", "Good afternoon", "Good evening",
                "Hi CyberBot", "Is anyone there?", "Greetings", "Yo", "Start", "Help me"
            ],
            "summary": "Welcome to CyberBot, your dedicated AI Cybersecurity Awareness Trainer.",
            "action_steps": [
                "Ask any question about online safety, phishing, passwords, or ransomware.",
                "Type 'quiz' to test your cybersecurity knowledge with interactive scenario questions.",
                "Paste an email or message snippet to analyze it for phishing red flags.",
                "Type 'emergency' if you think your account or device was recently compromised."
            ],
            "pro_tip": "Cybersecurity isn't about knowing complex technical jargon—it is about building daily habits of verification and caution.",
            "follow_ups": [
                "How do I recognize a phishing email?",
                "What should I do if I clicked a suspicious link?",
                "How can I create an uncrackable password?"
            ],
            "responses": [
                "Hello! I am CyberBot, your cybersecurity awareness trainer. Ask me about phishing, malware, passwords, safe browsing, or type 'quiz' to test your skills!",
                "Greetings! I'm here to help you strengthen your digital defenses. What cybersecurity topic or challenge can we explore today?"
            ]
        },
        {
            "tag": "bot_capabilities",
            "patterns": [
                "What can you do?", "What are your features?", "Who are you?", "What is cyberbot?",
                "How can you help me?", "Explain your capabilities", "What topics do you know?"
            ],
            "summary": "CyberBot is a 100% locally-trained cybersecurity awareness assistant designed to train employees and individuals on modern digital threats.",
            "action_steps": [
                "Identify Phishing & Social Engineering tactics (emails, SMS, phone calls).",
                "Explain Password security, Passkeys, and Multi-Factor Authentication (MFA).",
                "Provide step-by-step containment procedures during an active security incident.",
                "Simulate interactive cybersecurity quizzes and knowledge evaluations.",
                "Analyze suspicious message snippets for urgency, impersonation, and spoofed domains."
            ],
            "pro_tip": "I run 100% locally on your machine—your questions and text are never sent to third-party cloud servers.",
            "follow_ups": [
                "Can you check a suspicious email for me?",
                "Start a cybersecurity quiz",
                "What is multi-factor authentication?"
            ],
            "responses": [
                "I am your local cybersecurity coach! I can guide you through threat prevention, analyze suspicious messages, train you with interactive quizzes, and provide incident response checklists."
            ]
        },
        {
            "tag": "phishing_basics",
            "patterns": [
                "What is phishing?", "How to spot phishing?", "Recognize a phishing email",
                "Signs of a phishing message", "How do I identify phishing?", "Phishing email red flags",
                "How can I tell if an email is fake?", "Common phishing examples", "Phishing indicators",
                "Tell me about phishing attacks", "Suspicious email warning signs"
            ],
            "summary": "Phishing is a deceptive social engineering attack where cybercriminals impersonate reputable organizations or colleagues to steal credentials, money, or sensitive data.",
            "action_steps": [
                "Inspect the sender's actual email address (not just the display name) for typosquatting (e.g., @micros0ft.com or @paypal-security-alert.net).",
                "Look for artificial urgency ('Account suspended in 24 hours!', 'Immediate wire transfer required').",
                "Hover over hyperlinks (without clicking) to inspect the actual destination URL.",
                "Never open unsolicited attachments, especially archives (.zip, .rar, .iso) or macro-enabled documents.",
                "Verify suspicious requests via a secondary, trusted communication channel (call the person or visit the official website directly)."
            ],
            "red_flags": [
                "Generic greetings ('Dear Customer') when they should know your name.",
                "Urgent threats of account closure, legal action, or fines.",
                "Requests for passwords, gift cards, wire transfers, or MFA codes.",
                "Mismatched URLs that don't match the company's real domain name."
            ],
            "pro_tip": "When in doubt, never click the email link. Open your browser, type the official website URL manually, and log in from there.",
            "follow_ups": [
                "What should I do if I clicked a phishing link?",
                "What is spear phishing?",
                "Can you analyze a suspicious email for me?"
            ],
            "responses": [
                "Phishing relies on impersonation, artificial urgency, and deceptive links. Always check the true sender domain, hover over links before clicking, and verify unexpected requests through an independent channel."
            ]
        },
        {
            "tag": "spear_phishing_and_whaling",
            "patterns": [
                "What is spear phishing?", "Explain spear phishing", "What is whaling?",
                "Targeted phishing attacks", "Executive impersonation", "How does spear phishing work?",
                "Difference between phishing and spear phishing", "Whale phishing"
            ],
            "summary": "Spear phishing is a highly targeted attack where adversaries research a specific individual or company (using LinkedIn, social media, or company websites) to craft convincing, personalized lures. Whaling specifically targets senior executives, directors, or finance personnel.",
            "action_steps": [
                "Be aware that attackers can cite your real job title, coworkers' names, and current projects.",
                "Establish dual-control out-of-band authorization for any financial transaction or vendor bank detail changes.",
                "Scrutinize requests coming from lookalike executive domains (e.g., ceo-office@company-corp.com instead of company.com).",
                "Limit the amount of sensitive business and organizational hierarchy data shared publicly on social media."
            ],
            "red_flags": [
                "Emails claiming the CEO is in an 'urgent meeting' and cannot take phone calls.",
                "Requests to bypass standard purchase order or invoice verification protocols.",
                "Direct requests for employee W-2 forms, payroll accounts, or employee databases."
            ],
            "pro_tip": "If a high-level executive asks you to break normal security protocol, that urgency itself is the #1 indicator of spear phishing.",
            "follow_ups": [
                "What is business email compromise (BEC)?",
                "How do attackers impersonate email addresses?",
                "How can I report a spear phishing attempt?"
            ],
            "responses": [
                "Spear phishing uses tailored personal information to lower your guard. Whaling targets executives and finance teams to execute fraudulent wire transfers. Always verify out-of-band using an established phone number."
            ]
        },
        {
            "tag": "smishing_and_vishing",
            "patterns": [
                "What is smishing?", "What is vishing?", "SMS phishing", "Fake bank text message",
                "Scam phone call", "Text message scam", "Received weird SMS asking to verify account",
                "Package delivery text scam", "IRS phone call scam", "Voice phishing"
            ],
            "summary": "Smishing is phishing conducted via SMS text messages, while Vishing is voice phishing conducted over phone calls or automated voice bots. Both aim to induce immediate panic.",
            "action_steps": [
                "Never click links inside unexpected text messages—even if the sender claims to be USPS, UPS, your bank, or Netflix.",
                "Legitimate banks will NEVER call or text you demanding your one-time SMS verification passcode or debit card PIN.",
                "If someone calls claiming to be from IT support, law enforcement, or your bank, hang up immediately.",
                "Call the institution back using the official phone number printed on the back of your card or on their official website."
            ],
            "red_flags": [
                "Texts regarding 'Unclaimed package', 'Suspended debit card', or 'Overdue toll fees' containing shortened URLs.",
                "Callers with urgent or aggressive tones demanding immediate payment via gift cards or wire transfers.",
                "Callers asking you to read back a verification code sent to your phone."
            ],
            "pro_tip": "Forward suspicious SMS messages to spam reporting code 7726 (SPAM) on major mobile carriers to help block the campaign.",
            "follow_ups": [
                "Why is SMS 2FA dangerous?",
                "What should I do if I shared my debit card details?",
                "How do scammers spoof phone numbers?"
            ],
            "responses": [
                "Smishing (SMS) and Vishing (phone calls) exploit mobile convenience and urgency. Never click links in unprompted text messages and never read one-time passcodes over the phone."
            ]
        },
        {
            "tag": "business_email_compromise",
            "patterns": [
                "What is BEC?", "Business email compromise", "CEO fraud", "Vendor invoice fraud",
                "Urgent wire transfer email", "CEO asking for gift cards", "Supplier changed bank account details",
                "Fake executive email", "Payroll diversion scam"
            ],
            "summary": "Business Email Compromise (BEC) occurs when an attacker compromises a real corporate email account or spoofs a trusted vendor/executive to trick employees into transferring funds or revealing proprietary information.",
            "action_steps": [
                "Institute a strict policy: Any change in vendor banking details requires verbal voice confirmation with known contacts.",
                "Verify through a separate phone number already on file—never use the phone number provided in the suspect email.",
                "Flag and filter emails originating from external sources with 'External' email banners.",
                "Train staff to recognize the classic 'gift card request'—CEOs do not ask junior staff to buy Apple or Google Play gift cards."
            ],
            "red_flags": [
                "Sudden change of remittance bank accounts to overseas or unfamiliar institutions.",
                "Insistence on absolute secrecy ('Keep this between us until the deal closes').",
                "Slight domain variations (e.g., acme-supplier.com instead of acmesupplier.com)."
            ],
            "pro_tip": "A 30-second phone call to verify an invoice can prevent millions of dollars in corporate wire fraud.",
            "follow_ups": [
                "What is spear phishing?",
                "How can companies prevent invoice fraud?",
                "How do attackers hack into corporate email accounts?"
            ],
            "responses": [
                "BEC is responsible for billions in annual losses. Always establish dual-signature policies and verify changes to payment details via a confirmed verbal phone call."
            ]
        },
        {
            "tag": "ransomware",
            "patterns": [
                "What is ransomware?", "My files are locked", "Computer files have weird extension",
                "Ransom note on desktop", "How does ransomware spread?", "Should I pay the ransom?",
                "How to prevent ransomware?", "Ransomware protection", "What to do if infected with ransomware"
            ],
            "summary": "Ransomware is malicious software that encrypts your files and holds them hostage while demanding payment (usually in cryptocurrency) in exchange for a decryption key.",
            "action_steps": [
                "IMMEDIATELY disconnect infected devices from Wi-Fi, Ethernet, and Bluetooth to prevent network lateral movement.",
                "Do NOT pay the ransom—security agencies (FBI/CISA) advise against payment because it funds criminal syndicates and provides zero guarantee of file recovery.",
                "Report the incident immediately to your IT security department, incident response team, or local cybersecurity authorities.",
                "Maintain immutable, offline backups following the 3-2-1 backup rule (3 copies, 2 different media, 1 kept offline/offsite)."
            ],
            "red_flags": [
                "Files suddenly changing extensions to unknown strings (e.g., .locked, .crypt, .lockbit).",
                "Desktop background replaced with ransom instructions and countdown timers.",
                "Antivirus or Endpoint Detection and Response (EDR) software alerting on shadow copy deletion."
            ],
            "pro_tip": "Your strongest defense against ransomware is having an offline, air-gapped backup that cannot be reached or encrypted over the network.",
            "follow_ups": [
                "What is the 3-2-1 backup rule?",
                "How does malware infect a computer?",
                "What should I do right now if I suspect ransomware?"
            ],
            "responses": [
                "Ransomware encrypts your digital assets. Disconnect the computer from all networks immediately, do not pay the ransom, notify IT security, and restore clean files from offline backups."
            ]
        },
        {
            "tag": "malware_and_viruses",
            "patterns": [
                "What is malware?", "Types of malware", "What is a Trojan?", "What is spyware?",
                "Difference between virus and malware", "How do I know if I have malware?",
                "What is a keylogger?", "Signs of computer infection", "How to remove malware?",
                "What are infostealers?"
            ],
            "summary": "Malware (malicious software) is an umbrella term covering viruses, worms, trojans, ransomware, spyware, and keyloggers designed to damage, disrupt, or gain unauthorized access to computer systems.",
            "action_steps": [
                "Keep Microsoft Defender or an enterprise EDR solution active and updated.",
                "Never download cracked software, keygens, torrents, or pirated games—they are the primary delivery vector for info-stealer malware.",
                "Run a full anti-malware scan if your computer exhibits unexpected slowdowns, high CPU usage, or browser redirects.",
                "Keep your operating system and browsers updated to patch known vulnerabilities (CVEs)."
            ],
            "red_flags": [
                "Browser homepage or default search engine changing without your consent.",
                "Frequent pop-ups, even when the web browser is closed.",
                "Accounts being accessed from unfamiliar locations (a sign of infostealer credential theft)."
            ],
            "pro_tip": "Infostealers search your browser cache for saved passwords and session cookies. Never store sensitive master passwords in your plain browser storage.",
            "follow_ups": [
                "Are password managers safer than browser saved passwords?",
                "How do software updates protect against malware?",
                "What is a zero-day vulnerability?"
            ],
            "responses": [
                "Malware encompasses all harmful software like trojans, spyware, and worms. Avoid untrusted downloads, keep automatic updates enabled, and maintain active endpoint protection."
            ]
        },
        {
            "tag": "password_hygiene",
            "patterns": [
                "How to create a strong password?", "Password best practices", "Password security tips",
                "What is a passphrase?", "Should I change my password frequently?", "Password length vs complexity",
                "Why is password reuse bad?", "How do hackers crack passwords?", "Safe passwords guide"
            ],
            "summary": "Strong authentication starts with high entropy: Passwords should be long, unique for every account, and unpredictable. Modern standards (NIST SP 800-63B) favor length and passphrases over complex, hard-to-remember character combinations.",
            "action_steps": [
                "Use a Passphrase: Combine 4 to 5 random, unrelated words (e.g., 'correct-horse-battery-staple' or 'purple-cactus-orbit-piano!').",
                "Aim for at least 14 to 16 characters in length—length provides exponential resistance against brute-force cracking.",
                "NEVER reuse the same password across multiple accounts. If one service suffers a breach, attackers use automated 'credential stuffing' to breach all your accounts.",
                "Use a dedicated Password Manager to generate and store random 20+ character passwords."
            ],
            "red_flags": [
                "Using personal info: birthdays, pet names, kids' names, spouse names, sports teams.",
                "Predictable substitutions like 'P@ssw0rd2024!'. Automated cracking dictionaries guess these in milliseconds.",
                "Writing passwords on sticky notes attached to your monitor or under your keyboard."
            ],
            "pro_tip": "A 16-character passphrase made of 4 common words is vastly more secure and easier to remember than an 8-character string of random symbols.",
            "follow_ups": [
                "What is a password manager?",
                "What is credential stuffing?",
                "What is multi-factor authentication?"
            ],
            "responses": [
                "Focus on length and uniqueness. Use 4-5 random words to create memorable passphrases, never reuse passwords, and let a password manager handle the rest."
            ]
        },
        {
            "tag": "password_managers",
            "patterns": [
                "What is a password manager?", "Are password managers safe?", "Which password manager to use?",
                "Is Bitwarden safe?", "Is 1Password safe?", "Why use a password manager?",
                "What if the password manager gets hacked?", "Password manager benefits"
            ],
            "summary": "A password manager is an encrypted digital vault that generates, stores, and autofills strong, unique credentials for all your web services and applications.",
            "action_steps": [
                "Adopt a reputable password manager (e.g., Bitwarden, 1Password, KeePassXC).",
                "Create one extremely strong, memorable Master Passphrase (20+ characters) that you never write down or share.",
                "Enable Multi-Factor Authentication (preferably with a hardware security key or authenticator app) on your password manager vault.",
                "Leverage password managers to protect against phishing: They will not autofill your credentials if you land on a spoofed phishing URL."
            ],
            "red_flags": [
                "Using the browser's built-in password store without a master password lock.",
                "Storing passwords in unencrypted Word, Excel, or Notepad files."
            ],
            "pro_tip": "Password managers automatically protect you against typosquatting phishing sites: if the domain is fake, the password manager simply won't offer to autofill.",
            "follow_ups": [
                "How do passkeys compare to password managers?",
                "How do I create a secure master passphrase?",
                "What is multi-factor authentication?"
            ],
            "responses": [
                "Password managers are essential modern security tools. They use zero-knowledge end-to-end encryption so only you hold the decryption key. They prevent password reuse and neutralize phishing."
            ]
        },
        {
            "tag": "multi_factor_authentication",
            "patterns": [
                "What is 2FA?", "What is MFA?", "What is multi factor authentication?",
                "Why should I use MFA?", "Is two factor authentication secure?",
                "Authenticator apps vs SMS", "Best MFA method", "How does 2FA work?",
                "Explain two factor authentication"
            ],
            "summary": "Multi-Factor Authentication (MFA) requires two or more distinct verification factors before granting access: Something you know (password), Something you have (authenticator app, security key), and Something you are (biometrics).",
            "action_steps": [
                "Enable MFA on every critical account, starting with your email, banking, and password manager.",
                "Rank MFA methods from strongest to weakest: 1) Hardware Keys (YubiKey/FIDO2), 2) Passkeys, 3) Authenticator Apps (Google Authenticator, Aegis), 4) SMS/Email codes.",
                "Never share your 6-digit MFA code with ANYONE over the phone, email, or chat—no legitimate technician will ask for it.",
                "Save your one-time emergency backup recovery codes in a secure, encrypted offline location."
            ],
            "red_flags": [
                "Receiving unsolicited MFA prompts when you are not trying to log in (indicates your password has already been compromised).",
                "Anyone claiming to be support asking you to 'read back the code you just received'."
            ],
            "pro_tip": "Enabling MFA blocks over 99% of automated credential-stuffing and account takeover attacks.",
            "follow_ups": [
                "What is an MFA fatigue attack?",
                "What are passkeys?",
                "Why is SMS verification risky?"
            ],
            "responses": [
                "MFA adds a critical second layer of defense. Even if attackers steal your password, they cannot access your account without your physical second factor. Prefer authenticator apps or security keys over SMS."
            ]
        },
        {
            "tag": "mfa_fatigue_and_bypass",
            "patterns": [
                "What is MFA fatigue?", "MFA bombing", "Push notification spam",
                "Spammed with 2FA notifications", "How do hackers bypass MFA?",
                "What to do if getting repeated MFA requests?", "MFA fatigue attack"
            ],
            "summary": "MFA Fatigue (also called MFA Bombing) is a social engineering technique where attackers who already have your password send dozens of push notifications to your phone in hopes you will accidentally tap 'Approve' to make the buzzing stop.",
            "action_steps": [
                "NEVER tap 'Approve' on an unexpected MFA notification.",
                "If you receive repeated unsolicited MFA requests, decline the prompt immediately and report it to IT security.",
                "Change your account password immediately from a trusted device—the spammed notifications prove your password is known to attackers.",
                "Switch to number-matching MFA (where you must type the numbers shown on the screen into your authenticator app)."
            ],
            "red_flags": [
                "Multiple push notifications arriving late at night or during meetings.",
                "A caller pretending to be IT claiming: 'We are sending a test prompt, please tap Approve to clear the error'."
            ],
            "pro_tip": "If you tap 'Decline' on an MFA prompt, modern systems automatically trigger an alert to your company's security operations center (SOC).",
            "follow_ups": [
                "What are passkeys?",
                "What should I do if I approved a suspicious MFA prompt?",
                "How can I secure my accounts?"
            ],
            "responses": [
                "MFA fatigue exploits human frustration. Never approve an unprompted sign-in request. Decline the prompt and immediately change your password, because the attacker already knows it."
            ]
        },
        {
            "tag": "passkeys",
            "patterns": [
                "What are passkeys?", "How do passkeys work?", "Are passkeys better than passwords?",
                "What is FIDO2?", "Passkey security", "How to set up passkeys?",
                "Explain passkeys", "Can passkeys be phished?"
            ],
            "summary": "Passkeys are a modern, passwordless authentication standard based on FIDO2/WebAuthn public-key cryptography. They replace passwords with cryptographic key pairs stored on your device and unlocked via biometrics (Face ID/fingerprint) or device PIN.",
            "action_steps": [
                "Adopt passkeys for supported services like Google, Apple, Microsoft, Amazon, and GitHub.",
                "Enjoy phishing immunity: Passkeys are cryptographically bound to the exact website domain name—they physically cannot be entered on or phished by a fake website.",
                "Sync passkeys securely through your trusted ecosystem (Apple iCloud Keychain, Google Password Manager, or Bitwarden/1Password).",
                "Keep at least two devices enrolled (e.g., your laptop and your phone) so you don't lose account access if one device is damaged."
            ],
            "pro_tip": "Passkeys eliminate the possibility of phishing and credential reuse entirely. They represent the gold standard of modern identity security.",
            "follow_ups": [
                "How do passkeys prevent phishing?",
                "What is multi-factor authentication?",
                "Are password managers still useful with passkeys?"
            ],
            "responses": [
                "Passkeys replace passwords with un-phishable cryptographic keys bound to specific domains. You unlock them with your fingerprint or face scan, making credential theft practically impossible."
            ]
        },
        {
            "tag": "public_wifi_risks",
            "patterns": [
                "Is public Wi-Fi safe?", "Risks of public Wi-Fi", "Using hotel Wi-Fi",
                "Airport Wi-Fi safety", "What is an evil twin attack?", "Man in the middle attack Wi-Fi",
                "How to stay safe on public Wi-Fi?", "Should I use Wi-Fi at coffee shops?",
                "Public Wi-Fi security tips"
            ],
            "summary": "Public Wi-Fi networks in airports, hotels, and cafes are unencrypted open networks. Attackers can snoop on unencrypted traffic, conduct Man-In-The-Middle (MITM) attacks, or set up rogue 'Evil Twin' access points with identical names.",
            "action_steps": [
                "Turn off 'Auto-Connect to Open Wi-Fi' on your phone and laptop.",
                "Use a trusted Virtual Private Network (VPN) or use your phone's cellular hotspot when performing banking or sensitive work.",
                "Ensure every visited website displays 'HTTPS' and has no SSL certificate warnings.",
                "Turn off File Sharing and AirDrop/Nearby Share when connected to public hotspots."
            ],
            "red_flags": [
                "Two identical network names (e.g., 'Starbucks_Guest' and 'Starbucks_Guest_Free').",
                "Networks asking you to install a security certificate or download an app to gain internet access.",
                "Browser SSL certificate warnings ('Your connection is not private')."
            ],
            "pro_tip": "Your mobile phone's personal hotspot is exponentially safer than any free airport or coffee shop public Wi-Fi network.",
            "follow_ups": [
                "What does a VPN do?",
                "What is HTTPS?",
                "How do attackers create fake Wi-Fi hotspots?"
            ],
            "responses": [
                "Public Wi-Fi can expose your device to traffic eavesdropping and rogue access points. Use a reputable VPN or cellular hotspot, ensure HTTPS connections, and disable file sharing."
            ]
        },
        {
            "tag": "vpn_usage",
            "patterns": [
                "What is a VPN?", "What does a VPN do?", "Do I need a VPN?",
                "When to use a VPN?", "Can a VPN protect against phishing?",
                "Does a VPN make me anonymous?", "VPN myths and facts", "How does VPN work?"
            ],
            "summary": "A Virtual Private Network (VPN) creates an encrypted tunnel between your device and a secure server, protecting your network traffic from local eavesdroppers and disguising your IP address.",
            "action_steps": [
                "Use a VPN when working on public Wi-Fi, in hotels, or connecting to company internal systems remotely.",
                "Understand what a VPN DOES NOT DO: It does not stop phishing, it does not prevent malware downloads, and it does not make you immune to credential theft.",
                "Choose reputable, paid, no-logs VPN providers over suspicious 'free' VPNs that sell your browsing data.",
                "Always use your organization's official corporate VPN when accessing internal corporate applications."
            ],
            "pro_tip": "A VPN protects your connection in transit, but if you type your password into a phishing site, a VPN will not protect you.",
            "follow_ups": [
                "Is public Wi-Fi safe?",
                "What is data encryption?",
                "How can I spot a phishing site?"
            ],
            "responses": [
                "A VPN encrypts your network traffic, shielding you on untrusted public Wi-Fi networks. However, it does not stop you from falling for phishing links or downloading malware."
            ]
        },
        {
            "tag": "safe_browsing_and_https",
            "patterns": [
                "How to browse safely?", "What is HTTPS?", "Does HTTPS mean a site is safe?",
                "Padlock icon in browser", "What is typosquatting?", "Suspicious website warning",
                "How to check if a website is legit?", "Safe browsing tips", "Dangerous websites"
            ],
            "summary": "Safe browsing involves inspecting domain names, understanding SSL/TLS encryption, and avoiding drive-by download traps. Crucially, HTTPS means your connection is encrypted, NOT that the website owner is honest.",
            "action_steps": [
                "Inspect the domain name carefully: Check for typosquatting (e.g., paypa1.com, netfIix.com with an uppercase 'i').",
                "Remember: Attackers use HTTPS too! Over 80% of modern phishing websites have valid SSL certificates and padlock icons.",
                "Never bypass browser security interstitial warnings ('Deceptive site ahead').",
                "Keep browser extensions to a minimum and audit permissions regularly."
            ],
            "red_flags": [
                "Websites with countdown timers demanding you claim a prize or install an update immediately.",
                "Download prompts that initiate automatically without you clicking anything.",
                "Unusual top-level domains (.xyz, .top, .work) used for mainstream bank or government services."
            ],
            "pro_tip": "HTTPS protects data from eavesdroppers between you and the server. It does NOT guarantee that the server doesn't belong to a criminal.",
            "follow_ups": [
                "How do attackers create lookalike domains?",
                "What is drive-by malware?",
                "How can I spot a phishing message?"
            ],
            "responses": [
                "Browsing safely means verifying domain names and not trusting a site solely because it has HTTPS. Avoid suspicious downloads, keep extensions minimal, and never ignore browser warnings."
            ]
        },
        {
            "tag": "software_updates_and_patches",
            "patterns": [
                "Why are software updates important?", "Should I update my phone?",
                "Why patch software?", "What is a zero-day vulnerability?", "Can I postpone updates?",
                "Do updates slow down computers?", "Operating system updates security", "Patch Tuesday"
            ],
            "summary": "Software updates and security patches fix known vulnerabilities and programming flaws (CVEs) that cybercriminals actively scan the internet to exploit.",
            "action_steps": [
                "Enable automatic updates for your operating system (Windows/macOS), browsers (Chrome/Firefox/Edge), and mobile devices.",
                "Restart your computer when updates require it—many critical patches don't take effect until the system reboot completes.",
                "Uninstall obsolete software and old browser extensions that you no longer use.",
                "Apply critical security patches within 24 to 48 hours of release."
            ],
            "red_flags": [
                "Ignoring 'Update Available' notifications for weeks at a time.",
                "Downloading 'Flash Player' or 'Video Player' updates from pop-up banners—these are almost always malware."
            ],
            "pro_tip": "Over 90% of successful corporate breaches exploit software vulnerabilities for which a security patch was already available for months.",
            "follow_ups": [
                "What is a zero-day exploit?",
                "How does malware infect a device?",
                "What is endpoint security?"
            ],
            "responses": [
                "Software updates are your primary armor against known cyber exploits. Enable automatic updates, reboot promptly, and only download updates through official system settings."
            ]
        },
        {
            "tag": "data_encryption",
            "patterns": [
                "What is data encryption?", "How does encryption work?", "What is BitLocker?",
                "What is FileVault?", "Encryption at rest vs in transit", "Why encrypt data?",
                "Full disk encryption benefits", "Is encrypted data safe?"
            ],
            "summary": "Encryption scrambles plaintext data into unreadable ciphertext using mathematical algorithms and cryptographic keys, ensuring that only authorized parties holding the key can decrypt it.",
            "action_steps": [
                "Enable full-disk encryption on all laptops and mobile devices (BitLocker on Windows, FileVault on macOS).",
                "If a full-disk encrypted laptop is lost or stolen, thieves cannot read your files even if they pull out the physical hard drive.",
                "Ensure sensitive files sent via email or cloud share are encrypted or password-protected with out-of-band key sharing.",
                "Safeguard your BitLocker or FileVault recovery key in a secure, non-public vault."
            ],
            "pro_tip": "Full disk encryption turns a stolen laptop from a devastating corporate data breach into a minor hardware replacement incident.",
            "follow_ups": [
                "What is physical security?",
                "How does BitLocker work?",
                "What is clean desk policy?"
            ],
            "responses": [
                "Encryption protects data both at rest (stored on devices) and in transit (traveling over networks). Always turn on BitLocker or FileVault so stolen hardware cannot lead to stolen data."
            ]
        },
        {
            "tag": "safe_attachments_and_downloads",
            "patterns": [
                "Are email attachments safe?", "Dangerous file extensions", "Can PDFs contain viruses?",
                "What is a macro virus?", "Opening suspicious attachments", "Safe downloading tips",
                "Is it safe to open zip files from email?", "Malicious attachments warning"
            ],
            "summary": "Email attachments and web downloads are top infection vectors for trojans, info-stealers, and ransomware. Attackers disguise executables as invoices, resumes, or shipping manifests.",
            "action_steps": [
                "Examine file extensions carefully: watch out for double extensions (e.g., 'Invoice_Q3.pdf.exe' or 'Receipt.docx.vbs').",
                "High-risk file extensions include: .exe, .scr, .iso, .vbs, .js, .bat, and .hta.",
                "NEVER click 'Enable Content' or 'Enable Macros' on unexpected Microsoft Office documents.",
                "If someone sends an unexpected archive (.zip or .7z) with a password in the email body, it is designed to bypass security email scanners."
            ],
            "red_flags": [
                "An invoice sent as an executable file (.exe or .scr) or disk image (.iso).",
                "Documents prompting you to disable security controls to view protected content.",
                "Unsolicited resumes or order confirmations from companies you have never contacted."
            ],
            "pro_tip": "Real invoices are almost never delivered as .zip, .iso, or .exe files. If you see those extensions, report the message immediately.",
            "follow_ups": [
                "How do macro viruses work?",
                "What is phishing?",
                "What should I do if I opened a suspicious attachment?"
            ],
            "responses": [
                "Treat all unsolicited attachments with extreme skepticism. Watch for double extensions, never enable macros, and never open .exe or .iso files sent via email."
            ]
        },
        {
            "tag": "social_engineering",
            "patterns": [
                "What is social engineering?", "Social engineering tactics", "What is pretexting?",
                "What is baiting?", "What is shoulder surfing?", "How do attackers manipulate people?",
                "Psychology of cyber attacks", "Human factor in cybersecurity"
            ],
            "summary": "Social engineering is the psychological manipulation of people into performing actions or divulging confidential information, bypassing technical security controls.",
            "action_steps": [
                "Recognize the 5 emotional triggers attackers use: 1) Urgency, 2) Fear/Intimidation, 3) Authority, 4) Curiosity/Greed, and 5) Sympathy/Helpfulness.",
                "Slow down: Legitimate emergencies will never be jeopardized by a 2-minute independent verification.",
                "Be willing to challenge authority politely when standard security policies are at stake.",
                "Never plug in random USB drives found in parking lots, hallways, or lobbies (Baiting)."
            ],
            "red_flags": [
                "Someone rushing you: 'We will lose this client if you don't send the files in 5 minutes!'.",
                "Unfamiliar technicians asking you to disable your antivirus or read them your password.",
                "Strangers asking you to hold open secure doors (Tailgating)."
            ],
            "pro_tip": "Attackers hack humans because humans are easier to exploit than 256-bit AES encryption. When an email or call induces sudden anxiety, that emotion is your warning alarm.",
            "follow_ups": [
                "What is spear phishing?",
                "What is tailgating in physical security?",
                "What is baiting?"
            ],
            "responses": [
                "Social engineering targets human psychology—urgency, fear, and authority. Always pause, verify unexpected requests independently, and never let emotion override security policy."
            ]
        },
        {
            "tag": "clean_desk_and_physical_security",
            "patterns": [
                "What is clean desk policy?", "Physical security tips", "Locking my computer screen",
                "What is tailgating?", "Shoulder surfing prevention", "Leaving laptop unattended",
                "Office security awareness", "Protecting physical documents"
            ],
            "summary": "Physical security protects hardware, paper records, and workspaces from unauthorized access. A clean desk policy ensures sensitive information is not exposed to passersby, visitors, or cleaners.",
            "action_steps": [
                "Always lock your screen (Windows Key + L or Mac Ctrl + Cmd + Q) every single time you step away from your desk.",
                "Never leave company laptops, access badges, or sensitive client files visible in parked cars or unattended conference rooms.",
                "Do not allow 'Tailgating': ensure every person swipes their own security badge at building access doors.",
                "Shred sensitive physical documents using cross-cut shredders rather than throwing them into standard recycling bins."
            ],
            "red_flags": [
                "Sticky notes containing passwords stuck to monitors or under keyboards.",
                "Unknown individuals wandering corporate corridors without visitor badges.",
                "Printed confidential payroll or HR documents left unattended on shared printers."
            ],
            "pro_tip": "Make locking your workstation a physical reflex: fingers on 'Win+L' whenever your feet leave your chair.",
            "follow_ups": [
                "What is shoulder surfing?",
                "How to protect my laptop during travel?",
                "What is a BadUSB?"
            ],
            "responses": [
                "Digital safety requires physical vigilance. Lock your workstation every time you step away (Win+L), safeguard access badges, shred sensitive paperwork, and prevent unauthorized tailgating."
            ]
        },
        {
            "tag": "usb_security_and_juice_jacking",
            "patterns": [
                "Are USB drives safe?", "What is a BadUSB?", "Found a random USB drive",
                "What is juice jacking?", "Public phone charging stations risk", "USB data blocker",
                "Can USBs spread viruses?", "Plugging in unknown flash drive"
            ],
            "summary": "USB flash drives can carry malware or hardware exploits (BadUSB) that disguise themselves as keyboards and execute malicious command-line payloads within seconds. Public USB charging ports can also be modified to steal data ('Juice Jacking').",
            "action_steps": [
                "NEVER plug an unknown or unverified USB drive into your computer—give it directly to IT security.",
                "Use your own AC wall charger or an external power bank rather than public USB charging kiosks in airports.",
                "If you must charge from public USB ports, use a 'USB Data Blocker' (a hardware adapter that physically disconnects data pins).",
                "Organizations should enforce USB device control policies to restrict unauthorized removable media."
            ],
            "red_flags": [
                "Promotional USB drives handed out by unknown vendors or left in public lobbies.",
                "Phones prompting 'Trust this computer?' when plugged into a public charging station."
            ],
            "pro_tip": "A BadUSB does not look like a virus to your computer; it registers as an ultra-fast keyboard typing malicious PowerShell commands at 1,000 words per minute.",
            "follow_ups": [
                "What is physical security?",
                "How does malware spread?",
                "What is clean desk policy?"
            ],
            "responses": [
                "Never plug in unknown USB flash drives—they can execute malicious code in seconds. For public charging, use standard AC wall outlets or a hardware USB data blocker."
            ]
        },
        {
            "tag": "remote_work_and_home_wifi",
            "patterns": [
                "Remote work security tips", "How to secure home Wi-Fi?", "Work from home security",
                "Changing router password", "IoT device security", "Securing home office",
                "Safe telecommuting", "Home network safety"
            ],
            "summary": "Working from home expands the corporate security perimeter to your home network. Vulnerable routers, default credentials, and smart IoT devices can become attack footholds.",
            "action_steps": [
                "Change default router credentials (both the admin password and the Wi-Fi WPA3/WPA2 passphrase).",
                "Create a separate Guest Wi-Fi network for smart home gadgets (IoT cameras, smart bulbs, smart TVs) to isolate them from work devices.",
                "Keep work data strictly on company-issued devices; avoid forwarding work emails to personal email accounts.",
                "Ensure your home router's firmware is updated and remote management features are turned off."
            ],
            "pro_tip": "Putting your smart home appliances and IoT devices on a dedicated Guest Wi-Fi network prevents a hacked smart lightbulb from compromising your work laptop.",
            "follow_ups": [
                "Is public Wi-Fi safe?",
                "How to protect against malware?",
                "What is clean desk policy?"
            ],
            "responses": [
                "Secure your remote workplace: Change default router passwords, isolate smart IoT gadgets on a guest Wi-Fi network, and conduct all business solely on managed corporate devices."
            ]
        },
        {
            "tag": "mobile_security",
            "patterns": [
                "Mobile phone security", "Smartphone safety tips", "Is my phone hacked?",
                "App permissions security", "What is sideloading?", "Lost or stolen phone security",
                "Android security tips", "iPhone security tips"
            ],
            "summary": "Smartphones hold immense amounts of personal, biometric, and corporate data. Protecting them requires minimal app permissions, verified app stores, and remote wipe capabilities.",
            "action_steps": [
                "Install apps only from official stores (Apple App Store, Google Play); avoid sideloading APK files from third-party websites.",
                "Review app permissions regularly: Revoke access to microphone, camera, contacts, and precise location for apps that do not need them.",
                "Enable 'Find My Device' / 'Find My iPhone' with remote wipe enabled in case of theft.",
                "Set a strong 6-digit PIN or passphrase (avoid 1234 or 0000) combined with biometric face or fingerprint lock."
            ],
            "red_flags": [
                "Battery draining rapidly or phone overheating when idle (a symptom of background spyware).",
                "Unexplained spikes in mobile data consumption.",
                "Strange pop-up windows appearing across your home screen."
            ],
            "pro_tip": "Rebooting your smartphone once a day flushes many zero-click, in-memory spyware implants that do not possess persistent boot storage.",
            "follow_ups": [
                "What is smishing?",
                "What is juice jacking?",
                "How does MFA protect mobile accounts?"
            ],
            "responses": [
                "Keep mobile devices protected: Use strong PINs, review app permissions, only install from official app stores, and enable remote locate/wipe capabilities."
            ]
        },
        {
            "tag": "incident_response_immediate",
            "patterns": [
                "I clicked a suspicious link", "What should I do if I entered my password?",
                "I think I got hacked", "Emergency cybersecurity help", "I got phished what to do?",
                "Accidentally opened a bad attachment", "Compromised account help", "I made a mistake clicked link",
                "Security incident steps", "How to report an incident"
            ],
            "summary": "Immediate action can prevent a minor error from escalating into a full organizational breach. Don't panic, don't hide the mistake, and act quickly.",
            "action_steps": [
                "1. DISCONNECT IMMEDIATELY: Unplug the network cable (Ethernet) or turn off Wi-Fi on the affected device to halt malware transmission.",
                "2. CHANGE PASSWORDS (from a DIFFERENT, uncompromised device): Change the password for the affected account and terminate all other active sessions.",
                "3. REPORT TO IT / SECURITY: Contact your organization's IT Helpdesk or Security Operations Center (SOC) immediately. Quick reporting is valued, not punished.",
                "4. DO NOT DELETE EVIDENCE: Keep the phishing email, headers, and transaction timestamps so analysts can block the threat across the company.",
                "5. CONTACT YOUR BANK: If financial data or debit/credit cards were entered, notify the bank immediately to freeze the card."
            ],
            "red_flags": [
                "Attempting to cover up the mistake or delay reporting—delays allow attackers time to establish persistence and steal data."
            ],
            "pro_tip": "Security teams deal with clicked links every single day. The faster you report it, the faster they can contain the impact and protect your colleagues.",
            "follow_ups": [
                "How do I recognize a phishing email?",
                "What is ransomware?",
                "How do I revoke active sessions?"
            ],
            "responses": [
                "Immediate steps: Disconnect the device from Wi-Fi/Ethernet, change your passwords from a clean device, report the incident to IT security right away, and preserve the suspicious message for evidence."
            ]
        },
        {
            "tag": "cloud_and_account_takeover",
            "patterns": [
                "Signs my account is hacked", "How to revoke active sessions?", "Account takeover recovery",
                "Hacked Google account", "Hacked Microsoft account", "Someone logged into my account",
                "Unauthorized login detected", "Recover compromised account"
            ],
            "summary": "Account takeover occurs when an unauthorized user gains access to your cloud account. Prompt session revocation and recovery audits are vital.",
            "action_steps": [
                "Go to your account's Security settings and click 'Log out of all other sessions' / 'Revoke active devices'.",
                "Change your account password to a new, unique 16+ character passphrase.",
                "Audit your account's Recovery email address and Recovery phone number to verify the attacker did not change them to their own.",
                "Check for malicious email forwarding rules (attackers frequently configure silent inbox rules to forward your sensitive emails to themselves).",
                "Enable an Authenticator App or Passkey for MFA."
            ],
            "red_flags": [
                "Sent emails or direct messages that you never wrote.",
                "Notifications of password resets or sign-ins originating from foreign countries or unfamiliar devices.",
                "New mailbox rules that automatically redirect incoming emails to the Trash or RSS folder."
            ],
            "pro_tip": "Always check your email forwarding rules after an account scare; sneaky forwarding rules are how attackers maintain quiet access even after password changes.",
            "follow_ups": [
                "What is multi-factor authentication?",
                "What is credential stuffing?",
                "How to create a strong password?"
            ],
            "responses": [
                "To reclaim a compromised account: Revoke all active sessions, change your password immediately, verify recovery details, check for hidden email forwarding rules, and enable MFA."
            ]
        },
        {
            "tag": "identity_theft_and_data_breaches",
            "patterns": [
                "What is a data breach?", "Was my email breached?", "What is Have I Been Pwned?",
                "Identity theft protection", "What to do after a data breach?", "Credit freeze explained",
                "How to protect my identity?", "Someone stole my identity"
            ],
            "summary": "Data breaches occur when corporate databases containing customer credentials or personal identifiable information (PII) are stolen or leaked online.",
            "action_steps": [
                "Check HaveIBeenPwned.com to see if your email address or passwords have appeared in public data breaches.",
                "Place a FREE Credit Freeze with the three major credit bureaus (Equifax, Experian, TransUnion) to prevent criminals from opening unauthorized loans in your name.",
                "Change any passwords that match the leaked credentials immediately across all accounts.",
                "Set up transaction alerts on bank accounts and credit cards to detect fraudulent charges instantly."
            ],
            "pro_tip": "A credit freeze is free by law, takes 10 minutes to set up, and is the single most effective barrier against identity theft.",
            "follow_ups": [
                "What is credential stuffing?",
                "Why is password reuse bad?",
                "How to spot phishing?"
            ],
            "responses": [
                "After a breach: Check your exposure on HaveIBeenPwned, change exposed passwords, turn on MFA, and place a free credit freeze across major credit reporting bureaus."
            ]
        },
        {
            "tag": "insider_threat_and_shadow_it",
            "patterns": [
                "What is shadow IT?", "What is an insider threat?", "Using unauthorized software at work",
                "Sending work files to personal email", "Using personal Dropbox for company files",
                "Company data policy", "Accidental data leak prevention"
            ],
            "summary": "Shadow IT is the use of unapproved hardware, cloud services, or software without the knowledge or approval of corporate IT. Insider threats stem from employees or contractors who misuse or accidentally leak internal data.",
            "action_steps": [
                "Never forward confidential company spreadsheets, code, or client lists to personal email or personal cloud storage.",
                "Request approval from IT before using new AI tools, software apps, or collaboration platforms.",
                "Understand that personal services lack enterprise security controls, DLP monitoring, and data retention compliance.",
                "Report inadvertent data leaks to IT security immediately so they can be contained."
            ],
            "red_flags": [
                "Pasting proprietary company source code, financial roadmaps, or customer PII into public AI tools.",
                "Sharing company Google Drive or OneDrive links configured with 'Anyone with the link can edit'."
            ],
            "pro_tip": "Most insider data breaches are not malicious sabotage—they are well-meaning employees trying to work faster using unvetted personal tools.",
            "follow_ups": [
                "What is clean desk policy?",
                "How to protect company data?",
                "What is social engineering?"
            ],
            "responses": [
                "Avoid Shadow IT by using only authorized company tools for business data. Never forward company assets to personal accounts or unvetted cloud storage."
            ]
        },
        {
            "tag": "quiz_request",
            "patterns": [
                "Start a quiz", "Take a quiz", "Quiz me", "Cybersecurity quiz", "Test my knowledge",
                "Give me a test", "Practice questions", "Cyber test", "Quiz", "Ask me a question"
            ],
            "summary": "Interactive Cybersecurity Awareness Quiz Mode.",
            "action_steps": [
                "Answer the multiple-choice scenario questions to test your practical security instincts.",
                "Type the letter (A, B, C, or D) corresponding to your answer.",
                "Receive instant explanations and best practices."
            ],
            "pro_tip": "Frequent micro-quizzing increases security retention by over 70% compared to once-a-year compliance videos.",
            "follow_ups": [
                "Analyze a suspicious email",
                "What is phishing?",
                "Emergency response steps"
            ],
            "responses": [
                "Let's test your cybersecurity instincts! Here is your scenario question:\n\n**Scenario**: You receive an email from 'IT Support <helpdesk@company-internal-portal.net>' stating your mailbox is full and you must click a link within 2 hours or your account will be deleted.\n\n**What should you do?**\n- **A)** Click the link and enter your credentials to clean your mailbox.\n- **B)** Forward the email to your personal account to test the link safely.\n- **C)** Ignore the email and delete it without telling anyone.\n- **D)** Check the sender's domain, do not click the link, and report it to your official IT security channel.\n\n*Reply with A, B, C, or D!*"
            ]
        },
        {
            "tag": "phishing_analyzer_trigger",
            "patterns": [
                "Analyze this email", "Check this message", "Is this email phishing?",
                "Check this link", "Is this suspicious?", "Analyze email snippet",
                "Can you check a text for me?", "Evaluate this email", "Phishing inspection"
            ],
            "summary": "CyberBot Phishing Inspection Engine.",
            "action_steps": [
                "Paste the text, subject line, or sender address of the suspicious email or message directly into the chat.",
                "CyberBot will inspect it for artificial urgency, impersonation cues, credential harvesting keywords, and domain inconsistencies.",
                "You will receive a Risk Rating (Low, Medium, High, or Critical) with specific red flags."
            ],
            "pro_tip": "Never paste real passwords, API tokens, or credit card numbers into any inspection tool.",
            "follow_ups": [
                "Start a quiz",
                "What are phishing red flags?",
                "What to do if I clicked a bad link?"
            ],
            "responses": [
                "I can analyze suspicious messages! Please paste the email subject, sender address, and body text below (e.g., 'Analyze this: From: support@bank-alert.com, Urgent: Account suspended, click here...'). I'll evaluate the red flags and provide a threat assessment."
            ]
        },
        {
            "tag": "goodbye",
            "patterns": [
                "Bye", "Goodbye", "See you later", "Exit", "Quit", "Cya", "Farewell", "Have a good day"
            ],
            "summary": "Session completion.",
            "action_steps": [
                "Stay safe and remember: When in doubt, verify out-of-band!"
            ],
            "pro_tip": "Stay alert, keep software updated, and verify before you click.",
            "follow_ups": [
                "Start a new chat",
                "Take a quick quiz"
            ],
            "responses": [
                "Stay safe out there! Remember: think twice before you click, and always verify unexpected requests. Goodbye!",
                "Goodbye! Keep your software updated and your passwords strong. See you next time!"
            ]
        },
        {
            "tag": "gratitude",
            "patterns": [
                "Thank you", "Thanks", "Thanks a lot", "Very helpful", "Appreciate it",
                "Good bot", "Awesome", "Great explanation", "Thanks CyberBot"
            ],
            "summary": "User appreciation.",
            "action_steps": [
                "Share these security practices with your team and colleagues."
            ],
            "pro_tip": "A culture of security thrives when everyone helps each other stay safe.",
            "follow_ups": [
                "Take a cybersecurity quiz",
                "How to spot phishing?"
            ],
            "responses": [
                "You're very welcome! Security is a team effort—feel free to ask whenever you encounter anything suspicious.",
                "Happy to help! Keep practicing strong digital habits, and stay safe online!"
            ]
        }
    ],
    "quiz_questions": [
        {
            "id": 1,
            "scenario": "You receive an email from 'IT Support <helpdesk@company-internal-portal.net>' stating your mailbox is full and you must click a link within 2 hours or your account will be deleted.",
            "options": {
                "A": "Click the link and enter your credentials to clean your mailbox.",
                "B": "Forward the email to your personal account to test the link safely.",
                "C": "Ignore the email and delete it without telling anyone.",
                "D": "Check the sender's domain, do not click the link, and report it to your official IT security channel."
            },
            "correct_answer": "D",
            "explanation": "Option D is correct! Legitimate IT departments do not threaten immediate account deletion with tight countdowns. The domain 'company-internal-portal.net' is suspicious, and reporting it protects other employees from being tricked."
        },
        {
            "id": 2,
            "scenario": "While at an airport terminal, you find a brand-new 64GB USB flash drive lying on a seat with a label that says 'Executive Payroll Q4'. What should you do?",
            "options": {
                "A": "Plug it into your laptop to find the owner's contact information.",
                "B": "Format the USB drive immediately so you can use it for your own files.",
                "C": "Do not plug it into any device; hand it to airport security or company IT.",
                "D": "Plug it in, but open files only in Notepad so malware cannot execute."
            },
            "correct_answer": "C",
            "explanation": "Option C is correct! This is a classic 'Baiting' attack. Flash drives can execute hardware keystroke injection payloads (BadUSB) the moment they are inserted. Never plug in unknown media."
        },
        {
            "id": 3,
            "scenario": "You receive a phone call from someone claiming to be from your bank's fraud department. They say: 'There is a $1,200 charge on your card right now. We just sent a 6-digit code to your phone. Read it to me to cancel the charge.' What should you do?",
            "options": {
                "A": "Read the code immediately to stop the fraudulent charge.",
                "B": "Hang up immediately, and call the bank using the number printed on the back of your card.",
                "C": "Ask the caller for their employee ID and then give them the code.",
                "D": "Text the code to them instead of speaking it."
            },
            "correct_answer": "B",
            "explanation": "Option B is correct! This is a Vishing scam. The attacker already has your password and is trying to trigger a real transaction or password reset; the code they want you to read is your two-factor verification code! Banks will NEVER ask you to read back a one-time code."
        },
        {
            "id": 4,
            "scenario": "Which of the following is considered the strongest and most secure password / passphrase?",
            "options": {
                "A": "P@ssw0rd2024!",
                "B": "JohnDoe#1985",
                "C": "sunset-blanket-guitar-whistle!",
                "D": "Tr0ub4dor&3"
            },
            "correct_answer": "C",
            "explanation": "Option C is correct! Passphrases made of 4+ random words have much higher entropy (length) than short words with common substitutions like '@' for 'a' or '0' for 'o', which modern cracking tools test in milliseconds."
        },
        {
            "id": 5,
            "scenario": "You are working remotely from a coffee shop on an unencrypted public Wi-Fi network. What is the safest way to connect to your work resources?",
            "options": {
                "A": "Browse only sites that have HTTPS and ignore any certificate warnings.",
                "B": "Connect through a trusted corporate VPN or use your phone's personal cellular hotspot.",
                "C": "Turn on Incognito / Private Browsing mode in your web browser.",
                "D": "Disconnect your antivirus software to speed up public Wi-Fi access."
            },
            "correct_answer": "B",
            "explanation": "Option B is correct! Incognito mode does NOT encrypt network traffic. A VPN or personal cellular hotspot ensures your data is encrypted against rogue access points and eavesdroppers."
        }
    ]
}

output_path = Path(__file__).resolve().parent / "cybersecurity.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(DATASET, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {output_path} with {len(DATASET['intents'])} intents and {len(DATASET['quiz_questions'])} quiz scenarios.")

