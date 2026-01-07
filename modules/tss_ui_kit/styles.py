"""
TSS UI Kit - CSS Styles and Themes
Complete styling system for professional Streamlit applications.
"""

def get_custom_css() -> str:
    """Get complete custom CSS for TSS UI Kit styling"""
    return """
<style>
    /* Global font unification */
    *, *::before, *::after,
    html, body, 
    [class*="css"], 
    .stApp,
    .stMarkdown,
    .stText,
    .stCaption,
    .stButton,
    .stSelectbox,
    .stFileUploader,
    .stExpander,
    .stMetric,
    .stProgress,
    div, span, p, h1, h2, h3, h4, h5, h6,
    button, input, textarea, select {
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        font-feature-settings: normal !important;
        text-rendering: optimizeLegibility !important;
    }
    
    /* Force consistent font rendering */
    .stApp * {
        font-family: inherit !important;
        text-shadow: none !important;
    }
    
    /* Main app styling */
    .main-header {
        text-align: center !important;
        color: #111827;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        background: transparent;
        width: 100% !important;
        display: block !important;
    }
    
    .main-header h1 {
        color: #111827;
        font-weight: 600;
        font-size: 1.875rem;
        margin-bottom: 0.125rem;
        letter-spacing: -0.025em;
        margin-top: 0;
        text-align: center !important;
        width: 100% !important;
    }
    
    .main-header p {
        color: #6b7280;
        font-weight: 400;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 0;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Upload area styling - compact version */
    .upload-area-compact {
        border: 1px dashed #d1d5db;
        border-radius: 6px;
        padding: 0.75rem;
        text-align: center;
        margin: 0.5rem auto;
        background-color: #f9fafb;
        transition: all 0.15s ease;
        width: 70%;
        max-width: 800px;
        min-width: 350px;
    }
    
    /* Compact spacing for file uploader */
    .stFileUploader {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        width: 70% !important;
        max-width: 800px !important;
        min-width: 350px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    .upload-area-compact:hover {
        border-color: #9ca3af;
        background-color: #f3f4f6;
    }
    
    .upload-title {
        color: #374151 !important;
        font-weight: 600 !important;
        margin: 0 0 0.25rem 0 !important;
        font-size: 1.1rem !important;
    }
    
    .upload-subtitle {
        color: #6b7280 !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }
    
    /* Legacy upload area - keep for compatibility */
    .upload-area {
        border: 1px dashed #d1d5db;
        border-radius: 8px;
        padding: 0.1875rem;
        text-align: center;
        margin: 0.125rem 0 0.375rem 0;
        background-color: #f9fafb;
        transition: all 0.15s ease;
    }
    
    .upload-area:hover {
        border-color: #9ca3af;
        background-color: #f3f4f6;
    }
    
    .upload-area h3 {
        color: #374151;
        font-weight: 500;
        margin-bottom: 0.125rem;
        font-size: 1rem;
        margin-top: 0;
    }
    
    .upload-area p {
        color: #6b7280;
        font-weight: 400;
        font-size: 0.875rem;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    /* Progress bar container - compact version */
    .progress-container-compact {
        margin: 0.5rem 0;
        padding: 0.75rem;
        background-color: #ffffff;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
    }
    
    .progress-title {
        color: #111827 !important;
        font-weight: 600 !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 1.1rem !important;
    }
    
    /* Legacy progress container */
    .progress-container {
        margin: 1rem 0;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
    }
    
    .progress-container h3 {
        color: #111827;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    /* Step indicators */
    .step-indicator {
        display: block;
        margin: 0.75rem 0;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }
    
    .step-completed {
        background-color: #f0f9f4;
        border: 1px solid #d1fae5;
        color: #065f46;
    }
    
    .step-running {
        background-color: #fffbeb;
        border: 1px solid #fed7aa;
        color: #92400e;
    }
    
    .step-pending {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        color: #6b7280;
    }
    
    .step-error {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
    }
    
    /* Download section - centered and consistent width with reduced height */
    .download-section {
        background-color: #f0f9f4;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.75rem auto;
        text-align: center;
        border: 1px solid #d1fae5;
        width: 70%;
        max-width: 800px;
        min-width: 350px;
        box-sizing: border-box;
    }
    
    .download-section h3 {
        color: #065f46;
        font-weight: 500;
        font-size: 0.875rem;
        margin: 0 0 0.25rem 0;
    }
    
    .download-section p {
        color: #047857;
        font-weight: 400;
        font-size: 0.875rem;
        margin: 0;
    }
    
    /* Info boxes - match upload box width */
    .info-box {
        padding: 0.75rem 1rem;
        margin: 0.75rem auto;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        background-color: #f8fafc;
        color: #374151;
        font-weight: 400;
        font-size: 0.875rem;
        width: 70%;
        max-width: 800px;
        min-width: 350px;
        box-sizing: border-box;
    }
    
    .success-box {
        border-color: #d1fae5;
        background-color: #f0f9f4;
        color: #065f46;
    }
    
    .warning-box {
        border-color: #fed7aa;
        background-color: #fffbeb;
        color: #92400e;
    }
    
    .error-box {
        border-color: #fecaca;
        background-color: #fef2f2;
        color: #991b1b;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #9ca3af;
        font-size: 0.75rem;
        font-weight: 400;
        margin-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        color: #111827;
        font-weight: 600;
        line-height: 1.25;
    }
    
    p {
        color: #4b5563;
        line-height: 1.6;
    }
    
    /* Perfect button centering container using CSS Grid with debug border */
    .button-center-container {
        width: 70% !important;
        max-width: 800px !important;
        min-width: 350px !important;
        margin: 1rem auto !important;
        display: grid !important;
        place-items: center !important;
        box-sizing: border-box !important;
        box-shadow: 0 0 0 2px red !important; /* DEBUG: Red outline for button container */
        min-height: 60px !important; /* DEBUG: Ensure container has height */
    }
    
    .button-center-container .stButton {
        width: 100% !important;
        margin: 0 !important;
        justify-self: center !important;
        align-self: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .button-center-container .stButton > div {
        width: 100% !important;
        margin: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Aggressive button centering - override all Streamlit defaults */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    .stButton > button {
        font-weight: 500 !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
        z-index: 10 !important;
        position: relative !important;
        white-space: nowrap !important;
        overflow: visible !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 1rem !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
        margin: 0 auto !important;
        width: auto !important;
    }
    
    /* Button inside grid container - force center everything */
    .button-center-container .stButton > button {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: auto !important;
        margin: 0 auto !important;
    }
    
    /* Force all button content to center */
    .button-center-container .stButton button {
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .button-center-container .stButton > button > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
        margin: 0 !important;
    }
    
    /* Grid container child elements - nuclear option centering */
    .button-center-container > * {
        justify-self: center !important;
        align-self: center !important;
    }
    
    /* Nuclear option - override everything Streamlit does */
    div.button-center-container > div.stButton,
    div.button-center-container > div.stButton > div,
    div.button-center-container > div.stButton > div > div {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
    }
    
    div.button-center-container button[kind="primary"] {
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Force center alignment on button text content */
    .stButton > button > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Target button content more specifically */
    .stButton > button > div > p,
    .stButton > button > div > span,
    .stButton > button p,
    .stButton > button span {
        text-align: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* Primary button blue styling with forced centering */
    .stButton > button[kind="primary"] {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
        color: #ffffff !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
        margin: 0 auto !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #ffffff !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .stButton > button[kind="primary"]:focus {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
        color: #ffffff !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* Force white text and centering for primary button content */
    .stButton > button[kind="primary"] * {
        color: #ffffff !important;
        text-align: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
    }
    
    .stButton > button[kind="primary"]:hover * {
        color: #ffffff !important;
        text-align: center !important;
        justify-content: center !important;
    }
    
    /* Primary button text content specifically */
    .stButton > button[kind="primary"] > div,
    .stButton > button[kind="primary"] > div > p,
    .stButton > button[kind="primary"] > div > span {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    
    /* Compact layout adjustments for better space utilization */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* Reduce default Streamlit spacing */
    .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
    
    /* Standardize body text sizes */
    .stMarkdown p, .element-container p {
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }
    
    /* File uploader text standardization */
    .stFileUploader label, .stFileUploader div {
        font-size: 0.9rem !important;
    }
    
    /* Enhanced button text standardization with aggressive centering */
    .stButton button {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
        margin: 0 auto !important;
        width: auto !important;
    }
    
    /* All button content must be centered */
    .stButton button * {
        text-align: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Primary button enhanced styling with maximum centering */
    .stButton > button[kind="primary"] {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
        z-index: 100 !important;
        position: relative !important;
        margin: 1rem auto !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
        width: auto !important;
    }
    
    /* Force center on primary button inner content */
    .stButton > button[kind="primary"] div,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
        margin: 0 auto !important;
        width: 100% !important;
    }
    
    /* Progress text standardization */
    .stProgress div {
        font-size: 0.9rem !important;
    }
    
    /* Responsive optimizations */
    @media (max-width: 768px) {
        .app-header-container {
            max-width: 95% !important;
        }
        
        .compact-title {
            font-size: 2.1rem !important;
        }
        
        .compact-subtitle {
            font-size: 0.9rem !important;
        }
        
        .upload-title {
            font-size: 1rem !important;
        }
        
        .upload-subtitle {
            font-size: 0.85rem !important;
        }
        
        .progress-title {
            font-size: 1rem !important;
        }
        
        /* Mobile button adjustments with aggressive centering */
        .stButton {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
            width: 100% !important;
        }
        
        .stButton button {
            font-size: 1.1rem !important;
            padding: 0.65rem 1.25rem !important;
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            display: flex !important;
            margin: 0 auto !important;
            width: auto !important;
        }
        
        .stButton button * {
            text-align: center !important;
            justify-content: center !important;
            margin: 0 auto !important;
            display: flex !important;
            align-items: center !important;
        }
        
        .stButton > button[kind="primary"] {
            font-size: 1.1rem !important;
            padding: 0.65rem 1.25rem !important;
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            display: flex !important;
            margin: 0 auto !important;
            width: auto !important;
        }
        
        .stButton > button[kind="primary"] div,
        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span {
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            display: flex !important;
            margin: 0 auto !important;
            width: 100% !important;
        }
        
        .upload-area-compact {
            padding: 0.5rem !important;
            margin: 0.25rem auto !important;
            width: 90% !important;
            min-width: 320px !important;
        }
        
        .stFileUploader {
            width: 90% !important;
            min-width: 320px !important;
        }
        
        .progress-container-compact {
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
        }
    }
    
    /* Viewport height optimization */
    .main .block-container {
        min-height: auto !important;
    }
    
    .stMarkdown h2 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .stMarkdown h3 {
        margin-top: 2.25rem;
        margin-bottom: 0.5rem;
        font-size: 1.125rem;
        font-weight: 500;
    }
    
    /* Fix overlapping text in expanders */
    .streamlit-expanderHeader {
        z-index: 10 !important;
        position: relative !important;
        background: white !important;
        line-height: 1.5 !important;
        padding: 0.75rem 1rem !important;
        margin: 0 !important;
        display: block !important;
        width: 100% !important;
        overflow: hidden !important;
        transform: translateZ(0) !important;
        isolation: isolate !important;
    }
    
    /* Hide any pseudo-elements that might cause duplicate text */
    .streamlit-expanderHeader::before,
    .streamlit-expanderHeader::after {
        display: none !important;
        content: none !important;
    }
    
    /* Fix expander content spacing */
    .streamlit-expanderContent {
        background: white !important;
        padding: 0.5rem 1rem !important;
        z-index: 5 !important;
        margin-top: 0.25rem !important;
        clear: both !important;
    }
    
    /* Compact header styling */
    .app-header-container {
        margin: 0.5rem auto !important;
        text-align: center !important;
    }
    
    .compact-title {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
        margin: 0.5rem 0 0.25rem 0 !important;
        text-align: center !important;
        line-height: 1.2 !important;
    }
    
    .compact-subtitle {
        font-size: 1rem !important;
        color: #6b7280 !important;
        margin: 0 0 0.5rem 0 !important;
        text-align: center !important;
        line-height: 1.4 !important;
    }
    
    /* Hide Streamlit branding elements */
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide GitHub button specifically */
    button[title="View app source on GitHub"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide the entire toolbar area */
    .stToolbar {
        display: none !important;
    }
    
    /* Hide Share, Star, Edit buttons */
    [aria-label="Share"],
    [aria-label="Star"],
    [aria-label="Edit"],
    [title="Star"],
    [title="Share"],
    [title="Edit"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide Manage app section */
    [data-testid="manage-app-button"],
    .css-1kyxreq,
    .css-k1vhr4 {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide top toolbar completely */
    .css-1rs6os.edgvbvh3,
    .css-18e3th9,
    .css-1d391kg.e1fqkh3o3 {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide any GitHub related elements */
    [href*="github.com"],
    a[href*="github"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Generic toolbar hiding */
    header[data-testid="stToolbar"],
    .stToolbar,
    .toolbar {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide Streamlit footer "Made with Streamlit" */
    footer,
    .stApp > footer,
    [data-testid="stFooter"],
    footer[data-testid="stFooter"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide any footer elements */
    .css-1d391kg footer,
    .main footer,
    footer.stFooter {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Force hide footer with more specific selectors */
    div[data-testid="stFooter"],
    .stApp footer,
    .stMarkdown footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Center download button within download section */
    .download-section .stDownloadButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 1rem auto !important;
        text-align: center !important;
    }
    
    .download-section .stDownloadButton > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    
    .download-section .stDownloadButton button {
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }
    
    /* Ensure all elements in download section are centered */
    .download-section > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }
</style>
"""

