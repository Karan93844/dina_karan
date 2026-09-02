import io, streamlit as st
from huggingface_hub import InferenceClient
client = InferenceClient(
        model="meta-llama/Meta-Llama-3-8B-Instruct", 
        token=st.secrets.get("HF_TOKEN")
    )
    col_text, col_img = st.columns(2)
    
    with col_text, st.spinner("Writing..."):
        prompt_t = f"Short heartfelt birthday wish from {wisher} to {receiver}. Detail: {needs}. No placeholders."
        # Call chat.completions without repeating the model name inside it
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_t}], 
            max_tokens=150
        )
        st.info(res.choices.message.content)
st.title("🎂 Mini Cartoon Wisher")
wisher = st.text_input("Your Name", "Dina")
receiver = st.text_input("Birthday Person", "Indira S")
needs = st.text_input("Their Needs/Traits", "loves Dark chocolates,kind hearted")

st.audio("https://soundhelix.com", loop=True)

if st.button("Generate ✨"):
    c1, c2 = st.columns(2)
    c1.image(f"https://dicebear.com{wisher}", caption=wisher)
    c2.image(f"https://dicebear.com{receiver}", caption=f"{receiver} 🎉")
    
    client = InferenceClient(token=st.secrets.get("HF_TOKEN"))
    col_text, col_img = st.columns(2)
    
    with col_text, st.spinner("Writing..."):
        prompt_t = f"Short heartfelt birthday wish from {wisher} to {receiver}. Detail: {needs}. No placeholders."
        res = client.chat.completions.create(model="meta-llama/Meta-Llama-3-8B-Instruct", messages=[{"role": "user", "content": prompt_t}], max_tokens=150)
        st.info(res.choices.message.content)
            
    with col_img, st.spinner("Baking card..."):
        try:
            prompt_i = f"3D cartoon birthday celebration for {receiver}, {needs}, pastel colors, digital art."
            gen_img = client.text_to_image(prompt_i, model="black-forest-labs/FLUX.1-schnell")
            st.image(gen_img, caption="Custom Card 🎁")
            
            buf = io.BytesIO()
            gen_img.save(buf, format="PNG")
            st.download_button("Download Card 💾", data=buf.getvalue(), file_name=f"card_{receiver}.png", mime="image/png")
        except:
            st.error("Image generation limit hit.")
