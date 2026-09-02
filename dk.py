import io
import streamlit as st
from huggingface_hub import InferenceClient

st.title("🎂 Mini Cartoon Wisher")
wisher = st.text_input("Your Name", "Dina")
receiver = st.text_input("Birthday Person", "Indira S")
needs = st.text_input("Their Needs/Traits", "loves Dark chocolates,kind hearted")

# Note: Added a working audio stream link for SoundHelix
st.audio("https://soundhelix.com", loop=True)

if st.button("Generate ✨"):
    c1, c2 = st.columns(2)
    # Fixed: DiceBear requires a specific style path and format parameter
    c1.image(f"https://dicebear.com{wisher}", caption=wisher)
    c2.image(f"https://dicebear.com{receiver}", caption=f"{receiver} 🎉")
    
      client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=st.secrets.get("HF_TOKEN"))
    col_text, col_img = st.columns(2)
    
    with col_text, st.spinner("Writing..."):
        prompt_t = f"Short heartfelt birthday wish from {wisher} to {receiver}. Detail: {needs}. No placeholders."
        
        # Use simpler text generation layout to avoid strict chat template validation
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_t}], 
                max_tokens=150
            )
            st.info(res.choices[0].message.content)
        except Exception as text_err:
            st.error(f"Text generation issue: {text_err}")
    
    # Text Generation Client
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=st.secrets.get("HF_TOKEN"))
    col_text, col_img = st.columns(2)
    
    with col_text, st.spinner("Writing..."):
        prompt_t = f"Short heartfelt birthday wish from {wisher} to {receiver}. Detail: {needs}. No placeholders."
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt_t}], max_tokens=150)
        st.info(res.choices.message.content)
            
    with col_img, st.spinner("Baking card..."):
        try:
            # Fixed: Model path must be assigned directly inside the client initialization
            img_client = InferenceClient(model="black-forest-labs/FLUX.1-schnell", token=st.secrets.get("HF_TOKEN"))
            prompt_i = f"3D cartoon birthday celebration for {receiver}, {needs}, pastel colors, digital art."
            
            # Fixed: Call text_to_image without a model parameter here
            gen_img = img_client.text_to_image(prompt_i)
            st.image(gen_img, caption="Custom Card 🎁")
            
            buf = io.BytesIO()
            gen_img.save(buf, format="PNG")
            st.download_button("Download Card 💾", data=buf.getvalue(), file_name=f"card_{receiver}.png", mime="image/png")
        except Exception as e:
            # Helpful tip: printing 'e' in terminal helps you see if it's a token or rate limit error
            print(f"Error details: {e}")
            st.error("Image generation failed or limit hit.")
