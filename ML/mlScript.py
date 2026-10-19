import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

DATASET_PATH = Path(__file__).resolve().parents[1] / "dataset" / "cybersecurity.json"
MIN_CONFIDENCE = 0.3

with DATASET_PATH.open(encoding="utf-8") as dataset_file:
    intents_data = json.load(dataset_file)

patterns = []
labels = []
for intent in intents_data["intents"]:
    tag = (
        "reporting_incidents"
        if intent["tag"] == "reporting_incident"
        else intent["tag"]
    )
    patterns.extend(intent["patterns"])
    labels.extend([tag] * len(intent["patterns"]))

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode", sublinear_tf=True),
    MultinomialNB(alpha=0.2),
)
model.fit(patterns, labels)

TOPIC_RESPONSES = {
    "greeting": "Hi! I can help with practical cybersecurity topics such as phishing, malware, passwords, account security, and safe browsing. What would you like to know?",
    "phishing": "Phishing messages impersonate a trusted person or service to steal information or get you to open a harmful link or file. Check the sender and destination carefully, and verify unexpected requests through a separate, trusted channel. Do not reply, open attachments, or enter credentials from the message. Report it using your email provider's phishing controls or your organization's IT team. If you already entered a password, change it from the official site and sign out other sessions.",
    "malware": "Malware is software intended to damage a device, spy on activity, or steal data; viruses, ransomware, spyware, and trojans are examples. Keep your operating system and apps updated, use reputable built-in or managed security protection, and install software only from trusted sources. If you suspect an infection, avoid entering passwords on that device and contact your IT/security support; follow their advice before disconnecting or wiping it.",
    "password_security": "Use a unique, long password or passphrase for every account; a password manager can generate and store them. Turn on multi-factor authentication, especially for email, financial, and administrator accounts. Avoid reusing passwords. Change one promptly if it may have been exposed, and use the service's official recovery page if you cannot sign in.",
    "two_factor_auth": "Multi-factor authentication (MFA), often called two-factor authentication (2FA), asks for an additional proof of identity beyond your password. Prefer a passkey or hardware security key where supported, then an authenticator app; text-message codes are better than no MFA but can be vulnerable to number-porting attacks. Never share a sign-in code with someone who contacts you.",
    "public_wifi": "Public Wi-Fi is not automatically unsafe, but networks can be untrusted. Use HTTPS sites and current software, turn off automatic joining and file sharing, and avoid sensitive activity if you cannot verify the connection. A reputable VPN can protect traffic between your device and the VPN provider, but it does not make phishing sites safe or replace HTTPS.",
    "data_encryption": "Encryption transforms readable data into ciphertext that should be unusable without the appropriate key. It helps protect data on a device or while it travels over a network, but security also depends on strong keys, correct implementation, and protecting the device and account. Use built-in full-disk encryption and secure connections where available, and keep recovery keys private and backed up safely.",
    "social_engineering": "Social engineering is manipulation designed to make someone reveal information, send money, or take an unsafe action. Watch for urgency, secrecy, unexpected attachments, and requests to bypass normal procedures. Verify the person or request using a known phone number or separate channel, and never share passwords or one-time sign-in codes.",
    "software_updates": "Install operating-system, browser, and application updates from their built-in updater or the vendor's official source. Updates often fix security vulnerabilities attackers could exploit. Enable automatic updates where practical, restart when needed to finish them, and avoid update links in unsolicited messages.",
    "reporting_incidents": "If you suspect a security incident, contact your organization's IT/security team promptly if you have one. For a personal account, use the provider's official support and recovery pages; contact your bank through the number on your card if money or payment details may be involved. Preserve relevant messages and times, avoid deleting evidence, and do not share sensitive details publicly.",
    "risk_response": "If an account may be compromised, use a trusted device to change its password, revoke other active sessions, enable MFA, and check recovery details and recent activity. If payment details or work systems are involved, contact the bank or your IT/security team promptly. If a device may be infected, stop using it for sensitive sign-ins and ask qualified support what to do before disconnecting, resetting, or deleting files.",
    "safe_browsing": "For safer browsing, check that a site address is the one you intended before signing in, keep your browser updated, and download files only from trusted sources. HTTPS encrypts a connection but does not prove a site is honest. Use unique passwords and MFA, review site permissions, and avoid unexpected pop-ups or download prompts.",
}


def get_intent(message):
    probabilities = model.predict_proba([message])[0]
    best_index = probabilities.argmax()
    if probabilities[best_index] < MIN_CONFIDENCE:
        return None
    return model.classes_[best_index]


class Model:
    @staticmethod
    def respond(message):
        if not isinstance(message, str) or not message.strip():
            return "Type a question about cybersecurity to get started."

        intent = get_intent(message.strip())
        if intent is None:
            return "I’m not confident I understood that. I can help with phishing, malware, passwords, MFA, public Wi-Fi, encryption, social engineering, updates, incident response, and safe browsing. Try asking about one of those topics."

        return TOPIC_RESPONSES[intent]


# print("Bot: Hi there! Ask me something about the cyber security.")
# while True:
#     user_input = input("You: ")
#     print("Bot:", respond(user_input))