def get_dark_theme_css() -> str:
    """Get dark theme variant of the CSS"""
    return """
<style>
    /* Dark theme override */
    .stApp {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
    }
    
    .main-header h1 {
        color: #f1f5f9 !important;
    }
    
    .main-header p {
        color: #94a3b8 !important;
    }
    
    .upload-area-compact {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #f1f5f9 !important;
    }
    
    .upload-area-compact:hover {
        background-color: #334155 !important;
        border-color: #64748b !important;
    }
    
    .upload-title {
        color: #f1f5f9 !important;
    }
    
    .upload-subtitle {
        color: #94a3b8 !important;
    }
    
    .progress-container-compact {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }
    
    .progress-title {
        color: #f1f5f9 !important;
    }
    
    .info-box {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #f1f5f9 !important;
    }
    
    .success-box {
        background-color: #064e3b !important;
        border-color: #059669 !important;
        color: #34d399 !important;
    }
    
    .warning-box {
        background-color: #92400e !important;
        border-color: #d97706 !important;
        color: #fbbf24 !important;
    }
    
    .error-box {
        background-color: #7f1d1d !important;
        border-color: #dc2626 !important;
        color: #fca5a5 !important;
    }
    
    .download-section {
        background-color: #064e3b !important;
        border-color: #059669 !important;
    }
    
    .download-section h3 {
        color: #34d399 !important;
    }
    
    .download-section p {
        color: #6ee7b7 !important;
    }
    
    .footer {
        color: #64748b !important;
        border-top-color: #475569 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    p {
        color: #cbd5e1 !important;
    }
</style>
"""

