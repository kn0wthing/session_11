import streamlit as st
from pathlib import Path
from hindi_tokenizer import load_tokenizer, encode_text, decode_text

def load_hindi_tokenizer():
    """Load the trained Hindi BPE tokenizer"""
    output_dir = Path("output")
    config_path = output_dir / "hindi_encoder.json"
    
    if not config_path.exists():
        st.error("Error: Tokenizer configuration not found! Please train the tokenizer first.")
        st.stop()
    
    return load_tokenizer(str(config_path))

def main():
    st.set_page_config(
        page_title="Hindi BPE Tokenizer",
        page_icon="🇮🇳",
        layout="wide"
    )
    
    st.title("Hindi BPE Tokenizer")
    st.markdown("A web interface for encoding and decoding Hindi text using BPE tokenization")
    
    # Load tokenizer
    try:
        tokenizer = load_hindi_tokenizer()
    except Exception as e:
        st.error(f"Error loading tokenizer: {e}")
        st.stop()
    
    # Create two columns
    encode_col, decode_col = st.columns(2)
    
    # Encoding Section
    with encode_col:
        st.header("Encode Hindi Text")
        st.markdown("Convert Hindi text into token IDs")
        
        input_text = st.text_area(
            "Enter Hindi Text",
            placeholder="यहाँ हिंदी टेक्स्ट लिखें...",
            height=150,
            key="encode_input"
        )
        
        if st.button("Encode", key="encode_button"):
            if input_text.strip():
                try:
                    token_ids, tokens = encode_text(tokenizer, input_text)
                    
                    st.subheader("Results:")
                    st.markdown("**Tokens:**")
                    st.write(tokens)
                    
                    st.markdown("**Token IDs:**")
                    st.write(token_ids)
                    
                    # Display as comma-separated string for easy copying
                    st.markdown("**Token IDs (comma-separated):**")
                    st.code(", ".join(map(str, token_ids)))
                    
                except Exception as e:
                    st.error(f"Error during encoding: {e}")
            else:
                st.warning("Please enter some text to encode")
    
    # Decoding Section
    with decode_col:
        st.header("Decode Token IDs")
        st.markdown("Convert token IDs back to Hindi text")
        
        input_ids = st.text_area(
            "Enter Token IDs (comma-separated)",
            placeholder="2517, 2074, 340, 4, 201...",
            height=150,
            key="decode_input"
        )
        
        if st.button("Decode", key="decode_button"):
            if input_ids.strip():
                try:
                    # Convert string of IDs to list of integers
                    token_ids = [int(id.strip()) for id in input_ids.split(",")]
                    
                    decoded_text = decode_text(tokenizer, token_ids)
                    
                    st.subheader("Results:")
                    st.markdown("**Decoded Text:**")
                    st.write(decoded_text)
                    
                    # Display in a box for better visibility
                    st.text_area(
                        "Decoded Text (copyable)",
                        value=decoded_text,
                        height=100,
                        key="decoded_output"
                    )
                    
                except ValueError:
                    st.error("Invalid input format. Please enter comma-separated numbers.")
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
            else:
                st.warning("Please enter token IDs to decode")
    
    # Add information section at the bottom
    st.markdown("---")
    st.markdown("### About the Tokenizer")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        **Tokenizer Details:**
        - Type: Byte Pair Encoding (BPE)
        - Vocabulary Size: 4,500 tokens
        - Special Tokens: `<pad>`, `<unk>`, `<s>`, `</s>`
        - Minimum Token Frequency: 2
        """)
    
    with info_col2:
        st.markdown("""
        **Preprocessing:**
        - Retains Hindi Unicode (\\u0900-\\u097F)
        - Removes digits and special characters
        - Normalizes punctuation
        - Cleans whitespace
        """)

if __name__ == "__main__":
    main() 