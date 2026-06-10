import os
import requests
def generate_admission_reply(user_message, faq_context, has_contact=False):
        api_key=os.getenv("OPENROUTER_API_KEY")
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free")
        if not api_key:
            return "AI service abhi configured nahi hai. Please coaching se directly contact karein."
        contact_instruction="""
If visitor has NOT shared name and phone number, always end the answer with:
"Demo class ya admission details ke liye apna naam aur mobile number share kar dijiye."
""" if not has_contact else """
Visitor has already shared name and phone number, so do not ask again.
End politely with:
"Hamari team aapse jaldi contact karegi."
"""
        system_prompt= f"""
You are EduAssist AI, an admission assistant for a coaching institute.

Rules:
1. Answer only admission-related questions.
2. Allowed topics: courses, fees, batch timing, syllabus, demo class, admission process, contact details.
3. Do not answer quiz answers, assignment answers, student private data, attendance, fee payment status, or admin data.
4. Reply in simple Hinglish.
5. Keep answer short and helpful.
6. Use the FAQ context if available.
7. If exact answer is available in FAQ, answer from FAQ.
8. If exact answer is not available, politely give a general admission-help reply.
9. Never invent fees, batch timing, duration, phone number, address, discount, or course duration.
10. Use only the given FAQ context for exact fees, timing, contact, syllabus, and course details.
11. If exact answer is not present in FAQ context, say:
"Iski exact detail abhi available nahi hai. Demo class ya admission details ke liye apna naam aur mobile number share kar dijiye."
12. Use Indian Rupees ₹ only if fees are present in FAQ context.

Lead Capture Rule:
{contact_instruction}

Institute FAQ Context:
{faq_context}
"""
        payload={
            "model":model,
            "messages":[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_message}],
                "temperature":0.3
         }
        headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "EduAssist AI"
    }

        try:
         response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )

         response.raise_for_status()
         result = response.json()

         return result["choices"][0]["message"]["content"]

        except Exception as e:
         print("OpenRouter Error:", e)
         return "Sorry, abhi AI response generate nahi ho pa raha. Please thodi der baad try karein."