def get_minimal_css() -> str:
    """Get minimal CSS for basic styling only"""
    return """
<style>
    /* Minimal styling - just essentials */
    .stApp {
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    .upload-area-compact {
        border: 1px dashed #d1d5db;
        border-radius: 6px;
        padding: 0.75rem;
        text-align: center;
        margin: 0.5rem 0;
        background-color: #f9fafb;
    }
    
    .progress-container-compact {
        margin: 0.5rem 0;
        padding: 0.75rem;
        background-color: #ffffff;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
    }
    
    .info-box {
        padding: 0.75rem 1rem;
        margin: 0.75rem 0;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        background-color: #f8fafc;
    }
    
    .success-box {
        border-color: #d1fae5;
        background-color: #f0f9f4;
        color: #065f46;
    }
    
    .error-box {
        border-color: #fecaca;
        background-color: #fef2f2;
        color: #991b1b;
    }
    
    .warning-box {
        border-color: #fed7aa;
        background-color: #fffbeb;
        color: #92400e;
    }
    
    /* Hide Streamlit branding */
    [data-testid="stToolbar"],
    .stToolbar,
    button[title="View app source on GitHub"] {
        display: none !important;
    }
</style>
"""

# Color themes
THEMES = {
    "default": {
        "primary": "#2563eb",
        "success": "#065f46", 
        "error": "#991b1b",
        "warning": "#92400e",
        "info": "#374151",
        "background": "#ffffff",
        "surface": "#f9fafb"
    },
    "dark": {
        "primary": "#3b82f6",
        "success": "#10b981",
        "error": "#ef4444", 
        "warning": "#f59e0b",
        "info": "#94a3b8",
        "background": "#0f172a",
        "surface": "#1e293b"
    },
    "minimal": {
        "primary": "#000000",
        "success": "#16a34a",
        "error": "#dc2626",
        "warning": "#ca8a04", 
        "info": "#64748b",
        "background": "#ffffff",
        "surface": "#f8fafc"
    }
}