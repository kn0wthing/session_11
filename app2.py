import streamlit as st
from pathlib import Path
from original import load_tokenizer, encode_text, decode_text
import random
import colorsys

def generate_distinct_colors(n):
    """Generate n visually distinct colors"""
    colors = []
    for i in range(n):
        hue = (i * 0.618033988749895) % 1
        # Lighter pastel colors
        saturation = 0.15
        value = 0.99
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors.append(color)
    return colors

def main():
    st.set_page_config(
        page_title="Hindi BPE Tokenizer",
        page_icon="🔤",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
        }
        .main {
            max-width: 1200px;
            padding: 2rem;
        }
        .text-input {
            background-color: #f7f7f8;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 1.5rem;
            font-size: 1.2em;
            min-height: 150px;
            font-family: 'Arial', sans-serif;
        }
        .token-stats {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .token-display {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 2rem;
            line-height: 2.2;
            font-size: 1.2em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .token {
            padding: 0.3em 0.5em;
            border-radius: 6px;
            margin: 0 2px;
            display: inline-block;
            transition: transform 0.1s ease;
        }
        .token:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .clear-button {
            background-color: #f1f3f4;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        .clear-button:hover {
            background-color: #e8eaed;
        }
        .stats-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #1e88e5;
        }
        .stats-label {
            font-size: 1.1em;
            color: #666;
            margin-top: 0.5rem;
        }
        .token-mapping {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin-top: 1.5rem;
            font-family: monospace;
            font-size: 1.1em;
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Load tokenizer
    try:
        output_dir = Path("output")
        config_path = output_dir / "hindi_encoder.json"
        if not config_path.exists():
            st.error("Tokenizer configuration not found! Please train the tokenizer first.")
            st.stop()
        tokenizer = load_tokenizer(str(config_path))
    except Exception as e:
        st.error(f"Error loading tokenizer: {e}")
        st.stop()

    # Create tabs for encode/decode
    encode_tab, decode_tab = st.tabs(["🔤 Encode", "📝 Decode"])

    with encode_tab:
        text = st.text_area(
            "Enter Hindi Text",
            value="",
            height=150,
            key="encode_input",
            help="Type or paste Hindi text here to see its tokenization"
        )

        if st.button("Clear", key="clear_encode", type="secondary"):
            st.session_state.encode_input = ""
            st.experimental_rerun()

        if text:
            # Get tokens
            token_ids, tokens = encode_text(tokenizer, text)
            
            # Display token and character counts
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="stats-number">{len(tokens)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="stats-label">Tokens</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="stats-number">{len(text)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="stats-label">Characters</div>', unsafe_allow_html=True)
            
            # Generate colors for tokens
            colors = generate_distinct_colors(len(tokens))
            
            # Display colored tokens
            html_tokens = []
            for token, token_id, color in zip(tokens, token_ids, colors):
                html_tokens.append(
                    f'<span class="token" style="background-color: {color};" '
                    f'title="Token ID: {token_id}">{token}</span>'
                )
            
            st.markdown(
                f'<div class="token-display">{"".join(html_tokens)}</div>',
                unsafe_allow_html=True
            )
            
            # Show token IDs for copying
            st.markdown("### Token IDs")
            st.code(", ".join(map(str, token_ids)), language="text")
            
            # Show token mapping
            st.markdown("### Token Mapping")
            mapping_text = []
            for i, (token, token_id) in enumerate(zip(tokens, token_ids), 1):
                mapping_text.append(f"{i}. '{token}' → ID {token_id}")
            
            st.markdown(
                f'<div class="token-mapping">' + 
                '<br>'.join(mapping_text) + 
                '</div>',
                unsafe_allow_html=True
            )

    with decode_tab:
        token_input = st.text_area(
            "Enter Token IDs (comma-separated)",
            value="",
            height=100,
            key="decode_input",
            help="Enter comma-separated token IDs to decode back to text"
        )

        if st.button("Clear", key="clear_decode", type="secondary"):
            st.session_state.decode_input = ""
            st.experimental_rerun()

        if token_input:
            try:
                token_ids = [int(id.strip()) for id in token_input.split(",")]
                decoded_text = decode_text(tokenizer, token_ids)
                
                st.markdown("### Decoded Text")
                st.markdown(
                    f'<div class="token-display">{decoded_text}</div>',
                    unsafe_allow_html=True
                )
                
                st.markdown("### Token Mapping")
                mapping_text = []
                for i, token_id in enumerate(token_ids, 1):
                    if token_id in tokenizer.itos:
                        mapping_text.append(f"{i}. ID {token_id} → '{tokenizer.itos[token_id]}'")
                    else:
                        mapping_text.append(f"{i}. ID {token_id} → [Unknown Token]")
                
                st.markdown(
                    f'<div class="token-mapping">' + 
                    '<br>'.join(mapping_text) + 
                    '</div>',
                    unsafe_allow_html=True
                )
                        
            except ValueError:
                st.error("Invalid input format. Please enter comma-separated numbers.")
            except Exception as e:
                st.error(f"Error during decoding: {e}")

if __name__ == "__main__":
    main() 