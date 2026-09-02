import io, streamlit as st
from huggingface_hub import InferenceClient

st.title("🎂 Mini Cartoon Wisher")
wisher = st.text_input("Your Name", "Dina")
receiver = st.text_input("Birthday Person", "Indira S")
needs = st.text_input("Their Needs/Traits", "loves Dark chocolates,kind hearted")

st.audio("https://soundhelix.com", loop=True)

if st.button("Generate ✨"):
    c1, c2 = st.columns(2)
    c1.image(f"https://dicebear.com{wisher}", caption=wisher)
    c2.image(f"https://dicebear.com{receiver}", caption=f"{receiver} 🎉")
    
    # Secure token retrieval
    hf_token = st.secrets.get("HF_TOKEN")
    
    col_text, col_img = st.columns(2)
    
    # 1. Text Generation Block
    with col_text, st.spinner("Writing..."):
        try:
            # Using direct client initialization for the text model
            client_text = InferenceClient(token=hf_token)
            prompt_t = f"Short heartfelt birthday wish from {wisher} to {receiver}. Detail: {needs}. No placeholders."
            res = client_text.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct", 
                messages=[{"role": "user", "content": prompt_t}], 
                max_tokens=150
            )
            st.info(res.choices.message.content)
        except Exception as e:
            st.error(f"Text Generation Error: {str(e)}")
            
    # 2. Image Generation Block
    with col_img, st.spinner("Baking card..."):
        try:
            client_img = InferenceClient(token=hf_token)
            prompt_i = f"3D cartoon birthday celebration for {receiver}, {needs}, pastel colors, digital art."
            gen_img = client_img.text_to_image(prompt_i, model="black-forest-labs/FLUX.1-schnell")
            st.image(gen_img, caption="Custom Card 🎁")
            
            buf = io.BytesIO()
            gen_img.save(buf, format="PNG")
            st.download_button("Download Card 💾", data=buf.getvalue(), file_name=f"card_{receiver}.png", mime="image/png")
        except Exception as e:
            st.error("Image generation limit hit or token error.")
