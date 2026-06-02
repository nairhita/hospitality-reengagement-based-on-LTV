import os
from openai import OpenAI

class LLMCopywriter:
    def __init__(self):
        # Pulls the API key from environment variable if available
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_reengagement_email(self, guest_id: str, cltv: float, last_amenity: str) -> str:
        """Drafts a targeted re-engagement email leveraging stay metadata."""
        prompt = (
            f"Write a luxury, warm re-engagement marketing email for a VIP hotel guest ({guest_id}).\n"
            f"Their projected Customer Lifetime Value score is ${cltv:,.2f}.\n"
            f"They haven't stayed with us recently, but historically their favorite part of our resort "
            f"was the {last_amenity}.\n"
            f"Offer them a complimentary premium perk tailored around their preference to incentivize a new booking. "
            f"Keep it concise, exclusive, and compelling. Do not use generic placeholders."
        )

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an elite concierge copywriter for a 5-star hospitality brand."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"[API Error - Falling back to template]: Welcome back! Enjoy an exclusive credit toward your next stay featuring {last_amenity}."
        else:
            # Clean, production-ready localized template fallback
            return (
                f"Subject: We Miss You at the Resort – An Exclusive Invitation for {guest_id}\n\n"
                f"Dear Valued Guest,\n\n"
                f"It has been far too long since your last stay with us. As one of our most distinguished guests, "
                f"we wanted to extend an exclusive invitation to welcome you back.\n\n"
                f"On your next visit, we would delight in treating you to a complimentary experience at our "
                f"world-class {last_amenity}—crafted specifically around what you love most about our properties.\n\n"
                f"Warmest regards,\nThe Guest Relations Team"
            )
